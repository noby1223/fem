import pandas as pd
import numpy as np


#ver2はconductibityをWET塗膜の長さによって補正していく

def wet_conduct(I_sekisan,  bd_ws  , bd2,area_b_hairetu,  area_p_hairetu   ,m  , i_ori):

    I_sekisan_w = np.delete(I_sekisan,slice(0,len(bd2[0])))

    df = pd.read_excel('/home/noby/fem/fem3d/4box/resistance_data/1回目WET電導度計算用20231028_240V_ソフトS120秒_PVC容器＿180s_攪拌なし__温度26度＿テープYT_WET電導度最初のほう塗料.xlsx')
    data_sekisan = df['積算電流A/mm']#70mm*70mm 単位はmA/㎟
    data_sekisan[0] = 0#何も入れないとnanなので
    resi = df['電導度換算（厚さ0.1ミリ）']
    roh_hairetu = []
    

    
    for i in range(len(I_sekisan_w)):

        area_b_hairetu[i] = area_b_hairetu[i]*1000000#m㎡に換算
        area_p_hairetu[i] = area_p_hairetu[i]*1000000#m㎡に換算
        

        #ここで電導度を補正するための計算をしておく。
        #body側の面積＋paint側の面積÷２×0.1㎜　：　wet凸の体積　の比率をconductibityのそれぞれ乗じる
        propotion = m.convex_area(bd_ws[0][i])  /  ((area_b_hairetu[i] + area_p_hairetu[i])/2 *0.1) 
        propotion = propotion[0]
        
        for i2 in range(len(data_sekisan)):

            

            if I_sekisan_w[i]/(area_b_hairetu[i]) <= data_sekisan[0] :#一番低いときは塗料と同じ電導度にする
                roh = 100*propotion#mS/m
                roh_hairetu.append(roh)
                break


            if i2 == len(data_sekisan)-1:#i2がラストになってしまうと＋１でエラーが出てしまうため、ここで条件分岐
                roh = resi[i2-1]*1000*propotion #1/resi[i2-1]/(0.07*0.07)*0.0001#ρ　＝　S＊ＴＰの面積/ＷＥＴの厚み S= 1/R
                roh_hairetu.append(roh)
                break

            if data_sekisan[i2+1] >I_sekisan_w[i]/(area_b_hairetu[i]) > data_sekisan[i2] :
                #mI_sekisan[i]/area_hairetu[i]がIconvex.py積算電流が当該より高く、当該＋１より低い場合は当該番号の塗膜抵抗をappendしている。



                roh = resi[i2+1]
                roh = roh*1000*propotion#mS/m 
                roh_hairetu.append(roh)
                if i == 0: print(data_sekisan[i2+1], ">" , I_sekisan_w[i]/(area_b_hairetu[i]), ">" , data_sekisan[i2])
                if i == 0: print("mIsekisan[1]",I_sekisan_w[i], "area_hairetu",area_b_hairetu[i])
                break

    return roh_hairetu