import getfem as gf

m = gf.Mesh('import','gmsh','/home/noby/fem/untitled_copycopy.msh')
gf.Mesh.export_to_vtk(m,'untitled_copy.vtk')


#test