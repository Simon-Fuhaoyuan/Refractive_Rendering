// Created in 2017-09-29 17:52:30.203157
#declare shape_5 =
difference {

intersection{
cylinder {
 <0, 0, 0>, <0,1.42,0>, 0.64 scale <1,1,0.58> 
}cylinder {
 <0, 0, 0>, <0,1.42,0>, 0.64 scale <0.66,1,1> 
} 
scale <1,1,1>
}

intersection{
cylinder {
 <0, 0, 0>, <0,1.42,0>, 0.64 scale <1,1,0.58> 
}cylinder {
 <0, 0, 0>, <0,1.42,0>, 0.64 scale <0.66,1,1> 
} 
scale <0.91, 1,0.91> translate <0,0.19,0>
}

rotate <0.00, -36.51, 0.00>
}
