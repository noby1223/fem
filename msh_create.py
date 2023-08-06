import getfem as gf

m = gf.Mesh("import", "gmsh", "/home/noby/fem/fem3d/msh_geo/t20rev.msh")
m.export_to_vtk( "t20rev_ascii","ascii")

# m = gf.Mesh("import", "gmsh", "/home/noby/fem/fem3d/boxtest.msh")
# gf.Mesh.export_to_vtk(m, "boxtest.vtk")

# test
