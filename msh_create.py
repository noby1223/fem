import getfem as gf

m = gf.Mesh("import", "gmsh", "/home/noby/fem/fem3d/msh_geo/fem3d_wahr_wet.msh")
gf.Mesh.export_to_vtk(m, "fem3d_wahr_wet.vtk")

# m = gf.Mesh("import", "gmsh", "/home/noby/fem/fem3d/boxtest.msh")
# gf.Mesh.export_to_vtk(m, "boxtest.vtk")

# test
