import os
import pickle #pickleでオブジェクトを保存している いちいち計算すると時間かかるので


def point_awase(m,mf):

    f_path = '/home/noby/fem/fem3d/TPウェット塗膜抵抗測定/m_mf_point/m_mf_awase.bin'#ここにファイルパスを入れる

    if os.path.exists(f_path):

        with open(f_path, 'rb') as p:
            pts_junban = pickle.load(p)

    else:

        #MeshオブジェクトとMeshFemオブジェクトのidがずれているので、（ptsの座標が電位Vの何番目の要素に該当するかわからなくなってしまう。
        #最初にMeshFemの座標を配列にしておく

        #やり方としては、mf．basic_dof_nodeで本来のpt番号と座標を取得しておき、
        #mのWET塗膜の凸IDと紐づいているm.ptsの座標からm.pt番号を紐づける.つまり座標同士でmfとmの番号を紐づける
        #         
        mf_hairetu = []
        for i3 in range(m.nbpts()):#range(m.nbpts())
            mf_hairetu.append(mf.basic_dof_nodes(i3))


        pts_junban = []
        for i4 in range(m.nbpts()):#MESHオブジェクトとMESHFEMオブジェクトのﾎﾟｲﾝﾄを合わせておく
        #ここで合わせておかないと計算が膨大になって時間がかかる。
            pt = m.pts(i4)
            for nbpt in range(m.nbpts()):
  
                if pt[0] == mf_hairetu[nbpt][0] and pt[1] == mf_hairetu[nbpt][1] and pt[2] == mf_hairetu[nbpt][2]:#xyzの座標で合わせていく。pt[0]がx
                    pts_junban.append(nbpt)
                    print('今'+ str(i4) + str(m.pts(nbpt)))
                    break

              

        with open(f_path, 'wb') as p:
            pickle.dump(pts_junban, p)
        



    return pts_junban




        










