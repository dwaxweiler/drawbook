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
  
  
  def __init__(self, j, i, parentNode, x, y, width, height, player, imageWidth, screenWidth, screenHeight, imageNumber, folder, drawBook):
    '''
    draws the rectangle & sets event handler
    '''
    self.j = j # y position of the rectangle
    self.i = i # x position of the rectangle
    self.player = player # libavg player
    self.imageWidth = imageWidth # width of the image
    self.screenWidth = screenWidth # width of the screen
    self.screenHeight = screenHeight # height of the screen
    self.imageNumber = imageNumber # number of the new drawing
    self.folder = folder # folder where the new drawing should be saved
    self.drawBook = drawBook # instance of the draw book
    
    rect = avg.RectNode(id=str(i)+"x"+str(j), fillcolor="FFFFFF", fillopacity=1.0, parent=parentNode, pos=(x, y), size=(width, height),
                        strokewidth=0)
    rect.setEventHandler(avg.CURSORDOWN, avg.TOUCH|avg.MOUSE, self.onTouch)


  def onTouch(self, event):
    '''
    start to draw on this position
    '''
    Draw.Draw(self.j, self.i, self.player, self.imageWidth, self.screenWidth, self.screenHeight, self.imageNumber, self.folder,
              self.drawBook)