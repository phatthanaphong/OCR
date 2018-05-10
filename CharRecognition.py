import glob
import errno
import os
import cv2
import numpy as np
from   ContourCharAndRecognize import processNoPredict
import statistics
import math
from   PredictThai import predictThai
from   FormatText import formatText1


# ============================================================================    
def gaussian(x, mu, sig):
    return np.exp(-np.power((x - mu)/sig, 2.)/2)


# ============================================================================    
def distance(x1,y1,x2,y2):
    return math.aqrt((x1-x2)**2 + (y1-y2)**2)


# ============================================================================    
def checkIntersec(a,b,c,d):
    if (c>a and c <b) :
        return 1
    if (d>a and d < b) :
        return 1
    return 0


# ============================================================================    
def findNB(t, tmp):
    x,y,w,h = t
    l = len(tmp)
    ret = []
    for i in range(l):
        bi,xx,yy,bbox,char_img = tmp[i]
        if xx < 0 and yy < 0:
            continue
        x1, y1, w1, h1 = bbox
        cx = x1+(w1/2)
        cy = y1+(h1/2)
        if x < cx and cx < x+w and y < cy and cy < y+h:
             ret.append((i,bi,xx,yy,bbox,char_img))

    return ret

# The main function to perform the detection and recognition
# ============================================================================    
def CharRecognition(file, modelFile):
    
        chars, im = processNoPredict(file)

        if  im == None:
            return None
    
        model = loadModel(modelFile) 
        output_img = cv2.cvtColor(im, cv2.COLOR_GRAY2BGR)

        max_char = 100
        min_char = 10
        
        no_all = len(chars)

        if max_char < max_char:
            max_char = no_all;

        mx = 0
        th = []
        wh = []
        for d, v, bbox, char_img in chars:
            x,y,w,h = bbox
            th.append(h)
            wh.append(w)
            
        mx = statistics.median(th)*2.5
        wx = statistics.median(wh)
        
        trans = []

        ## maximum/page
        page_line = 120

        #-----------------------------------------------
        # Detectioin part
        #-----------------------------------------------
        
        ## loop through each line 
        for p in range(page_line):
            if len(chars) == 0 :
                break
            
            ##sort along y-axis
            chars = sorted(chars, key=lambda x: x[1])
            
            ## initializing variables
            tmp = []
            m = 0
            v = mx
            t = []
            ht = []
            no_all = len(chars)
            
            if max_char > no_all:
               max_char = no_all;

            ## ks-test the center of each block in x-direction is uniform
            for bi in range(max_char):
                if chars[bi] != None:
                    xx,yy,bbox,char_img = chars[bi]
                    x,y,w,h = bbox
                    ceny = y+(h/2)
                    if bi == 0:
                        tmp.append((bi,x,y,bbox,char_img))
                        t.append(ceny)
                        m = ceny
                        
                    else:
                        f = gaussian(y, m, v)
                        if f > 0.90 :
                             tmp.append((bi,x,y,bbox,char_img))
                             t.append(ceny)
                             m = statistics.mean(t)


            tmp =sorted(tmp, key=lambda x: x[1])
            
            ## tracing by the lower boundary
            line_tmp = []
            l = len(tmp)
            flag = 0
            
            for i in range(l):
                bi,x,y,bbox,char_img = tmp[i]
                if i == 0:
                        x0,y0,w0,h0 = bbox
                        #line_tmp.append((bi,x,y,bbox,char_img))
                        cury = y0+(h0/2)
                        curh = y0+h0
                        #cv2.rectangle(output_img,(x,y),(x+w,y+h),(0,0,255),2)
                
                if x >= 0 and y >=0 :
                        x1,y1,w1,h1 = bbox
                        cenx = x1+(w1/2)
                        ceny = y1+(h1/2)
                        yh = y1+h1
                       
                        if math.sqrt((yh-curh)**2) > 15:
                            continue
                        
                        line_tmp.append((bi,x,y,bbox,char_img))
                        tmp[i] = (-1,-1,-1,0,0)
                        cury = y1+(h1/2);
                        curh = y1+h1
                        
                        xn = x1
                        yn = int(y1 - (mx*0.35))
                        wn = w1
                        hn = int(h1 + (mx*0.20)+(y1-yn))

                        ls = findNB((xn,yn,wn,hn), tmp)
                        ls = sorted(ls, key=lambda x: x[3], reverse=True)

                        if ls:
                            for (ix,bi,xx,yx,bboxx,char_imgx) in ls:
                                line_tmp.append((bi,xx,yy,bboxx,char_imgx))
                                tmp[ix] = (-1,-1,-1,0,0)
                            
                        
                        ##  cv2.rectangle(output_img,(xn,yn),(xn+wn,yn+hn),(0,0,255),2)
                        ##  cv2.rectangle(output_img,(x1,y1),(x1+w1,y1+h1),(0,0,255),2)
                        ##  cv2.namedWindow('Original',0)
                        ##  cv2.imshow('Original',output_img)
                        ##  cv2.waitKey(0)
                    
            for  bi,x,y,bbox,char_img in line_tmp:
                chars[bi] = None
           
            chars = [x for x in chars if x is not None]

            tmp = line_tmp
            line = []
            l = len(tmp)
            insertidx = []

            #-----------------------------------------------
            # Recognition part
            #-----------------------------------------------
            for i in range(l):
                bi,xx1,yy1,bbox1,char_image1 = tmp[i]
                x1,y1,w1,h1 = bbox1
                cv2.rectangle(output_img,(x1,y1),(x1+w1,y1+h1),(0,0,255),2)
                ## drawing sequence
                if i < l-1:
                    bi,xx2,yy2,bbox2,char_image2 = tmp[i+1]
                    x2,y2,w2,h2 = bbox2
                    ## for visualization
                    ## cv2.circle(output_img,(int(x1+(w1/2)),int(y1+(h1/2))),3,(255,0,0),-1)
                    ## cv2.line(output_img,(int(x1+(w1/2)),int(y1+(h1/2))),(int(x2+(w2/2)),int(y2+(h2/2))),(255,0,0),2)

                    a = predictThai(char_image1, model)
                    
                    line.append(a)
        
                    ## checking for white spaces
                    if (math.sqrt((x1 - x2)**2) > wx*1.65) and (math.sqrt((y1 - y2)**2) < 3):
                        a = ' '
                        line.append(a)

                else:
                    a = predictThai(char_image1, model)
                    line.append(a)


            line = formatText1(line)
            if len(line) > 1 :
                trans.append(line)

            return trans
