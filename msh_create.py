import getfem as gf

m = gf.Mesh("import", "gmsh", "/home/noby/fem/fem2d_test/fem2d_2_test.msh")
gf.Mesh.export_to_vtk(m, "fem2d_test.vtk")


# test
