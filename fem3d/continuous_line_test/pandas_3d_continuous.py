import pandas as pd
import os
import numpy as np

name = '/home/noby/fem/fem3d/continuous_line_test/csv/exel'

def excel_3d  (i,m,mf,I_sekisan,I_hairetu,ws):
    #ws はWETのregionの配列(phisical group)
    #凸とregionを紐づける
    rw = []#WETのregion
    i = 0
    for w in ws:
        rw.append(m.region(w))

    cv_rg = []
    for cv in range(m.nbcvs()):
            
            for i in range(len(ws)):
                if cv in rw[i]:
                    cv_rg.append([cv,ws[i]])

    
           
    #凸とconductivityを紐づける

    fp =  name +str(i)+'.csv'#cvのファイルを作成
    if os.path.isfile(fp):
        os.remove(fp)
        f = open(fp, 'w')
        f.write('')

    else:
        
        f = open(fp, 'w')
        f.write('')

    data = []
    for di in range(len(cv_rg)):
        data.append(["cv_no"+str(di),m.pid_from_cvid(di)[0].tolist()
                                ,cv_rg[di][1]
                                ,I_hairetu[di]
                                ,I_sekisan[di]
                                
                                ])


    df =  pd.DataFrame(#こいつは引数が辞書だな

                        data,
                        columns =['no','pt_no', 'region','temp_I','integ_I']
                        )
                        
    df.to_csv(fp)



    fp2 = name + "pts" + str(i) + '.csv'#ptを基準にファイルを作成
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

    
def excel_3d_matome(cond_wet_mtm,I_hai_mtm,V_matome,area_hairetu,I_seki_mtm,bd2):
    fp =  name + 'cond_matome.csv'#cvのファイルを作成
    if os.path.isfile(fp):
        os.remove(fp)
        f = open(fp, 'w')
        f.write('')

    else:
        
        f = open(fp, 'w')
        f.write('')



    data = cond_wet_mtm
    df =  pd.DataFrame(#こいつは引数が辞書だな

                        data
                        
                        ).T

    df.to_csv(fp)


    #電流のまとめ
    fp2 = name + 'I_matome.csv'#cvのファイルを作成
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



    #電位のまとめ
    fp3 = name + 'V_matome.csv'#cvのファイルを作成
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

        #面積あたりの電流のまとめ
    fp4 = name + 'I_area_matome.csv'#cvのファイルを作成

    I_np = np.array(I_hai_mtm) 
    I_area_mtm = I_np[0][-len(area_hairetu):]/area_hairetu*1000#数字が小さくなりすぎるのでμAにしようか（1000を乗じて）
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



        #電流積算のまとめ
    I_seki_mtm2 = np.delete(I_seki_mtm,slice(0,len(bd2[0])),axis = 1)
    fp5 = name + 'I_sekisan_aa.csv'#cvのファイルを作成


    if os.path.isfile(fp5):
        os.remove(fp5)
        f5 = open(fp5, 'w')
        f5.write('')

    else:
        
        f5 = open(fp5, 'w')
        f5.write('')

    data5 = I_seki_mtm2
    df5 = pd.DataFrame(
           data5 
    ).T
   

    
    df5.to_csv(fp5) 


