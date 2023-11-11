import getfem as gf
import dennryuu_keisan_kakunin_231005 as post_3d
import numpy as np
import pandas_3d as pd3
import wet_conductibity as w_cond
import msh_mf_point as msh_mf
import add_region as add_re


# from memory_profiler import profile　　　　　#メモリ診断用
# @profile()
# def main_dayo():



elements_degree = 1


m = gf.Mesh("import", "gmsh", "/home/noby/fem/fem3d/4box/msh_geo/FEM__4枚BOX2Φ穴なしregionmainasu_wet.msh")




bd1 = m.region(90)#電極のregion
bd2 = m.region(12)#paintのregionを追加
bd_ws,bd_wsf1,bd_wsf2,ws,reg1,reg2 = add_re.addregion(m)
#bd_wsはウェットの凸
#bd_wsf1　wetの面region(0v側)を追加していくよ
#bd_wsf2　wetの面region(0vじゃない側)を追加していくよ
#wsはWET凸領域(111 ~ 117 )
#reg1は塗料側、reg2はボディ側の凸、面は共有



ANODE = 1
PAINT = 2
BODY_SURFACE = 3 #ここでTPの表裏、計7面を分けてregionを設定し、Dhiriclet_condition_multiでやろうとしたら謎のエラーがでた。（０Vが1000Vになったりして）わかるのに結構時間かかってしまった。
WET_SURFACE = 4

m.set_region(ANODE, bd1)
m.set_region(PAINT, bd2)
m.set_region(BODY_SURFACE, bd_wsf1)
m.set_region(WET_SURFACE, bd_wsf2)




md = []




# 時間軸にそって複数のファイルを作成するための繰り返し処理はここかやってみるよ

for i in range(1):
    print(str(i) + "ファイル目")

    # 有限要素法と積分法の定義 meshfemはmeshオブジェクトと求めたい次元の物理量

    mf = gf.MeshFem(m, 1)  # 電位を求めたいのでスカラーの１
    mf.set_classical_fem(elements_degree)  # 要素の次数をセットする。1次のラグランジュ
    mim = gf.MeshIm(
        m, elements_degree * 3
    )  # 積分法の次数のセット printするとim_triangle(次数)が凸に紐づけられる

    md.append(gf.Model("real"))
    # 実数と複素数で実数を選択
    conductivity = 100#ms/m
    conduct = "cond"


    # WET塗膜の領域を作成していくよ
    WET = [] #凸毎のregionの配列　既存のregion番号が40までなので41から順番につけていく。1000くらいまで。
    wi = 0
    conductivity_wet = []
    conduct_wet = []
    md[i].add_fem_variable("V", mf)


    
       
    conductivity_wet = [conductivity]*len(bd_ws[0]) #1000μS/cm　がﾒｰﾄﾙ換算で100mS/ｍかなと


        

    for k in bd_ws[0]:  # WET塗膜の凸毎にsetregionで領域とconductibityを設定していく
        
        WET.append(120 + wi)
        m.set_region(WET[wi], [bd_ws[0][wi],bd_ws[1][wi]])


        conduct_wet.append("cond_wet" + str(wi))

        md[i].add_initialized_data(conduct_wet[wi], [conductivity_wet[wi]])
        md[i].add_linear_term(mim, conduct_wet[wi] + "*(Grad_V.Grad_Test_V)", WET[wi])

        wi += 1

    md[i].add_initialized_data("cond", [conductivity])  # 初期化された固定サイズデータをモデルに追加します
    md[i].add_linear_term(
        mim, conduct + "*(Grad_V.Grad_Test_V)", PAINT
    )  # アセンブリ文字列 expr で指定された非線形項を追加します．この意味はsigamaeps*grad_V.Test_Grad_Vってことだな


    md[i].add_initialized_data("DdataV_b", [0])
   
    md[i].add_Dirichlet_condition_with_multipliers(
            mim, "V", elements_degree - 1, BODY_SURFACE, "DdataV_b"
        )
    md[i].add_initialized_data("DdataV_a", [150])
    md[i].add_Dirichlet_condition_with_multipliers(
        mim, "V", elements_degree - 1, ANODE, "DdataV_a"
    )  # 変数 varname とメッシュ領域 region にDirichlet条件を追加します．



    md[i].solve()  

    V = md[i].variable("V")
    mf.export_to_vtk(
        "fem/fem3d/4box/vtk/fem_3d_wet_electric_potential_4box_ver2_" + str(i) +'.vtk' , "ascii", V, "Electric potential"
    )




   