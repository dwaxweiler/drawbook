'''
DrawBook

To do:
- use DrawNode.DrawNode()?
Bugs:
'''

#!/usr/bin/env python
# -*- coding: utf-8 -*-

from libavg import avg
import DrawBook, DrawNode



class Draw(object):
  
  
  def __init__(self, j, i, player, imageWidth, screenWidth, screenHeight, imageNumber):
    '''
    loads the tool bar and the draw surface
    '''
    self.j = j # y-position of the new drawing in the matrix
    self.i = i # x-position of the new drawing in the matrix
    self.player = player # libavg player
    self.imageNumber = imageNumber # number that of the new drawing
    
    # create a container for all the tool bar elements
    self.toolBar = avg.DivNode(id="tools", parent=player.getRootNode())
    # create the background of the tool bar
    avg.RectNode(fillcolor="000000", fillopacity=1.0, parent=self.toolBar, pos=(0, 0),
                 size=(screenWidth-imageWidth, screenHeight), strokewidth=0)
    # pace the icons with their functionality on the tool bar
    n = screenWidth-imageWidth-10
    save = avg.ImageNode(href="img/apply.png", parent=self.toolBar, pos=(5, 50), size=(n, n))
    save.setEventHandler(avg.CURSORDOWN, avg.TOUCH|avg.MOUSE, self.save)
    cancel = avg.ImageNode(href="img/cancel.png", parent=self.toolBar, pos=(5, 200), size=(n, n))
    cancel.setEventHandler(avg.CURSORDOWN, avg.TOUCH|avg.MOUSE, self.cancel)
    
    # create canvas for the drawing surface
    self.drawNode = player.loadCanvasString("<canvas id=\"drawing\" width=\""+str(imageWidth)+"\" height=\""+str(screenHeight)+"\"></canvas>")
    avg.RectNode(fillcolor="FFFFFF", fillopacity=1.0, parent=player.getCanvas("drawing").getRootNode(),
                 pos=(0, 0), size=(imageWidth, screenHeight))
    # load canvas in the scene
    self.surface = avg.ImageNode(id="surface", href="canvas:drawing", parent=player.getRootNode(),
                                 pos=(screenWidth-imageWidth, 0), size=(imageWidth, screenHeight))
  
  
  def save(self, event):
    '''
    event handler function that saves the image and returns to the gallery
    '''
    #DrawBook.DrawBook.setNewImage(self.j, self.i, self.imageNumber)
    #DrawBook.DrawBook.imageNumber += 1
    self.exit()
  
  
  def cancel(self, event):
    '''
    event handler function that cancels drawing
    '''
    self.exit()
  
  
  def exit(self):
    '''
    deletes everything related to drawing
    '''
    self.toolBar.unlink()
    self.surface.unlink()
    self.player.deleteCanvas("drawing")