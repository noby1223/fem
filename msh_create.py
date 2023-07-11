import getfem as gf

m = gf.Mesh("import", "gmsh", "/home/noby/fem/fem3d/msh_geo/t20rev.msh")
gf.Mesh.export_to_vtk(m, "t20rev.vtk")

# m = gf.Mesh("import", "gmsh", "/home/noby/fem/fem3d/boxtest.msh")
# gf.Mesh.export_to_vtk(m, "boxtest.vtk")

# test
