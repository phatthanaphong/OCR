from loadModel import loadModel
from CharRecognition import CharRecognition
import sys, json
from ctypes import *
# give location of dll
#modeldll = cdll.LoadLibrary('C:\\inetpub\\wwwroot\\TextPrepPilot\\ORCModule\\model.dll')
#def loadmodel():
    #fn  = str(sys.argv)
    #fn  = 'C:\\inetpub\\wwwroot\\TextPrepPilot\\ORCModule\\im10.jpg'
    #model = loadModel('charmodelmix55.cnn')
    #out   = CharRecognition(fn, model)
    #print(out)
    #model = 'xxxx'
    #if model != None:
    #    return 'cannot load model'
    #else:
    #    return model

#value = sys.argv[0]
#v = loadmodel()
#data = {"fail" : 35}
#sys.stdout.write(str(data))
fn  = sys.argv[1]# 'C:\\inetpub\\wwwroot\\TextPrepPilot\\OCRModule\\im10.jpg'
#mdll= ctypes.WinDLL ("C:\\inetpub\\wwwroot\\TextPrepPilot\\ORCModule\\model.dll")#= loadModel('charmodelmix55.cnn')
model = loadModel('charmodelmix55.cnn') 
out   = CharRecognition(fn, model)
tmp = ''
for l in out:
    for lp in l:
        tmp = tmp+lp
    tmp = tmp+'\n'
#s = unicode(tmp, "utf-8")
print(tmp)
