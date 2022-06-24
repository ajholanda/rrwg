# Random Repelling Walks on Graphs

 This program simulates the vertex-reinforced random walks on
arbitrary connected graphs. In this model, each walk has higher
probability to visit the vertices which have been less visited by the
other walks. Jun (2014) proved that two walks (particles) have small
joint support if the repulsion is strong enough in a complete graph
[Jun Chen, "Two particle's repelling random walks on the complete
graph," Eletron. J. Probab. *19* (113), 1--17, 2014].

## Description

The vertices are visited by walks that choose the next vertex to be
visited according to the number of other walks' visits. Each walk is
repelled by the others. The next vertex to be visited has probability
inversely proportional to the number of visits of the other walks in
it. Self-loops are created by default because the walk can stay at the
same place to the next interaction.

The program output is a file containing the number of visits per time
(row) of each vertex.

## Downloading

The project can be downloaded using `git` as follows:

````
$ git clone https://github.com/aholanda/rrwg.git
$ cd rrwg
````

## Installing

To install the program and the man page in the system path, just run:

````
$ sudo make install
````

## Uninstalling

To uninstall from system path and clear the current directory
from generated files, execute:

````
$ sudo make uninstall
$ make clean
````
## Manual

Default values are assigned to alpha, number of vertices, number of
walks and time steps. To check the default values, just execute the
program to print the help message:

```
rrwg -h
```

To modify the default behavior, the flags may be added as follows:

```
rrwg -a 0.1 -d 4 -m 3 -n 200
```

and the simulation is performed with 200 time steps, 4 vertices, 3
walks and alpha equal to 1.

The execution with the flags

```
rrwg -a 8.5 -d 3 -m 2 -n 1000 -f pow
```

computes the visits of 3 vertices, 2 walks, 1000 time steps and use
the power function to plug into the calculation of transition
probability.

A file with the normalized number of visits is generated and its name
contains the input data. For exemple, the previous execution generates
a file called `d3m2n1000.dat`.