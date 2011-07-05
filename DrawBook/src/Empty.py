'''
DrawBook

To do:
Bugs:
'''

#!/usr/bin/env python
# -*- coding: utf-8 -*-

from libavg import avg



class Empty(object):
  
  
  def __init__(self, id, parentNode, x, y, width, height):
    '''
    draws the rectangle & sets event handler
    '''
    rect = avg.RectNode(id=id, fillcolor="FFFFFF", fillopacity=1.0, parent=parentNode, pos=(x, y), size=(width, height), strokewidth=0)
    rect.setEventHandler(avg.CURSORDOWN, avg.TOUCH, self.onTouch)
    
  def onTouch(self, event):
    '''
    start to draw on this position
    '''
    raise NotImplementedError