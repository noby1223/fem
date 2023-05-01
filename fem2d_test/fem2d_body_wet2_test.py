import getfem as gf
import pyvista as pv
import postprocess_2d as post_2d
import random
import numpy as np

elements_degree = 1


m = gf.Mesh("import", "gmsh", "/home/noby/fem/fem2d/fem2d_2.msh")



bd2 = m.region(32)
bd3 = m.region(31)
bd4 = m.region(35)


ANODE = 2
BODY = 3
PAINT = 4


m.set_region(ANODE, bd2)
m.set_region(BODY, bd3)
m.set_region(PAINT, bd4)

I_sekisan = []


# 有限要素法と積分法の定義 meshfemはmeshオブジェクトと求めたい次元の物理量

mf = gf.MeshFem(m, 1)  # 電位を求めたいのでスカラーの１
mf.set_classical_fem(elements_degree)  # 要素の次数をセットする。1次のラグランジュ
mim = gf.MeshIm(m, elements_degree * 2)  # 積分法の次数のセット printするとim_triangle(次数)が凸に紐づけられる


# 時間軸にそって複数のファイルを作成するための繰り返し処理はここから？


md = gf.Model("real")
# 実数と複素数で実数を選択
conductivity = 1000
conduct = "cond"
# conductivity2 = 100
# conduct2 = "cond2"

# WET塗膜の領域を作成していくよ
bdw = []
WET = []
wi = 0
conductivity_wet = []
conduct_wet = []
md.add_fem_variable("V", mf)


for w in m.region(34)[0]:
    bdw.append([m.region(34)[0][wi], 65535])
    WET.append(40 + wi)
    m.set_region(WET[wi], bdw[wi])

    conductivity_wet.append(random.randint(50, 100))
    conduct_wet.append("cond_wet" + str(wi))

    md.add_initialized_data(conduct_wet[wi], [conductivity_wet[wi]])
    md.add_linear_term(mim, conduct_wet[wi] + "*(Grad_V.Grad_Test_V)", WET[wi])

    wi += 1


md.add_initialized_data("cond", [conductivity])  # 初期化された固定サイズデータをモデルに追加します
md.add_linear_term(
    mim, conduct + "*(Grad_V.Grad_Test_V)", PAINT
)  # アセンブリ文字列 expr で指定された非線形項を追加します．この意味はsigamaeps*grad_V.Test_Grad_Vってことだな

# md.add_linear_term(mim, conduct2 +"*(Grad_V.Grad_Test_V)",WET)
# md.add_initialized_data("cond2", [conductivity2])

md.add_initialized_data("DdataV_b", [0])
md.add_Dirichlet_condition_with_multipliers(
    mim, "V", elements_degree - 1, BODY, "DdataV_b"
)
md.add_initialized_data("DdataV_a", [500])
md.add_Dirichlet_condition_with_multipliers(
    mim, "V", elements_degree - 1, ANODE, "DdataV_a"
)  # 変数 varname とメッシュ領域 region にDirichlet条件を追加します．

print(md.brick_list())


md.solve("max_res", 1e-9, "noisy")  # noisyｿﾙﾊﾞ進行状況　res目標残差値　iter最大反復回数

V = md.variable("V")
print(md.variable("V"))


mf.export_to_vtk("fem_2d_wet_electric_potential.vtk", mf, V, "Electric potential")
# pvvtk = pv.read("fem_2d_wet_electric_potential.vtk")
# pvvtk.plot()


# I_hairetu = post_2d.postprosecc_2d(m, V, mf)

# I_sekisan += I_hairetu

# ここから電流を表示するプロットをpyvistaで書いてみよう
"""とりあえず凍結した。電流データがメシュ分ないのでエラーがでてしまった。

vectors = np.vstack(
    (
        
        # np.sin(sphere.points[:, 0]),
        # np.cos(sphere.points[:, 1]),
        # np.cos(sphere.points[:, 2]),
        [r[0][0] for r in I_hairetu],#リストの内包表記を使用しているよ
        [r[1][0] for r in I_hairetu]
    )
).T

# add and scale
pvvtk["vectors"] = vectors 
pvvtk.set_active_vectors("vectors")

pvvtk.arrows.plot()

"""
