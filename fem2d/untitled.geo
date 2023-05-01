// Gmsh project created on Wed Jan 11 10:53:59 2023
//+

lc = 1;

Point(1) = {0, 0, 0, lc};
//+
Point(2) = {0, 100, 0, lc};
//+
Point(3) = {300, 100, 0, lc};
//+
Point(4) = {300, 0, 0, lc};
//+
Point(5) = {270, 10, 0, lc};
//+
Point(6) = {280, 10, 0, lc};
//+
Point(7) = {280, 90, 0, lc};
//+
Point(8) = {270, 90, 0, lc};
//+
Point(9) = {30, 20, 0, lc};
//+
Point(10) = {30, 45, 0, lc};
//+
Point(11) = {60, 45, 0, lc};
//+
Point(12) = {75, 70, 0, lc};
//+
Point(13) = {125, 70, 0, lc};
//+
Point(14) = {140, 45, 0, lc};
//+
Point(15) = {170, 45, 0, lc};
//+
Point(16) = {170, 20, 0, lc};
//+
Line(1) = {1, 2};
//+
Line(2) = {2, 3};
//+
Line(3) = {3, 4};
//+
Line(4) = {4, 1};
//+
Line(5) = {9, 10};
//+
Line(6) = {10, 11};
//+
Line(7) = {11, 12};
//+
Line(8) = {12, 13};
//+
Line(9) = {13, 14};
//+
Line(10) = {14, 15};
//+
Line(11) = {15, 16};
//+
Line(12) = {16, 9};
//+
Line(13) = {8, 5};
//+
Line(14) = {5, 6};
//+
Line(15) = {6, 7};
//+
Line(16) = {7, 8};
//+
Curve Loop(1) = {1, 2, 3, 4};
//+
Curve Loop(2) = {7, 8, 9, 10, 11, 12, 5, 6};
//+
Curve Loop(3) = {13, 14, 15, 16};
//+
Physical Curve("EDtank", 17) = {1, 2, 3, 4};
//+
Physical Curve("body", 18) = {8, 9, 10, 11, 7, 6, 5, 12};
//+
Physical Curve("anode", 19) = {16, 13, 15, 14};
//+
Plane Surface(1) = {1, 2, 3};
//+
Physical Surface("paint", 20) = {1};
//+
Show "*";
//+
Show "*";
//+
