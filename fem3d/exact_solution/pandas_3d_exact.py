import pandas as pd
import os
import numpy as np

name = '/home/noby/fem/fem3d/TPウェット塗膜抵抗測定/csv/each/'
name2 = '/home/noby/fem/fem3d/TPウェット塗膜抵抗測定/csv/matome/'

def excel_3d  (r_p,i,m,mf,I_sekisan,I_hairetu,ws,bd_ws,bd2):
    
    #凸とregionを紐づける
    rp = bd2 #bd2はpaintのm.region()    
    rw = bd_ws#全てのWET領域ののregion凸

    


    cv_rg = []
    for cv in range(m.nbcvs()):

            if cv in rp:
                cv_rg.append([cv,r_p])
            for k in range(len(ws)):
                if cv in rw[0]:
                    cv_rg.append([cv,ws[k]])

    
           

    fp =  name +'cv_pt_rg' + str(i)+'.csv'#cvのpids,region,Iファイルを作成
    if os.path.isfile(fp):
        os.remove(fp)
        f = open(fp, 'w')
        f.write('')

    else:
        
        f = open(fp, 'w')
        f.write('')

    data = []
    for di in range(m.nbcvs()):
        data.append(["cv_no"+str(di),m.pid_from_cvid(di)[0].tolist()
                                ,cv_rg[di][1]
                                ,I_hairetu[di]
                                ,I_sekisan[di]
                                
                                ])


    df =  pd.DataFrame(#こいつは引数が辞書だな

                        data,
                        columns =['no','pt_no', 'region','temp_I','sekisan_I']
                        )
                        
    df.to_csv(fp)



    fp2 = name + "pts_coord" + str(i) + '.csv'#ptのファイル ptno cooridante を作成
    if os.path.isfile(fp2):
        os.remove(fp2)
        f = open(fp2, 'w')
        f.write('')

    else:
        
        f = open(fp2, 'w')
        f.write('')

    data2 = []
    for di2 in range(m.nbpts()):
        data2.append(["pt_no"+str(di2),mf.basic_dof_nodes(di2).tolist()])#ここをm.ptsにすると例のごとく違った番号になる

    df2 =  pd.DataFrame(#こいつは引数が辞書だな

                        data2
                        ,columns=  ['pt_no', 'coordinate']
                        )
                        
    df2.to_csv(fp2)

    



def excel_3d_matome(cond_wet_mtm,I_hai_mtm,V_matome,area_hairetu,I_seki_mtm,bd2,bd_ws,region_w):


    # 1 電導度のまとめ
    fp =  name2 + 'wet_conductivity_matome.csv'#cvのファイルを作成
    if os.path.isfile(fp):
        os.remove(fp)
        f = open(fp, 'w')
        f.write('')

    else:
        
        f = open(fp, 'w')
        f.write('')



    data = cond_wet_mtm
    data = np.insert( data, 0, bd_ws[0], axis = 0)
    data = np.insert( data, 0, region_w, axis = 0)
    df =  pd.DataFrame(#こいつは引数が辞書だな

                        data
                        #,columns=  ['region_no', 'conve_no']
                        ).T

    df.to_csv(fp)


    #2 各凸の電流のまとめ
    fp2 = name2 + 'I_each_conv_matome.csv'#cvのファイルを作成
    if os.path.isfile(fp2):
        os.remove(fp2)
        f2 = open(fp2, 'w')
        f2.write('')

    else:
        
        f2 = open(fp2, 'w')
        f2.write('')

    data2 = I_hai_mtm
    df2 = pd.DataFrame(
           data2 
    ).T
   

    
    df2.to_csv(fp2) 



    #3 電位のまとめ
    fp3 = name2 + 'V_matome.csv'#cvのファイルを作成
    if os.path.isfile(fp3):
        os.remove(fp3)
        f3 = open(fp3, 'w')
        f3.write('')

    else:
        
        f3 = open(fp3, 'w')
        f3.write('')

    data3 = V_matome
    df3 = pd.DataFrame(
           data3 
    ).T
   
    
    df3.to_csv(fp3) 


    #4 面積あたりの積算電流のまとめ
    fp4 = name2 + 'I_sekisan_per_mm2_matome.csv'#cvのファイルを作成

    I_seki_mtm2 = np.delete(I_seki_mtm,slice(0,len(bd2[0])),axis = 1)
    I_np = np.array(I_seki_mtm2) 
    I_area_mtm = I_np[-1][-len(area_hairetu):]/area_hairetu/1000000#area_haiが㎡なのでミリ㎡になおす【1,000,000）で除する。np.arrayでないとそのまま割算できない
    if os.path.isfile(fp4):
        os.remove(fp4)
        f4 = open(fp4, 'w')
        f4.write('')

    else:
        
        f4 = open(fp4, 'w')
        f4.write('')

    data4 = I_area_mtm
    df4 = pd.DataFrame(
           data4 
    ).T
   

    
    df4.to_csv(fp4) 




    #5 電流積算のまとめ
   
    fp5 = name2 + 'I_sekisan_matome.csv'#cvのファイルを作成


    if os.path.isfile(fp5):
        os.remove(fp5)
        f5 = open(fp5, 'w')
        f5.write('')

    else:
        
        f5 = open(fp5, 'w')
        f5.write('')

    data5 = I_seki_mtm2
    data5 = np.insert( data5, 0, bd_ws[0], axis = 0)
    data5 = np.insert( data5, 0, region_w, axis = 0)
    df5 = pd.DataFrame(
           data5 
    ).T
   

    
    df5.to_csv(fp5) 


