'''
DrawBook

To do:
Bugs:
'''

#!/usr/bin/env python
# -*- coding: utf-8 -*-

from libavg import avg
import DrawBook, DrawNode



class Draw(object):
  '''
  create the draw surface (call DrawNode & create tools)
  left: divNode <- RectNode (background color) & ImageNodes (for tools)
  right: CanvasNode (with RectNode & circleNodes)
  for the beginning: draw only
  '''
  
  
  def __init__(self, j, i, player, imageWidth, screenWidth, screenHeight, imageNumber):
    '''
    loads the tool bar and the draw surface
    '''
    self.j = j
    self.i = i
    self.imageNumber = imageNumber
    self.toolBar = avg.DivNode(id="tools", parent=player.getRootNode())
    avg.RectNode(fillcolor="000000", fillopacity=1.0, parent=self.toolBar, pos=(0, 0), size=(screenWidth-imageWidth, screenHeight), strokewidth=0)
    #DrawNode.DrawNode()
  
  def save(self):
    '''
    saves the image and returns to the gallery
    '''
    self.toolBar.unlink()
    DrawBook.DrawBook.setNewImage(self.j, self.i, self.imageNumber)
    DrawBook.DrawBook.imageNumber += 1