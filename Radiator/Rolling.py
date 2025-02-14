# -*- coding: utf-8 -*-
from collections import deque

# this object manage an ordered rolling list of item, when the end is reached
# the first item will be returned and so on
# Return None when the collection is empty
class Rolling(deque):
   # return the next element of the collection
   def get(self):
      if len(self) == 0:
         return None
      l =self.popleft()
      self.append(l)
      return l
