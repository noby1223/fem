// Gmsh project created on Fri Jun 09 11:10:46 2023
SetFactory("OpenCASCADE");

Point(1) = {0.3, 1.5, 0.7, 1.0};//pc
//+
Point(2) = {0.5, 1.5, 0.7,1.0};
//+
Point(3) = {0.3, 1.25, 0.7,1.0};
//+
Point(4) = {0.3, 1.5, 0.5, 1.0};


Point(5) = {0.29, 1.51, 0.71, 1.0};
//Point(6) = {0.3, 1.5, 0.5, 1.0};


//+
Line(1) = {1, 2};
//+
Line(2) = {1, 3};
//+
Line(3) = {1, 4};
//+
Line(4) = {1, 5};