from sys import modules
from cpython import get_dict
from types import FunctionType

main  = modules['__main__'].__dict__
origin_builtins = main['__builtins__'].__dict__

def delete_type():
    type_dict = get_dict(type)
    del type_dict['__bases__']
    del type_dict['__subclasses__']

def delete_func_code():
    func_dict = get_dict(FunctionType)
    del func_dict['func_code']

def safe_import(__import__,whiteList):
    def importer(name,globals={},locals={},fromlist=[],level=-1):
        if name in whiteList:
            return __import__(name,globals,locals,fromlist,level)
        else:
            print "HAHA,[%s]  has been banned~" % name
    return importer

class ReadOnly(dict):
    """docstring for ReadOnlu"""
    def __delitem__(self,keys):
        raise ValueError(":(")
    def pop(self,key,default=None):
        raise ValueError(":(")
    def popitem(self):
        raise ValueError(":(")
    def setdefault(self,key,value):
        raise ValueError(":(")
    def __setitem__(self,key,value):
        raise ValueError(":(")
    def __setattr__(self, name, value):
        raise ValueError(":(")
    def update(self,dict,**kwargs):
        raise ValueError(":(")

def builtins_clear():
    whiteList = "raw_input  SyntaxError   ValueError  NameError  Exception __import__".split(" ")
    for mod in __builtins__.__dict__.keys():
        if mod not in whiteList:
            del __builtins__.__dict__[mod]

def input_filter(string):
    ban = "exec eval pickle os subprocess input sys ls cat".split(" ")
    for i in ban:
        if i in string.lower():
            print "{} has been banned!".format(i)
            return ""
    return string

# delete_type();
del delete_type
delete_func_code();del delete_func_code
builtins_clear();del builtins_clear


whiteMod = []
origin_builtins['__import__'] = safe_import(__import__,whiteMod)
safe_builtins = ReadOnly(origin_builtins);del ReadOnly
main['__builtins__'] = safe_builtins;del safe_builtins

del get_dict,modules,origin_builtins,safe_import,whiteMod,main,FunctionType
del __builtins__, __doc__, __file__, __name__, __package__

print """
  ____
 |  _ \ _   _ _ __
 | |_) | | | | '_ \
 |  _ <| |_| | | | |
 |_| \_\\__,_|_| |_|


Escape from the dark house built with python :)

Try to getshell then find the flag!

"""

while 1:
    inp = raw_input('>>>')
    cmd = input_filter(inp)
    try:
        exec cmd
    except NameError, e:
        print "wow something lose!We can\'t find it !  D:"
    except SyntaxError,e:
        print "Noob! Synax Wrong! :("
    except Exception,e:
        print "unknow error,try again  :>"