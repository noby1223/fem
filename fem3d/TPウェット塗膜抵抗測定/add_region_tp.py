import numpy as np

def addregion(m):

    
    bd_ws = [[0],[0]]#wetの凸regionを追加していくよ(4枚ボックスのようにWET領域が複数ある場合、ここでまとめる)
    ws = [34]#WET凸領域  　　　　　　　　　　　　領域を変更するのはここｗｓとｗｓｆ１とｗｓｆだけ
    region_w = []
    for w in ws:
        bd_ws = np.hstack([bd_ws,m.region(w)])
        region_w += [w]*len(m.region(w)[0])

    bd_ws = np.delete(bd_ws,0,1)


    bd_wsf1 = [[0],[0]]#wetの面region(0v方)を追加していくよ
    wsf1 = [24]#WETの面
    for w in wsf1:
        bd_wsf1 = np.hstack([bd_wsf1,m.region(w)])
    bd_wsf1 = np.delete(bd_wsf1,0,1)#１列目削除しないと最初の0０が入ってしまう

    bd_wsf2 = [[0],[0]]#wetの面region(0vじゃない)を追加していくよ
    wsf = [14]#WETの面
    for w in wsf:
        reg1, reg2 = np.split(m.region(w), 2, 1)#reg1は塗料側、reg2はボディ側の凸、面は共有
        bd_wsf2 = np.hstack([bd_wsf2,reg2])
    bd_wsf2 = np.delete(bd_wsf2,0,1)#１列目削除しないと最初の0０が入ってしまう

    return bd_ws,bd_wsf1,bd_wsf2,ws,reg1,reg2,region_w