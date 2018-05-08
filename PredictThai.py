import numpy as np
import cv2
import tflearn
from tflearn.layers.core import input_data, dropout, fully_connected
from tflearn.layers.conv import conv_2d, max_pool_2d
from tflearn.layers.normalization import local_response_normalization
from tflearn.layers.estimator import regression

def categoryForNumber(num):
    thai = {
        1:"#",
        2:"$",
        3:"&",
        4:",",
        5:"(",
        6:")",
        7:"*",
        8:"+",
        9:",",
        10:"่", #-
        11:".",
        12:"/",
        13:"0",
        14:"1",
        15:"2",
        16:"3",
        17:"4",
        18:"5",
        19:"6",
        20:"7",
        21:"8",
        22:"9",
        23:"<",
        24:">",
        25:"?",
        26:"@",
        27:"A",
        28:"B",
        29:"C",
        30:"D",
        31:"E",
        32:"F",
        33:"G",
        34:"H",
        35:"I",
        36:"J",
        37:"K",
        38:"L",
        39:"M",
        40:"N",
        41:"O",
        42:"P",
        43:"Q",
        44:"R",
        45:"S",
        46:"T",
        47:"U",
        48:"V",
        49:"W",
        50:"X",
        51:"Y",
        52:"Z",
        53:"[",
        54:"\\",
        55:"]",
        56:"a",
        57:"b",
        58:"c",
        59:"d",
        60:"e",
        61:"f",
        62:"g",
        63:"h",
        64:"i",
        65:"j",
        66:"k",
        67:"l",
        68:"m",
        69:"n",
        70:"o",
        71:"p",
        72:"q",
        73:"r",
        74:"s",
        75:"t",
        76:"u",
        77:"v",
        78:"w",
        79:"x",
        80:"y",
        81:"z",
        82:"{",
        83:"|",
        84:"}",
        85:"ก",
        86:"ข",
        87:"ฃ",
        88:"ค",
        89:"ฅ",
        90:"ฆ",
        91:"ง",
        92:"จ",
        93:"ฉ",
        94:"ช",
        95:"ซ",
        96:"ฌ",
        97:"ญ",
        98:"ฎ",
        99:"ฏ",
        100:"ฐ",
        101:"ฑ",
        102:"ฒ",
        103:"ณ",
        104:"ด",
        105:"ต",
        106:"ถ",
        107:"ท",
        108:"ธ",
        109:"น",
        110:"บ",
        111:"ป",
        112:"ผ",
        113:"ฝ",
        114:"พ",
        115:"ฟ",
        116:"ภ",
        117:"ม",
        118:"ย",
        119:"ร",
        120:"ฤ",
        121:"ล",
        122:"ภ",
        123:"ว",
        124:"ศ",
        125:"ษ",
        126:"ส",
        127:"ห",
        128:"ฬ",
        129:"อ",
        130:"ฮ",
        131:"ฯ",
        132:"ั",
        133:"า",
        134:"ิ",
        135:"ี",
        136:"ึ",
        137:"ื",
        138:"ุ",
        139:"ู",
        140:"โ",
        141:"เ",
        142:"โ",
        143:"ใ",
        144:"ไ",
        145:"า",
        146:"ิ",#ๆ
        147:"็",
        148:"่",
        149:"้",
        150:"๊",
        151:"๋",
        152:"์",
        153:"ำ",
        154:"๐",
        155:"๑",
        156:"๒",
        157:"๓",
        158:"๔",
        159:"๕",
        160:"๖",
        161:"๗",
        162:"๘",
        163:"๙"}
    if num ==  134:
        return "ิ"
    return thai.get(num)


## parameters:
##  im     : image (imread from openCV lib)
##  model  : a predictve model trained  by a CNN

def predictThai(im, model):
    #b = imresize(im, [55,55])
    #img = cv2.imread(im,0)
    h,w =  im.shape
    scale1 = 55/w;
    scale2 = 55/h;
    tmpb = cv2.resize(im
        , None
        , fx= scale1
        , fy= scale2
        , interpolation=cv2.INTER_CUBIC)
    
    b = np.array(tmpb)
    tmp = b.flatten()
    tmp = tmp.reshape([-1, 55, 55, 1])
    predict = model.predict(tmp)
    a = predict[0]
    p = np.where(a == a.max())[0]
    k = p[0]
    if k == 133:
        k = 145
    k = k+1
    ans =categoryForNumber(k)
    del tmp
    return ans




