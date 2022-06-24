# Changelog

All notable changes to this project will be documented in this file.

## 2022-06-24

- Rewrite the entire program separating the funcionalities into
modules.
- Use `pyinstaller` to generate a sigle executable file.

- Simplify the program arguments and the initial assumptions, no input
 file is required.


##  2022-02-25

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

## 2022-02-24

### Added
- The Random Repelling Walks on Graphs simulation was
ported from C to Python. The user may pass as argument
the number of walks to simulate, the repelling function
to be used and the repelling coefficient called alpha.
The program generates a data file containing the path
of each walker.
