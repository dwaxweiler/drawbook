'''
DrawBook

To do:
- perhaps add animation that brings image to front (instead of creating new image node)
- perhaps show a smooth overlay "Touch to return/go back" after a few seconds
Bugs:
- when viewing an image, in the border you can touch other images, when oneself again -> crash
  -> create a grey background and set event handler here
'''

#!/usr/bin/env python
# -*- coding: utf-8 -*-

from libavg import *



class Entry(object):
  
  
  def __init__(self, path, id, parentNode, x, y, width, height, screenWidth, screenHeight, player):
    '''
    draws the image & sets event handler
    '''
    self.path = path # path to the image file
    self.id = id # id for this image
    self.parentNode = parentNode # parent node for this image
    self.screenWidth = screenWidth # with of the screen
    self.screenHeight = screenHeight # height of the screen
    self.player = player
    self.image = avg.ImageNode(id=id, href=path, parent=parentNode, pos=(x, y), size=(width, height))
    self.image.setEventHandler(avg.CURSORDOWN, avg.MOUSE, self.thumbOnTouch)
    
  
  
  def thumbOnTouch(self, event):
    '''
    bring this image bigger to the front & set event handler to remove it
    '''
    print self.image.x
    animObj = ParallelAnim(
      [LinearAnim(self.image, "x", 1000, self.image.x, 10),
       LinearAnim(self.image, "y", 1000, self.image.y, 10),
       LinearAnim(self.image, "width", 1000, self.image.width, self.screenWidth-20),
       LinearAnim(self.image, "height", 1000, self.image.height, self.screenHeight-20)])
    animObj.start()
    # currently @ work here!
    
    #self.bigImage = avg.ImageNode(id=self.id+"large", href=self.path, parent=self.parentNode, pos=(10, 10), size=(self.screenWidth-20, self.screenHeight-20))
    #self.bigImage.setEventHandler(avg.CURSORDOWN, avg.MOUSE, self.largeOnTouch)
    
  
  def largeOnTouch(self, event):
    '''
    return to normal view
    '''
    self.bigImage.unlink()