import os.path
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from .HeatCalendar import HeatCalendar
import time

class HeatCalendarLibrary(object):
  """
    Allows to test HeatCalendar.py with robot framework 
  """
  def __init__(self):
    self._result = 'INIT'
  
  def set_time_to(self, testTime):
    self._cal = HeatCalendar(calFile=self._calFile,localtime = lambda t=testTime: time.strptime(t, "%Y %m %d %H %M") )
    self._result = self._cal.getCurrentMode()
    
  def result_should_be(self, expected):
    if str(self._result) != expected: #arguments of robot are always string
      raise AssertionError('%s != %s' % (self._result, expected))

  def set_calendar(self, calFile):
    self._calFile = calFile
