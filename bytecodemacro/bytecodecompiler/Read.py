#this file describes the wrapper for reading files
    #it is a relic of when this project was differnet and should be deleted

#this might not need it's own file lmao (this is an old comment)

import csv

#reads a string from a file, calls read_str on it and returns it
def read(fname):
    return read_str(open(fname, "r").read())

#this function takes a string and splits it into each instruction and its arguemnts
    #this is done by making use of csv reader which does this automatically
    #it could be debated if this should be moved into parse, but in my opinion this is more of a
    #lexer than a parser but having an entire file just for this function is a bit unecersarry
def read_str(string):
    tmp = [n for n in csv.reader(string.split("\n"), delimiter=" ")]
    return tmp
