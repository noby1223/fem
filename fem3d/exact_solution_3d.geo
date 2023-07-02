// Gmsh project created on Fri Jun 30 15:25:36 2023
SetFactory("OpenCASCADE");
//+
Box(1) = {0, 0, 0, 1, 0.5, 0.5};

//+
Physical Surface("tank", 30) = {1, 6, 3, 5, 4};









Transfinite Surface{1:6} ;
Recombine Surface{1:6};
Transfinite Volume{1}; 
//+

Physical Volume("paint", 3) = 1;



Physical Surface("body", 32) = {1};





Physical Surface("anode", 31) = {2};