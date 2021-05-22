# bytecode macro lib
exposes (a slightly modified version of) the bytecode of a function to allow for run-time modification of python syntax.

# how to use
for a description of how to use and install the program, please go to the docs folder

# cool example to get you excited
this is a cool example to get you excited with what this library could do and the fun you can have
doing it.
[add example plox]

# todo
	- allow for uncompile and the compile packages to be used independently on files for other cool stuff (maybe)
	- increase code re-use
	- clean code of stuff that isn't used from when this was a different project (all the file stuff and header.py and tests)
	- add error / semantics checking for the returned bytecode (maybe)
	- add more examples
		- optimization macros?
		- steal from examples of lisp macros
	- byte_compile is just soooooo buggy
		- brackets in strings that are bytecompiled don't work for some reason
		- add handling for newly created variables in byte_compile to use store_fast rather than store_name
		- it doesn't compile in the calling scope so it can lead to some wacky situations (variables not recognized)
	- test and then handle encountering the extended arg instruction in the uncompile package
	- test the (end, 0) tuple is not causing any bugs in the bytecodecompile package
