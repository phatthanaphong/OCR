import numpy as np


def formatText1(l):
    t1 = []
    k=1
    ## for ะ
    for i in range(0,len(l)):
         if l[i] != '' or l[i] != ' ':
             if k == 0:
                k=1
                continue
             a1 = l[i]
             if i < len(l)-1:
                 a2 = l[i+1]
                 if a1 == a2  and a1 == 'ั':
                     t1.append(('ะ'))
                     k=0
                 else:
                     t1.append(a1)
                     k=1
             else:
                 t1.append(a1)
    if len(t1) == 0 :
        return t1
    t2 = []
    k = 1
    ## for ำ า
    for i in range(0,len(t1)):
         if k == 0:
            k=1
            continue
         a1 = t1[i]
         if i < len(t1)-1:
             a2 = t1[i+1]
             if (a1 == 'ำ' and a2 == 'า') or (a1 == 'ญ' and a2 == 'ั') or (a1 == 'ญ' and a2 == '้'):
                 t2.append(a1)
                 k=0
             else:
                 t2.append(a1)
                 k=1
         else:
             t2.append(a1)

##    t3 = []
##    k = 1
##    ## for ำ า
##    for i in range(0,len(t2)):
##         if k == 0:
##            k=1
##            continue
##         a1 = t2[i]
##         if i > 0 and i < len(t2)-1:
##             a2 = t2[i+1]
##             a3 = t2[i-1]
##             if (a1 == 'ิ' and a3 == 'เ') or (a1 == 'ื' and a3 == 'เ') or (a1 == 'ี' and a3 == 'เ') or (a1 == 'ิ' and a3 == 'ะ') or (a1 == 'ิ' and a3 == 'า'):
##                 t3.append(a2)
##                 t3.append(a1)
##                 k=0
##             else:
##                 t3.append(a1)
##                 k=1
##         else:
##             t3.append(a1)


    return t2
