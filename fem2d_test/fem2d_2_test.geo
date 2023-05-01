// Gmsh project created on Thu Feb 16 13:56:42 2023
SetFactory("OpenCASCADE");


lc = 30;
ws =30;


Point(1) = {0, 0, 0, lc};
//+
Point(2) = {0, 100, 0, lc};
//+
Point(3) = {300, 100, 0, lc};
//+
Point(4) = {300, 0, 0, lc};
//+


Point(5) = {1, 0, 0, lc};
//+
Point(6) = {1, 100, 0, lc};
//+




Line(1) = {1, 2};
//+
Line(2) = {2, 6};
//+
Line(3) = {6, 5};
//+
Line(4) = {5, 1};
//+
Line(5) = {5, 4};
//+
Line(6) = {4, 3};
//+
Line(7) = {3, 6};
//+




Curve Loop(1) = {1, 2, 3, 4};
//+
Curve Loop(2) = {3,5, 6,7  };
//気づくのに大変時間がかかったが・・・ｶｰﾌﾞﾙｰﾌﾟは小さい番号順ではないといけない、lineの向きも繋がっていないといけない模様。。。


//+

Physical Curve("paint", 30) = {3, 5, 6, 7};
//+
Physical Curve("body", 31) = {1};
//+
Physical Curve("anode", 32) = {6};
//+
Physical Curve("wet", 33) = {1,2,3,4};
//+



//+
Plane Surface(1) = {1};
//+
Plane Surface(2) = {2};
//+
Physical Surface("wet", 34) = {1};
//+
Physical Surface("paint", 35) = {2};
//+

Transfinite Curve {1,3} = 10 Using Progression 1;
//line1,3で10個に分割する。ここでてこずった
//Transfinite Surface {2};
Recombine Surface{1};


Show "*";
//+
Show "*";
//+
//+