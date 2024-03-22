""" Incompressible Navier-Stokes equation solved in an L-shaped domain.

  This program is used to check that python-getfem is working. This is also
  a good example of use of GetFEM.
"""


import numpy as np
import getfem as gf

#3dでやってみるよ

dt = 0.1
T = 3.
nu = 0.01

p_in_str = "3" #のちのち{0}の部分にformatメソッドでｔが入る.ここでは３とした。

#Mesh and MeshRegion

geotrans = "GT_QK(2,2)"

m = gf.Mesh("import", "gmsh", "/home/noby/fem/fem2d/塗料循環2d/msh/2d_EDtank_240108.msh")
m.optimize_structure()

#14　がInで13がout
WALL_RG = 4
P_IN_RG = 14
P_OUT_RG = 13

m.extend_region(WALL_RG, m.region(12))
m.region_subtract(WALL_RG, P_IN_RG) #wallからinoutを引いている
m.region_subtract(WALL_RG, 14) #wallからinoutを引いている


#MeshFem
mfv_ = gf.MeshFem(m, 2)#2は次元数 ここを１から２にするとmfv_.nb_basic_dof()が２倍になる(要はスカラーからベクトルになる)
mfv_.set_classical_fem(2)#凸辺の間に節点がもう一つできる、あと中央にも
kept_dofs = np.setdiff1d(np.arange(mfv_.nb_basic_dof()), #setdiff1dは配列でかぶっているところを消去して、返す。
                         mfv_.basic_dof_on_region(WALL_RG))
#setdiffで全体の自由度数（総節点数×自由度数２？）から壁領域の自由度数を差し引いた配列を作成。
mfv = gf.MeshFem("partial", mfv_, kept_dofs)
# mf の自由度のサブセットのみを保持することで，制限されたMeshFemを構築します．   どゆこと？
#kept_dofsは全体の自由度番号（2次元、2556)から壁の部分を取り除いた自由度番号

mfp_ = gf.MeshFem(m, 1)
mfp_.set_classical_fem(1)
kept_dofs = np.setdiff1d(np.arange(mfp_.nb_basic_dof()),
                         mfp_.basic_dof_on_region(P_IN_RG))
mfp = gf.MeshFem("partial", mfp_, kept_dofs)

#mfvはWALLRGを、mfpはOUTRGを除外している。vは流速で壁側は0で、pは圧力で出口を開放にしているから？

mim = gf.MeshIm(m, 5) # 9 gauss points per quad

md = gf.Model("real")
md.add_fem_variable("v", mfv)
md.add_fem_data("v0", mfv) #MeshFemにリンクされたモデルにデータを追加します
md.add_fem_variable("p", mfp)
md.add_fem_data("p_in", mfp_)
md.add_initialized_data("f", [0,0])#fは外力かなあ
md.add_initialized_data("dt", [dt])
md.add_initialized_data("nu", [nu])#動粘度　粘度/密度　μ/ρ　m2/s

md.add_Dirichlet_condition_with_multipliers(mim, "p", mfp, P_OUT_RG, "p_in")
md.add_nonlinear_term\
(mim, "1/dt*(v-v0).Test_v + (Grad_v0*v0).Test_v + nu*Grad_v:Grad_Test_v - f.Test_v")
md.add_nonlinear_term\
(mim, "Grad_p.Grad_Test_p + 1/dt*Trace(Grad_v)*Test_p")

mmat_v = gf.asm_mass_matrix(mim, mfv) #質量行列のアセンブリ SpMatオブジェクトを返します． なんのことやら 疎行列を英語でsparse matrix という
#mmat_v = gf.asm_generic(mim, 2, "Test2_v.Test_v", -1, "v", 1, mfv, np.zeros(mfv.nbdof()))
#mmat_V vのmassmatrix(質量行列)　2318*2318
IV = md.interval_of_variable("v") #モデルの線形システムの変数 varname の間隔を指定します．わからん

t = 0
step = 0
while t < T+1e-8:#300回ということ
   print("Solving step at t=%f" % t) #fにｔをいれてprintしてんのか
   md.set_variable\
   ("p_in", mfp_.eval(p_in_str, globals(), locals()).flatten("F")) #（lagrangian）MeshFemで式を補間します． とのこと　
   #sinで圧力の方向を徐々に変えている。しかしそれは
   md.set_variable("v0", md.variable("v"))#これを見るにv0は（-Δｔ,つまり前回の時刻の)vかね
   md.solve("noisy", "lsolver", "mumps", "max_res", 1e-8)
   vv = (gf.asm_generic(mim, 1, "(v-dt*Grad_p).Test_v", -1, md))[IV[0]:IV[0]+IV[1]]#‐1は全ての領域を指定
#mmatはΔtの間変わらない、vvだけ変化させている

   md.set_variable("v", gf.linsolve_mumps(mmat_v, vv)) #MUMPSソルバーを使用して， M.U = b を解きます．

   mfv.export_to_vtk("/home/noby/fem/fem2d/塗料循環2d/vtk/results_%i.vtk" % step,
                     mfv, md.variable("v"), "Velocity",
                     mfp, md.variable("p"), "Pressure")
   t += dt
   step += 1