# Changelog

All notable changes to this project will be documented in this file.
The version scheme adopted is `%YYYY%MM%DD` where `Y` is the year,
`M` the month and `D` the day of the release.

## Not realeased
- Add seed as an optional option in `rrwg.conf` to be used
by the pseudo-random number generator.

## 20220831
- Normalize each column in the `rrwg.dat` file by the
walks instead by vertices. The sum of the columns with
the same walk must be one. See #7 and #8.
- Rename `rrwg.conf` to `rrwg.conf.example`. This allows
the use of configuration file in the project directory that
is not overwritten by the project file.

## 20220830
- Fix approximation of the results in `rrwg.dat`.
- R script file is not generated anymore.
- Normalization of number of visits was done in the code.

## 20220826

- Add partitions option in the simulation where a walk can
  go to a complete subgraph from the original graph.
- Increase the details in the log file.
- Put the walk label in the header of data file `rrwg.dat`.
- The program generates a R script to plot the results.
- The program opens the browser to view the plot generated.
- Put a epsilon parameter in the power function.
- All parameters are set in a file called `rrwg.conf`.
- Eliminate all flags.
- Remove the matplotlib part.
- Test and purge CWEB.

## 20220624

- Rewrite the entire program separating the funcionalities into
modules.
- Use `pyinstaller` to generate a sigle executable file.

- Simplify the program arguments and the initial assumptions, no input
 file is required.


##  20220225

### Added
- Create class `Writer` to handle IO operations,
mostly write.
- Add a static method to create a graph called
`create_graph`.
- Create the `__str__` method to the class `Graph`.
- Write the data in float format.
- Put limits in the plot for y axis.
- Improve program arguments handling.
- Add an example of execution command line in the `README`.

## 20220224

### Added
- The Random Repelling Walks on Graphs simulation was
ported from C to Python. The user may pass as argument
the number of walks to simulate, the repelling function
to be used and the repelling coefficient called alpha.
The program generates a data file containing the path
of each walker.
