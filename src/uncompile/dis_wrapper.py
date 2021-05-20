import dis

#might have to change it later
def get_str(py_object):
    tmp = dis.Bytecode(py_object)
    return tmp.dis()
