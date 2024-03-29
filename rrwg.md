% RRWG(1)
% Adriano J. Holanda developed the program. Rafael A. Rosales proposed the idea and helped in the simulation design
% 2022-08-26 rrwg man page

# NAME

rrwg - simulate vertex-reinforced random walks on graphs

# SYNOPSIS

rrwg

# DESCRIPTION

*rrwg* simulates the vertex-reinforced random walks on graphs

# FILE

An input file called `rrwg.conf` is used to configure the simulation
behavior. In the file, the folowing parameters may be set:

```
[default]
type=[complete|partitions]
vertices=<integer>
alpha=<float>
epsilon=<float>
time=<integer>
partitions=<integer>
function=[EXP|POW]
```

The parameters are described as follows:

type - `complete` indicates no partition is considered,
	all walks can visit all vertices. Otherwise,
	`partition` is used to indicate that the walks
	are restricted to certain connected vertices
	that are complete subgraphs.
<"complete"|"partitions">

vertices - number of vertices used in the simulation
<integer>

alpha - reinforcing factor
<float>

epsilon - Pigeard/Rosales factor (optional)
<float>

partition_size - number of vertices in each partition
<integer>

seed - seed for the pseudo-random number generator (optional)
<integer>

time - number of steps to perform
<integer>

function - name of the function to be used in the transition
	   probability calculation
<"EXP"|"POW">

The function parameter may be

EXP exponential
: f(x) =  exp(-o(x)*alpha)

POW power
: f(x) = x*(m - epsilon*x  o(x))^alpha

: o(x) = normalized sum of visits from other walks

where m is the number of walks.
