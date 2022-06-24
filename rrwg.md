% RRWG(1)
% Adriano J. Holanda developed the program. Rafael A. Rosales proposed the idea and helped in the simulation design
% 2022-06-24 rrwg man page

# NAME

rrwg - simulate vertex-reinforced random walks on graphs

# SYNOPSIS

rrwg [Options] 

# DESCRIPTION

*rrwg* simulates the vertex-reinforced random walks on graphs

# COMMAND-LINE OPTIONS 
-a VALUE
: Value of alpha to be used in the calculations.

-d VALUE
: number of vertices

-f NAME
: Possible values are exp or pow.  The function used to
calculate the repelling index, values may be exp that stands for
exponential and pow that is power abbreviature, the following
equations are used to represent each category:

exponential
: f(x) =  exp(-x*alpha)

power
: f(x) =  x*(m-x)^alpha

where m is the number of walks and x is the normalized number of visits.

-m VALUE
: number of walks

-n VALUE
: number maximum of time steps to perform, it is the time limit when the simulations stops


