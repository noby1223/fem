@@ -0,0 +1,32 @@
// Gmsh project created on Wed Mar 15 21:28:08 2023
SetFactory("OpenCASCADE");
//+
Box(1) = {0, 0, 0, 1, 3, 1};
//+

Box(2) = {0.3, 0.5, 0.3, 0.4, 1, 0.4};
    

Cylinder(3) = {00.45, 2.5, 0.9, 0, 0, -0.8, 0.05, 2*Pi};


//+
Surface Loop(6) = {1, 3, 5, 2, 4, 6};

//+
Surface Loop(7) = {12, 7, 9, 11, 8, 10};


//+g
Physical Surface("body", 37) = {8, 9, 12, 7, 11, 10};
//+
Physical Surface("tank", 38) = {1, 6, 3, 5, 2, 4};
//+

Physical Surface("anode", 39) = {15, 13, 14};


BooleanDifference{ Volume{1}; Delete; }{ Volume{2,3}; Delete;}
//+
//+
Physical Volume("paint", 40) = {1};