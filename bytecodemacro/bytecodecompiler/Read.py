#this file describes the wrapper for reading files

#this might not need it's own file lmao (this is an old comment)

import csv

#this function takes a string and splits it into each instruction and its arguemnts
    #this is done by making use of csv reader which does this automatically
    #it could be debated if this should be moved into parse, but in my opinion this is more of a
    #lexer than a parser but having an entire file just for this function is a bit unecersarry
def read_str(string):
    tmp = [n for n in csv.reader(string.split("\n"), delimiter=" ")]
    return tmp
