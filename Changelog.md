# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [v0.2.0] 2022-02-25

### (rrwg.py)
- Create class `Writer` to handle IO operations,
mostly write.
- Add a static method to create a graph called
`create_graph`.
- Create the `__str__` method to the class `Graph`.
- Write the data in float format.
- Put limits in the plot for y axis.
- Improve program arguments handling.

### (Changelog.md)

- Add an example of execution command line.

## [v0.1.0] 2022-02-24

### Added
- The Random Repelling Walks on Graphs simulation was 
ported from C to Python. The user may pass as argument
the number of walks to simulate, the repelling function
to be used and the repelling coefficient called alpha.
The program generates a data file containing the path 
of each walker.
