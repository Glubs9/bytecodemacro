#this file describes the wrapper for reading files
    #it is a relic of when this project was differnet and should be deleted

#this might not need it's own file lmao (this is an old comment)

import csv

#i don't think this has been called
def read(fname):
    return read_str(open(fname, "r").read())

#no need for a lexer as the csvreader does it automatically
def read_str(string):
    tmp = [n for n in csv.reader(string.split("\n"), delimiter=" ")]
    return tmp
