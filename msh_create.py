import getfem as gf

# m = gf.Mesh("import", "gmsh", "/home/noby/fem/fem3d/fem3d.msh")
# gf.Mesh.export_to_vtk(m, "fem3d.vtk")

m = gf.Mesh("import", "gmsh", "/home/noby/fem/fem3d/boxtest.msh")
gf.Mesh.export_to_vtk(m, "boxtest.vtk")

# test
