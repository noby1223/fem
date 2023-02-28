import getfem as gf
import numpy as np
from IPython import embed
import pyvista as pv

elements_degree = 1
conduct = 1000
conduct2 = 100

m = gf.Mesh('import','gmsh','/home/noby/fem/fem2d_2.msh')


# 有限要素法と積分法の定義 meshfemはmeshオブジェクトと求めたい次元の物理量

mf = gf.MeshFem(m, 1)#電位を求めたいのでスカラーの１

bd1 = m.region(30)
bd2 = m.region(32)
bd3 = m.region(31)
TANK = 1;
ANODE= 2; 
BODY= 3;
m.set_region( TANK, bd1)
m.set_region( ANODE, bd2)
m.set_region( BODY,  bd3)

mf.set_classical_fem(elements_degree)#要素の次数をセットする。1次のラグランジュ

mim = gf.MeshIm(m, elements_degree*2)#積分法の次数のセット printするとim_triangle(次数)が凸に紐づけられる



md=gf.Model('real'); #実数と複素数で実数を選択
conductivity = "cond"
md.add_fem_variable('V', mf)
md.add_initialized_data('cond', [conduct])#初期化された固定サイズデータをモデルに追加します
md.add_linear_term(mim, conductivity+'*(Grad_V.Grad_Test_V)')#アセンブリ文字列 expr で指定された非線形項を追加します．この意味はsigamaeps*grad_V.Test_Grad_Vってことだな 
md.add_initialized_data('DdataV_b', [0])
md.add_Dirichlet_condition_with_multipliers(mim, 'V', elements_degree-1, BODY, 'DdataV_b')
md.add_initialized_data('DdataV_a', [500])
md.add_Dirichlet_condition_with_multipliers(mim, 'V', elements_degree-1, ANODE, 'DdataV_a')#変数 varname とメッシュ領域 region にDirichlet条件を追加します．

print(md.brick_list())

print(md.nbdof())
print(md.tangent_matrix())#グローバルマトリクス表示
print(md.rhs())
print(md.variable_list())

print(md.display())



md.solve('max_res', 1E-9, 'noisy')#noisyｿﾙﾊﾞ進行状況　res目標残差値　iter最大反復回数

V = md.variable('V')
print(md.variable('V'))


mf.export_to_vtk('fem_2d_electric_potential.vtk', mf, V, 'Electric potential')
