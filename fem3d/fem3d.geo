// Gmsh project created on Wed Mar 15 21:28:08 2023
SetFactory("OpenCASCADE");
//+

Box(1) = {0, 0, 0, 1, 3, 1};
//+
Box(2) = {0.3, 0.5, 0.3, 0.4, 1, 0.4};
//+

Cylinder(3) = {00.45, 2.5, 0.9, 0, 0, -0.8, 0.05, 2*Pi};


//+
Physical Surface("tank", 37) = {1, 6, 3, 5, 2, 4};
//+
Physical Surface("wet", 38) = {8, 9, 12, 7, 11, 10};
//+

Physical Surface("anode", 39) = {15, 13, 14};



BooleanDifference(4) = { Volume{1}; Delete; }{ Volume{2,3}; Delete;}
//+

//+
Physical Volume("paint", 40) = {1};



Box(5) = {0.28, 0.48, 0.28, 0.44, 1.04 , 0.44};
//+
Box(6) = {0.3, 0.5, 0.3, 0.4, 1, 0.4};
//+




BooleanDifference(7) = { Volume{5}; Delete; }{ Volume{6}; Delete;};

Physical Surface("body", 40) = {16,17,18,19,20,21};

Physical Volume("wet") = 3 ;


v() = BooleanFragments{ Volume{4}; Delete; }{ Volume{7}; Delete; };

Physical Volume(9) = v(#v()-1);

Physical Volume("paint") = 10 ;

//Transfinite Curve {1,  2,  3, 4, 5,6,  7, 8, 9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24 } = 3 ;
// Using Progression 1;

Transfinite Surface{1:21};
Recombine Surface{1:6, 7:12,  16:22};//13:15,


//Mesh.Hexahedra{Volume{8}};
//Recombine Volume{8};

lcar1 = 1.2;
lcar3 = 0.5;


//Mesh.MeshSizeMin = 30;

//MeshSize{ PointsOf{ Surface{13,14,15}; } } = lcar3;

