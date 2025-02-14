# -*- coding: utf-8 -*-

# This utility module define constant

class _const:
    """
      now any client-code can import const
      and bind an attribute ONCE:
      const.magic = 23
    """
    class ConstError(TypeError): pass
    def __setattr__(self,name,value):
        if self.__dict__.get(name):
            raise self.ConstError("Can't rebind const(%s)" % name)
        self.__dict__[name]=value
import sys
sys.modules[__name__]=_const()
