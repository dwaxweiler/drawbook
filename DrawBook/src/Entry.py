'''
DrawBook

To do:
Bugs:
'''

#!/usr/bin/env python
# -*- coding: utf-8 -*-

from libavg import avg



class Entry(object):
  
  
  def __init__(self, path, id, parentNode, x, y, width, height):
    '''
    draws the image & sets event handler
    '''
    image = avg.ImageNode(id=id, href=path, parent=parentNode, pos=(x, y), size=(width, height))
    #image.setEventHandler(avg.CURSORDOWN, avg.TOUCH, self.onTouch())
  
  def onTouch(self):
    '''
    bring this image bigger to the front
    '''
    raise NotImplementedError