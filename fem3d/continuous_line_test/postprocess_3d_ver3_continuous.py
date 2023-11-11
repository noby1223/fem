import numpy as np
import I_convex as I_conv


#ver3はWETの凸で電流値を計算している

#WET領域だと狭すぎて、誤差の影響が大きすぎる？その手前の凸で電流値を計算する。2023/7/25
#しかし凸面の面積はとりあえずWET０V側で計算しよう。


def postprocess_3d  (m,V,conductivity, bd_wsf1,pts_junban,conductivity_wet,i):


    #bd_wsf1　wetの面region(0v側)を追加していくよ
    
    wetregion = bd_wsf1
    area_hairetu = [0] * len(bd_wsf1[0])



    #wet塗膜の凸の数だけ繰り返し処理を書く
    I_hairetu = [0] * len(bd_wsf1[0])
     




    #次にWET塗膜の領域
    cv_li_w = wetregion[0].tolist()
    for  ci in range(len(cv_li_w)):
        c_w = cv_li_w[ci]#ciiはボディ側cii2は塗料側の凸


        pids = m.pid_in_cvids(c_w)




        convex_hairetu = []
        for p in pids:
            convex_hairetu.append([1, m.pts(p)[0][0], m.pts(p)[1][0],m.pts(p)[2][0]])

        gyakugr = np.linalg.pinv(convex_hairetu)
        gyakugyou = np.delete(gyakugr,0,axis = 0)


        #電位の配列を作成
        V_vector = []
        for pid in pids:
            V_vector.append(V[pts_junban[pid]])

        V_vector_ar = np.array(V_vector)
        V_vector_T = V_vector_ar.reshape(-1, 1)#Tでベクトルを転置している


        I_v = gyakugyou@V_vector_T


        #indexで凸の面番号fidを取得している。
        fid = wetregion[1][ci] 
        f_v = m.normal_of_face(c_w,fid)#continuous lineだからciiからc_wにしたよ
        f_pids = m.pid_in_faces([c_w,fid])



        I_convex =    I_conv.I_convex_norm_3d(I_v,f_v,f_pids,m)
        bibun_tanni = 1000#V/mmからV/mに換算
        I_hairetu[ci] += I_convex[0]*bibun_tanni*conductivity_wet[ci]/1000 #ここで乗じるのはconductivity_wet[ci] mS/cmではなくS/cmでいい.ﾐﾘSをSに換算するので1000で除する
        area_hairetu[ci] += I_convex[1]

        
        if ci == 0: print("１凸の電位", V_vector, "座標",convex_hairetu )
        #print(str(cvi) + '電流',)
      


    
    return [I_hairetu,area_hairetu]
