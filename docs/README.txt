this is the documentation folder for the python library bytecodemacro

this is not the easiest package to just dive into but i hope you'll come to find it's easier to use
then many of the other macro libraries written for python.

installation instructions are in install.txt

i would recommend reading prerequisites.txt before going through this file just to make sure you're
caught up on some of the python internals that I will be referring to throughout the documentation
but if you're confident feel free to skip it.

the main entry point for using this project is the python function decorator macro (you can from
bytecodemacro import macro to access this). This decorator allows for you to access a human readable
format of python bytecode, modify it and have the newly modified bytecode become the new function.

how this project works is that it takes in a python function, gets its code object, converts it to a
more human readable python bytecode format, passes that bytecode to the function passed with the
macro decorator, gets the returned bytecode, converts that back to a python function and returns it.
Allowing for the newly created and modified function to be used in python code.

for some examples go to examples.py
for a specification on how the format works refer to bytecode_format.txt
for a description of all the functions that are available with the package, go to api.txt
for a guide on the architecture of the packages please refer to architecture.txt
for contributing information please go to contributinginformation.txt

please contact me at jonte.fry@gmail.com if you have any questions or you have submitted a pull
request on github and want to see it included (as i am not very active on github itself so i might
not see it for a bit).

please try to keep the conversation positive in the github and I look forward to seeing the wacky
things you make with this library.

have fun!
