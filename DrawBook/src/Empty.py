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
    
    # create container
    container = avg.DivNode(id=str(i)+"x"+str(j), parent=parentNode, pos=(x, y), size=(width, height))
    container.setEventHandler(avg.CURSORDOWN, avg.TOUCH|avg.MOUSE, self.onTouch)
    # create white rectangle
    avg.RectNode(fillcolor="FFFFFF", fillopacity=1.0, parent=container, pos=(0, 0), size=(width, height), strokewidth=0)
    # create info text
    text = avg.WordsNode(color="000000", fontsize=20, parent=container, pos=(0, 0), text="Touch to draw here")
    # center text
    text.x = (width - text.width) / 2
    text.y = (height - text.height) / 2


  def onTouch(self, event):
    '''
    start to draw on this position
    '''
    Draw.Draw(self.j, self.i, self.player, self.imageWidth, self.screenWidth, self.screenHeight, self.imageNumber, self.folder,
              self.drawBook)