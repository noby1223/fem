# 初期化
import getfem as gf
import numpy as np
import pyvista as pv

# モデルのパラメータ
epsilon = 1.0
E = 21e6
nu = 0.3
clambda = E * nu / ((1 + nu) * (1 - 2 * nu))
cmu = E / (2 * (1 + nu))
clambdastar = 2 * clambda * cmu / (clambda + 2 * cmu)
F = 100e2
kappa = 4.0
D = 10
air_temp = 20
alpha_th = 16.6e-6
T0 = 20
rho_0 = 1.754e-8
alpha = 0.0039

h = 2
elements_degree = 2

# メッシュ生成
mo1 = gf.MesherObject("rectangle", [0.0, 0.0], [100.0, 25.0])
mo2 = gf.MesherObject("ball", [25.0, 12.5], 8.0)
mo3 = gf.MesherObject("ball", [50.0, 12.5], 8.0)
mo4 = gf.MesherObject("ball", [75.0, 12.5], 8.0)
mo5 = gf.MesherObject("union", mo2, mo3, mo4)
mo = gf.MesherObject("set minus", mo1, mo5)

mesh = gf.Mesh("generate", mo, h, 2)


# 境界の選択

fb1 = mesh.outer_faces_in_box([1.0, 1.0], [99.0, 24.0])
fb2 = mesh.outer_faces_with_direction([1.0, 0.0], 0.01)
fb3 = mesh.outer_faces_with_direction([-1.0, 0.0], 0.01)
fb4 = mesh.outer_faces_with_direction([0.0, 1.0], 0.01)
fb5 = mesh.outer_faces_with_direction([0.0, -1.0], 0.01)

RIGHT_BOUND = 1
LEFT_BOUND = 2
TOP_BOUND = 3
BOTTOM_BOUND = 4
HOLE_BOUND = 5

mesh.set_region(RIGHT_BOUND, fb2)
mesh.set_region(LEFT_BOUND, fb3)
mesh.set_region(TOP_BOUND, fb4)
mesh.set_region(BOTTOM_BOUND, fb5)
mesh.set_region(HOLE_BOUND, fb1)
mesh.region_subtract(RIGHT_BOUND, HOLE_BOUND)
mesh.region_subtract(LEFT_BOUND, HOLE_BOUND)
mesh.region_subtract(TOP_BOUND, HOLE_BOUND)
mesh.region_subtract(BOTTOM_BOUND, HOLE_BOUND)


# メッシュの描画
mesh.export_to_vtk("mesh.vtk")
# You can view the mesh for instance with
# mayavi2 -d mesh.vtk -f ExtractEdges -m Surface


# 有限要素法と積分法の定義

mfu = gf.MeshFem(mesh, 2)
mfu.set_classical_fem(elements_degree)
mft = gf.MeshFem(mesh, 1)
mft.set_classical_fem(elements_degree)
mfvm = gf.MeshFem(mesh, 1)
mfvm.set_classical_discontinuous_fem(elements_degree)
mim = gf.MeshIm(mesh, elements_degree * 2)


# モデルの定義

md = gf.Model("real")
md.add_fem_variable("u", mfu)
md.add_fem_variable("theta", mft)
md.add_fem_variable("V", mft)


# 弾性膜変形問題
md.add_initialized_data("cmu", [cmu])
md.add_initialized_data("clambdastar", [clambdastar])
md.add_initialized_data("T0", [T0])
md.add_isotropic_linearized_elasticity_brick(mim, "u", "clambdastar", "cmu")

md.add_Dirichlet_condition_with_multipliers(mim, "u", elements_degree - 1, LEFT_BOUND)
md.add_initialized_data("Fdata", [F * epsilon, 0])
md.add_source_term_brick(mim, "u", "Fdata", RIGHT_BOUND)

md.add_initialized_data("beta", [alpha_th * E / (1 - 2 * nu)])
md.add_linear_term(mim, "beta*(T0-theta)*Div_Test_u")


# 電位問題
sigmaeps = "(eps/(rho_0*(1+alpha*(theta-T0))))"
md.add_initialized_data("eps", [epsilon])
md.add_initialized_data("rho_0", [rho_0])
md.add_initialized_data("alpha", [alpha])
md.add_nonlinear_term(mim, sigmaeps + "*(Grad_V.Grad_Test_V)")
md.add_Dirichlet_condition_with_multipliers(mim, "V", elements_degree - 1, RIGHT_BOUND)
md.add_initialized_data("DdataV", [0.1])
md.add_Dirichlet_condition_with_multipliers(
    mim, "V", elements_degree - 1, LEFT_BOUND, "DdataV"
)


# 熱問題
md.add_initialized_data("kaeps", [kappa * epsilon])
md.add_generic_elliptic_brick(mim, "theta", "kaeps")
md.add_initialized_data("D2", [D * 2])
md.add_initialized_data("D2airt", [air_temp * D * 2])
md.add_mass_brick(mim, "theta", "D2")
md.add_source_term_brick(mim, "theta", "D2airt")

md.add_nonlinear_term(mim, "-" + sigmaeps + "*Norm_sqr(Grad_V)*Test_theta")


# モデルの求解
md.solve("max_res", 1e-9, "max_iter", 100, "noisy")


# 解のエクスポート/可視化
U = md.variable("u")
V = md.variable("V")
THETA = md.variable("theta")
VM = md.compute_isotropic_linearized_Von_Mises_or_Tresca(
    "u", "clambdastar", "cmu", mfvm
)
CO = np.reshape(
    md.interpolation("-" + sigmaeps + "*Grad_V", mfvm), (2, mfvm.nbdof()), "F"
)

mfvm.export_to_vtk(
    "displacement_with_von_mises.vtk",
    mfvm,
    VM,
    "Von Mises Stresses",
    mfu,
    U,
    "Displacements",
)
print("You can view solutions with for instance:")
print("mayavi2 -d displacement_with_von_mises.vtk -f WarpVector -m Surface")
mft.export_to_vtk("temperature.vtk", mft, THETA, "Temperature")
print("mayavi2 -d temperature.vtk -f WarpScalar -m Surface")
mft.export_to_vtk("electric_potential.vtk", mft, V, "Electric potential")
print("mayavi2 -d electric_potential.vtk -f WarpScalar -m Surface")


mesh2 = pv.read("electric_potential.vtk")
mesh2.plot()
