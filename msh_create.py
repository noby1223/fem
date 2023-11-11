import getfem as gf

for i in range(10):
    m = gf.Mesh("import", "gmsh", '/home/noby/fem/fem3d/continuous_line_test/msh_geo/paint_wet_mesh/paint_wet_done_' + str(i) + '.msh')
    m.export_to_vtk( "/home/noby/fem/fem3d/continuous_line_test/vtk/paint_vtk/test_paint_" + str(i) + ".vtk","ascii")

# m = gf.Mesh("import", "gmsh", "/home/noby/fem/fem3d/boxtest.msh")
# gf.Mesh.export_to_vtk(m, "boxtest.vtk")

# test
