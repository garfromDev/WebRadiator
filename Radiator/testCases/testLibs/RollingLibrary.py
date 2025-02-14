import os.path
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from .Rolling import Rolling

class RollingLibrary(object):
    """
    Allows to test Rolling.py with robot framework 
    """
    def __init__(self):
      self._result = ''
      self._roll = Rolling()
      
    def create_rolling_list_with(self, list):
       self._roll = Rolling(list)
      
    def result_should_be(self, expected):
      if str(self._result) != expected: #arguments of robot are always string
         raise AssertionError('%s != %s' % (self._result, expected))
         
    def get_next(self):
      self._result = self._roll.get()
