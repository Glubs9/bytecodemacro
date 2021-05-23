#this file describes some of the functional programming functions that get reused a lot and puts
#them here

from functools import reduce

#used to compose the pre-processing functions together
    #compose and bind are both used in both pre_processing here and uncompile and should be
    #moved somewhere else to increase code reuse
def compose(*f_list):
    def ret(arg):
        return reduce(lambda a,n: n(a), f_list, arg)
    return ret

#equivalent to the list monads bind operator. any attempt to explain this will end up just
#re-writing the code in comment form, please try to understand this be reading it yourself
def bind(f, li): #f is a function that takes an element from li and reutrns a list
    return list(reduce(lambda a1,a2: a1+a2, map(f, li))) #the + in here is list concatenation
