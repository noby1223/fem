import getfem as gf
import numpy as np

m = gf.Mesh("import", "gmsh", "/home/noby/fem/fem3d/msh_geo/fem3d_wahr_wet.msh")

pr = m.pid_in_regions(15)
i= 0
for p in pr:
    pp = np.squeeze(m.pts(p)).tolist()
    print("Point(" + str(i)  + ") = " + "{" + str(pp[0]) + "," + str(pp[1]) + "," + str(pp[2]) + " }" + ";\n")
    i += 1

# m = gf.Mesh("import", "gmsh", "/home/noby/fem/fem3d/boxtest.msh")
# gf.Mesh.export_to_vtk(m, "boxtest.vtk")

# test
