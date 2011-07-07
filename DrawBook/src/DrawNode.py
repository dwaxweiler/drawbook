'''
DrawBook

To do:
Bugs:
'''

#!/usr/bin/env python
# -*- coding: utf-8 -*-

from libavg import avg



class DrawNode(avg.CanvasNode):
  '''
  fields for size, color
  '''
  
  def __init__(self):
    '''
    creates white RectNode
    '''
    raise NotImplementedError
  
  def save(self):
    '''
    save the node as jpg
    '''
    raise NotImplementedError
  
  