#ベクトルの方向によって角度angが変わるかのテストファイル。結果変わった。

import numpy as np
import math
import getfem as gf

# v_x = 1 #v vector d1のｘ
# v_y = 0 
# v_x2 =0
# v_y2 =-1
# #2直線のなす角度θは以下で求められる。　内積d1・d2 = |d1||d2|sinθ 
# d1 = abs(math.sqrt(v_x**2+v_y**2))
# d2 = abs(math.sqrt(v_x2**2+v_y2**2)) #|d2|

# sin = ( v_x2*v_y - v_x*v_y2 ) / (d1*d2)  #ang  angle
# ang = math.degrees(math.asin(sin))

# print(ang)

m = gf.Mesh('import','gmsh','/home/noby/fem/fem2d_2.msh')
print(m)
gf.Mesh.export_to_vtk(m,'fem2d_2_wet.vtk')
# a = m.pid_in_regions(18)
# rr = m.region(18)[0]    
# rs = rr.tolist()

# for r in rs:
#     rm = m.pid_from_cvid(r)
#     rm0 = rm[0]
#     rms = rm0.tolist()
#     ind = rs.index(r)

#     if a[0] in rms and a[1] in rms:
#         face = m.normal_of_face(r,ind)
#         print(face)

