import getfem as gf
import postprocess_3d as post_3d
import numpy as np
import pandas_3d as pd3

elements_degree = 1


m = gf.Mesh("import", "gmsh", "/home/noby/fem/fem3d/exact_solution/msh_geo/exact_solution_3d.msh")

#　リージョン　region 7 全体の領域　region 3  wet領域

rp = m.region(7)

reg = m.region(3)[0]
rp2 = np.delete(rp,reg,1)

bd2 = m.region(4)#39
bd3 = m.region(3)#14
bd4 = rp2#5

ANODE = 2
BODY = 3
PAINT = 4

m.set_region(ANODE, bd2)
m.set_region(BODY, bd3)
m.set_region(PAINT, bd4)


I_sekisan = []
I_hairetu_each = []
md = []
cond_wet_mtm = []
I_hai_mtm = []
cvnb_a = m.nbcvs()#全領域の凸
cvnb_p = len(rp[0])#領域paintの凸

# 時間軸にそって複数のファイルを作成するための繰り返し処理はここかやってみるよ

for i in range(5):
    print(str(i) + "ファイル目")

    # 有限要素法と積分法の定義 meshfemはmeshオブジェクトと求めたい次元の物理量

    mf = gf.MeshFem(m, 1)  # 電位を求めたいのでスカラーの１
    mf.set_classical_fem(elements_degree)  # 要素の次数をセットする。1次のラグランジュ
    mim = gf.MeshIm(
        m, elements_degree * 3
    )  # 積分法の次数のセット printするとim_triangle(次数)が凸に紐づけられる

    md.append(gf.Model("real"))
    # 実数と複素数で実数を選択
    conductivity = 0.1
    conduct = "cond"


    # WET塗膜の領域を作成していくよ
    bdw = []
    WET = [] #凸毎のregionの配列　既存のregion番号が40までなので41から順番につけていく。1000くらいまで。
    wi = 0
    conductivity_wet = []
    conduct_wet = []
    md[i].add_fem_variable("V", mf)

    for w in m.region(3)[0]:  # WET塗膜の凸毎にsetregionで領域とconductibityを設定していく
        bdw.append([w, 65535])
        WET.append(50 + wi)
        m.set_region(WET[wi], bdw[wi])

        if i == 0:
            cv_cd = 0.1 #1000μS/cm　がﾒｰﾄﾙ換算で0.1S/ｍかなと

        else:
            if 0.1 / np.linalg.norm(I_sekisan[w])/10 **0.5  > 0.1:
                cv_cd = 0.1

            else:
                cv_cd = 0.1 / np.linalg.norm(I_sekisan[w])/10 **0.5

        conductivity_wet.append(cv_cd)
        conduct_wet.append("cond_wet" + str(wi))
 
        md[i].add_initialized_data(conduct_wet[wi], [conductivity_wet[wi]])
        md[i].add_linear_term(mim, conduct_wet[wi] + "*(Grad_V.Grad_Test_V)", WET[wi])

        wi += 1

    md[i].add_initialized_data("cond", [conductivity])  # 初期化された固定サイズデータをモデルに追加します
    md[i].add_linear_term(
        mim, conduct + "*(Grad_V.Grad_Test_V)", PAINT
    )  # アセンブリ文字列 expr で指定された非線形項を追加します．この意味はsigamaeps*grad_V.Test_Grad_Vってことだな



    md[i].add_initialized_data("DdataV_b", [0])
    md[i].add_Dirichlet_condition_with_multipliers(
        mim, "V", elements_degree - 1, BODY , "DdataV_b"
    )
    md[i].add_initialized_data("DdataV_a", [500])
    md[i].add_Dirichlet_condition_with_multipliers(
        mim, "V", elements_degree - 1, ANODE, "DdataV_a"
    )  # 変数 varname とメッシュ領域 region にDirichlet条件を追加します．

    

    md[i].solve()  # noisyｿﾙﾊﾞ進行状況　res目標残差値　iter最大反復回数

    V = md[i].variable("V")

    mf.export_to_vtk(
        "fem/fem3d/exact_solution/vtk/fem_3d_wet_electric_potential" + str(i) + ".vtk", mf, V, "Electric potential"
    )
    

    I_hairetu = post_3d.postprocess_3d(m, V, mf,conductivity,conductivity_wet)
    

    for y in range(len(I_hairetu)):
        if i == 0:
            I_sekisan.append(I_hairetu[y])
        else:
            I_sekisan[y] += I_hairetu[y]


    pd3.excel_3d_exact(i,m,mf, I_sekisan, I_hairetu,WET)

    cond_wet_m = [0.1]*cvnb_p
    cond_wet_mt = cond_wet_m + conductivity_wet   
    cond_wet_mtm.append(cond_wet_mt)

    I_hai_mtm.append(I_hairetu)



#電導度と電流の積算値をエクセルに出力するう！
pd3.excel_3d_matome_exact(cond_wet_mtm,I_hai_mtm)


# #ここから電流を表示するプロットをpyvistaで書いてみよう
# とりあえず凍結した。電流データがメシュ分ないのでエラーがでてしまった。

# vectors = np.vstack(
#     (

#         # np.sin(sphere.points[:, 0]),
#         # np.cos(sphere.points[:, 1]),
#         # np.cos(sphere.points[:, 2]),
#         [r[0][0] for r in I_hairetu],#リストの内包表記を使用しているよ
#         [r[1][0] for r in I_hairetu]
#     )
# ).T

# # add and scale
# pvvtk["vectors"] = vectors
# pvvtk.set_active_vectors("vectors")

# pvvtk.arrows.plot()
