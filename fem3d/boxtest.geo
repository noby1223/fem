// Gmsh project created on Mon May 22 13:55:49 2023
SetFactory("OpenCASCADE");
//+
Box(1) = {0, 0, 0, 1, 1, 1};
//+
Box(2) = {0.25, 0.25, 0.25, 0.5, 0.5, 0.5};
//+
BooleanDifference(3) = { Volume{1}; Delete; }{ Volume{2}; Delete;};
//+


Physical Volume("wet",4) = 3 ;


Transfinite Curve {1:12} = 3;

Transfinite Surface{1:12};