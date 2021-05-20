import marshal
from types import CodeType
from bytecodemacro.bytecodecompiler.Compile import Compile #in Compile.py (not a library)

class CodeContext:
    """
        this class holds the data for a piece of intermediary bytecode along with the context surrounding it
    """
    def __init__(self, **kwargs):
        #need to handle non existent key in kwargs
        self.arg_num = 0 if "arg_num" not in kwargs else kwargs["arg_num"] #might not be necersarry
        #skipped kwargnum (in original code object specification
        #skiped something unknown
        #skipped number of locals
        #skipped stacksize
        #skipped flag
        self.bytes = [] if "bytestring" not in kwargs else kwargs["bytestring"]
        self.constants = [] if "constants" not in kwargs else kwargs["constants"]
        self.names = [] if "names" not in kwargs else kwargs["names"]
        #skipped something unknown
        #skipped fname
        self.fname = "" if "fname" not in kwargs else kwargs["fname"] #might not be necersarry, still a lil foggy on the details
        self.name = "" if "name" not in kwargs else kwargs["name"]
        #skipped first line unmber
        #skipped real code line count array
        #skipped something unkown
        #skipped something unknown
        #below this line are things that are probably in the original code object but i'm not
        #sure where
        self.varnames = [] if "varnames" not in kwargs else kwargs["varnames"]
        self.globals = [] if "global_list" not in kwargs else kwargs["global_list"]
        self.cellvars = [] if "cellvars" not in kwargs else kwargs["cellvars"]
        #self.args = [] if "args" not in kwargs else kwargs["args"]

    def MakePyObj(self): #should be called after object is generated from PreProcess.py
        codestring = Compile(self.bytes)
        return CodeType(
                self.arg_num, #arg count
                0, #kwarg count
                0, #still have no clue what this is or how i figured this out
                len(self.varnames), #might not be right
                50000, #note: can't figure this out cause halting problem
                0, #flags for the compiler, (i will need to take a double check at this later)
                codestring,
                tuple(self.constants),
                tuple(self.names),
                tuple(self.varnames),
                "Generated_by_GlubsCPyAsm",
                self.name,
                1,
                bytes([1]*len(self.bytes)), #could be generated a list of ones but tbh don't really matter
                (), #gonna handle freevars later (maybe idk i'm confused (might not be necersarry to hand write (maybe for later compilers))
                tuple(self.cellvars)
        )
