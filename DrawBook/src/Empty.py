'''
DrawBook

To do:
Bugs:
'''

#!/usr/bin/env python
# -*- coding: utf-8 -*-

from libavg import avg
import Draw



class Empty(object):
  
  
  def __init__(self, j, i, parentNode, x, y, width, height, player, imageWidth, screenWidth, screenHeight, imageNumber):
    '''
    draws the rectangle & sets event handler
    '''
    self.j = j
    self.i = i
    self.player = player
    self.imageWidth = imageWidth
    self.screenWidth = screenWidth
    self.screenHeight = screenHeight
    self.imageNumber = imageNumber
    rect = avg.RectNode(id=str(i)+"x"+str(j), fillcolor="FFFFFF", fillopacity=1.0, parent=parentNode, pos=(x, y), size=(width, height), strokewidth=0)
    rect.setEventHandler(avg.CURSORDOWN, avg.TOUCH|avg.MOUSE, self.onTouch)


  def onTouch(self, event):
    '''
    start to draw on this position
    '''
    Draw.Draw(self.j, self.i, self.player, self.imageWidth, self.screenWidth, self.screenHeight, self.imageNumber)