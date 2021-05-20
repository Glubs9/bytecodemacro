# bytecode macro lib
exposes (a slightly modified version of) the bytecode of a function to allow for run-time modification of python syntax.

# how to use
tbh i am quite busy right now so if you want to try using this library I would advise looking at
the examples in meta to see how to use the library and just try to figure it out.
note: as of the current state of documentation i would absolutely not recommended trying this out. But if you come back later I should have added documentation.

# todo
	- add documentation on the modifications to bytecode and how to read it
	- allow for uncompile and the compile packages to be used independently on files for other cool stuff
	- for some reason semantic checking is occuring with the compile method in macro_lib for byte_code tuple assembly from strings, check why and fix
	- increase code re-use
	- clean code of stuff that isn't used from when this was a different project (all the file stuff and header.py)
	- add a .gitignore 
		- add temporary files, compilation and output files to this
	- remove outdated tests in bytecode asm after documentation has finished
	- remove all other temporary test files
