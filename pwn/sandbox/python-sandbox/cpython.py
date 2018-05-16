from ctypes import pythonapi,POINTER,py_object

_get_dict = pythonapi._PyObject_GetDictPtr
_get_dict.restype = POINTER(py_object)
_get_dict.argtypes = [py_object]

del pythonapi,POINTER,py_object

def get_dict(ob):
    return _get_dict(ob).contents.value


