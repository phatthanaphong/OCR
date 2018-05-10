import glob
import errno
import os
import cv2
import numpy as np
import math
#th = 183
scale = 2

# ============================================================================


def clean_image(img,fi,path):
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    resized_img = cv2.resize(gray_img
        , None
        , fx= scale
        , fy= scale
        , interpolation=cv2.INTER_CUBIC)

    #resized_img = cv2.GaussianBlur(resized_img,(3,3),0)
    #cv2.imwrite(fn, resized_img)

    ## threshold out with a pre-determined th -- declare at the beginning of the code
    ret, _ = cv2.threshold(resized_img,0,255,cv2.THRESH_OTSU)
    ret, mask0 = cv2.threshold(resized_img, ret+8, 255, cv2.THRESH_BINARY)

    ## erosion 
    bw_image = cv2.bitwise_not(mask0)
    kernel = np.ones((1,1), np.uint8)
    bw_image = cv2.erode(bw_image, kernel, iterations=1)
    mask = cv2.bitwise_not(bw_image)

    #mask = mask0
    
    del gray_img, resized_img
    return mask


# ============================================================================

def extract_characters(img0, img, fi,path, model):
    bw_image = cv2.bitwise_not(img)
    _, contours, hierarchy = cv2.findContours(bw_image,cv2.RETR_CCOMP,cv2.CHAIN_APPROX_SIMPLE)
    char_mask = np.zeros_like(img)
    bounding_boxes = []
    sz_area=img.size
    small_sz=sz_area*0.00002
    large_sz=sz_area*0.2
    c=0
    width,height = img.shape
    
    while c>=0:
        contour=contours[c]     
        x,y,w,h = cv2.boundingRect(contour)
        area = w * h
        center = (x + w/2, y + h/2)
        if (area>small_sz and area < large_sz):
            xx=x+w
            yy=y+h
            hh=h
            ww=w
            chIm = np.zeros((hh,ww),np.uint8)
            chIm = img[y:yy,x:xx]
            
            a=0
            
            for i in range(y,yy):
                b=0
                for j in range(x,xx):
                    d=cv2.pointPolygonTest(contour,(j,i),False)
                    if d<=0.0:
                        chIm.itemset((a,b),255)
                    b=b+1
                a=a+1

            x,y,w,h = x, y, w, h
            bounding_boxes.append((x, center, (x,y,w,h),chIm))
            cv2.rectangle(char_mask,(x,y),(x+w,y+h),255,-1)
        c=hierarchy[0][c][0]

    clean = cv2.bitwise_not(cv2.bitwise_and(char_mask, char_mask, mask = bw_image))

    characters = []
    line_char  = []
    
    ## order according to x of the bounding box -- not the center of the bb
    bounding_boxes = sorted(bounding_boxes, key=lambda item: item[0])

    for xx, center, bbox, chIm in bounding_boxes:
        x,y,w,h = bbox
        xx=x+w
        yy=y+h

##        ## avoid small object at the pre - next lines, 5 can be changed
##        if y > 5  and y < height-5 :        
##            
##            if model != None:
##                a = predictThai(char_image, model)
##                line_char.append(a)
        char_image = clean[y:yy,x:xx]
        characters.append((x, y, bbox, char_image))

    del bw_image
    return line_char, img, clean, characters


def highlight_characters(img, chars):
    output_img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
    for xx, yy, bbox, char_img in chars:
        x,y,w,h = bbox
        cv2.rectangle(output_img,(x,y),(x+w,y+h),255,1)

    return output_img


# ============================================================================    


def processNoPredict(name):
    pathIn, finame = os.path.split(name)
    fi=os.path.splitext(finame)[0]
    imgori = cv2.imread(name,1)
    if imgori == None : 
        print("cannot load images")
        return (None, None)
    h,w  = imgori.shape[:2]
    img  = clean_image(imgori,fi,pathIn)
    recog, img0, block_img, chars = extract_characters(imgori, img, fi,pathIn, None)

    del img0
    del img
    del imgori
    return chars, block_img




##path = 'D:\character/*.png' #note C:
##files = glob.glob(path)
##for name in files:
##    try:
####        with open(name) as f:
##        print(name)
##        print('please wait processing...')
          ##model = loadModel()
##        process(name, model)
##
##    except IOError as exc: #Not sure what error this is
##        if exc.errno != errno.EISDIR:
##            raise
##    print("\n")
