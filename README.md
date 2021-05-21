# bytecode macro lib
exposes (a slightly modified version of) the bytecode of a function to allow for run-time modification of python syntax.

# how to use
for a description of how to use and install the program, please go to the docs folder

# todo
	- test pip
	- add documentation on the modifications to bytecode and how to read it
	- allow for uncompile and the compile packages to be used independently on files for other cool stuff
	- for some reason semantic checking is occuring with the compile method in macro_lib for byte_code tuple assembly from strings, check why and fix
	- increase code re-use
	- clean code of stuff that isn't used from when this was a different project (all the file stuff and header.py)
	- add a .gitignore 
		- add temporary files, compilation and output files to this
	- remove outdated tests in bytecode asm after documentation has finished
	- remove all other temporary test files
	- remove the example files in meta and move them to the documentation for some examples
	- do something about those long ass import statements
	- add error / semantics checking for the returned bytecode
	- add more examples
		- optimization macros?
		- steal from examples of lisp macros
