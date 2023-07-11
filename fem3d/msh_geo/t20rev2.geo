// -----------------------------------------------------------------------------
//
//  Gmsh GEO tutorial 20
//
//  STEP import and manipulation, geometry partitioning
//
// -----------------------------------------------------------------------------

// The OpenCASCADE geometry kernel allows to import STEP files and to modify
// them. In this tutorial we will load a STEP geometry and partition it into
// slices.

SetFactory("OpenCASCADE");

// Load a STEP file (using `ShapeFromFile' instead of `Merge' allows to directly
// retrieve the tags of the highest dimensional imported entities):
v() = ShapeFromFile("t20_data.step");


Physical Surface("stuff", 39) = {10:30};


Box(2) = {-70, 100, -150, 130, 130, 200};


Cylinder(3) = {20, 180, -100, -60, 0, 0, 3, 2*Pi};


Physical Surface("anode", 40) = {7:9};



BooleanDifference(4) = { Volume{2}; Delete; }{ Volume{1,3}; Delete;};


Physical Volume("paint", 5) = {4};

//Recombine Surface{1:6};//,10:30

//Transfinite Curve {1,  2,  3, 4, 5,6,  7, 8, 9,10,11,12} = 10 ;
//Transfinite Surface{1:6};
