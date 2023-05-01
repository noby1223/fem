import fem_2d_wetpts_create


c = fem_2d_wetpts_create.wetpts()

la = 17  # 最後の点番号＋1
lc = 10
for i in range(len(c)):
    c[i][0] = round(c[i][0], 3)
    c[i][1] = round(c[i][1], 3)

    print(
        f"Point(", i + la, ") = {", c[i][0], ",", c[i][1], ", 0, lc};"
    )  # fで文字列を出力しているよ　｛｝で囲むと変数の表示ができる。

    print("//+")


for i in range(len(c)):
    if i == len(c) - 1:
        print(f"Line(", i + la, ") = {", i + la, ",", la, "};")
        print("//+")

    else:
        print(f"Line(", i + la, ") = {", i + la, ",", i + la + 1, "};")
        print("//+")


print("Curve Loop(4) = {17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29};")
print("//+")


print(
    'Physical Curve("wet", 21) = {17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29};'
)
print("//+")


print("Plane Surface(1) = {1, 2, 3, 21};")
# Plane Surface(1) = {1, 2, 3};
print("//+")
