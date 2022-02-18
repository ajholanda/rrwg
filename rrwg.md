% RRWG(1)
% Adriano J. Holanda developed the program. Rafael Rosales proposed the idea and helped in the simulation design
% 2022-02-18 v0.1.0 rrwg man page

# NAME

rrwg - simulate repelling random walks on graphs

# SYNOPSIS

rrwg [--nolog|--quiet] filename.net

# DESCRIPTION

*rrwg* simulates the the repelling random walks on graphs using
"filename.net" as input in a simplified Pajek-like format. After
 the walks are completed, "filename.dat" is generated with the
 walkers' path in terms of vertices. A R file called "filename.R"
 is also created with commands to plot the data.

# COMMAND-LINE OPTIONS
--alpha VALUE 
: value of alpha to be used in the calculations.

--function exp|pow
: The function used to calculate the repelling index, 
  values may be "exp" that stands for exponential and
  "pow" that is power abbreviature, the following 
  equations are used to represent each category:

exp
: f(x) =  exp(-x*alpha)

power
: f(x) =  x*(n-x)^alpha

where n is the number of vertices.

--nwalks VALUE
: number maximum of steps to perform, it is the time limit when the simulations stops

--nolog
: don't write the log file with detail of the walks.

--quiet
: suppress any message from the program.

# EXAMPLES OF INPUT FILE CONTENT

````
# BEGIN OF FILE "complete.net"
# Comments comes after #
# Two walkers' repelling random walks on the 3-complete graph.
1,2	0	1
0,2	2	*3
0,1	*4	5
# END OF FILE

In the content of input file presented above, the rows 
represent the vertices, the first column the adjacency 
list and the rest the number of times each walker 
identified by column index minus one visited the 
vertices before beginning the walks. The asterisk 
indicates where the walker starts the travelling. 
In the example, the walker 0 starts at vertex 2 and 
the walker 2 at vertex 3.
