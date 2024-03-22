import pandas as pd
import numpy as np


def wet_conduct(I_sekisan,bd2,area_hairetu,i_ori):

    I_sekisan_w = np.delete(I_sekisan,slice(0,len(bd2[0])))

    df = pd.read_excel('/home/noby/fem/fem3d/TPウェット塗膜抵抗測定/resistance_data/WET電導度計算用20240215_150V_ソフトS150秒_PVC容器＿300s_攪拌なし＿.xlsx')
    data_sekisan = df['積算電流A/mm']#70mm*70mm 単位はmA/㎟
    data_sekisan[0] = 0#何も入れないとnanなので
    resi = df['電導度換算（厚さ0.1ミリ）']
    roh_hairetu = []
    
    
    
    for i in range(len(I_sekisan_w)):

        area_hairetu[i] = area_hairetu[i]*1000000#m㎡に換算
        
        for i2 in range(len(data_sekisan)):

            

            if I_sekisan_w[i]/(area_hairetu[i]) <= data_sekisan[0] :#一番低いときは塗料と同じ電導度にする
                roh = 100#mS/m
                roh_hairetu.append(roh)
                break


            if i2 == len(data_sekisan)-1:#i2がラストになってしまうと＋１でエラーが出てしまうため、ここで条件分岐
                roh = resi[i2-1]*1000 #1/resi[i2-1]/(0.07*0.07)*0.0001#ρ　＝　S＊ＴＰの面積/ＷＥＴの厚み S= 1/R
                roh_hairetu.append(roh)
                break

            if data_sekisan[i2+1] >I_sekisan_w[i]/(area_hairetu[i]) > data_sekisan[i2] :
                #mI_sekisan[i]/area_hairetu[i]がIconvex.py積算電流が当該より高く、当該＋１より低い場合は当該番号の塗膜抵抗をappendしている。



                roh = resi[i2+1]#1/resi[i2+1]/(0.07*0.07)*0.0001#TPの面積m㎡で割り、ＷＥＴ塗膜の厚さ0.1mmを乗じる
                roh = roh*1000#mS/m 
                roh_hairetu.append(roh)
                if i == 0: print(data_sekisan[i2+1], ">" , I_sekisan_w[i]/(area_hairetu[i]), ">" , data_sekisan[i2])
                if i == 0: print("mIsekisan[1]",I_sekisan_w[i], "area_hairetu",area_hairetu[i])
                break

    return roh_hairetu