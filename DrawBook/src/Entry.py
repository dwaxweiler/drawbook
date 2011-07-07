'''
DrawBook

To do:
- perhaps show a smooth overlay "Touch to return/go back" after a few seconds
- change from MOUSE to TOUCH
Bugs:
'''

#!/usr/bin/env python
# -*- coding: utf-8 -*-

from libavg import *



class Entry(object):
  
  
  def __init__(self, path, id, parentNode, x, y, width, height, imageWidth, screenWidth, screenHeight):
    '''
    draws the image & sets event handler
    '''
    self.parentNode = parentNode # parent node for this image
    self.imageWidth = imageWidth
    self.screenWidth = screenWidth # with of the screen
    self.screenHeight = screenHeight # height of the screen
    self.thumb = avg.ImageNode(id=id, href=path, parent=parentNode, pos=(x, y), size=(width, height))
    self.thumb.setEventHandler(avg.CURSORDOWN, avg.MOUSE, self.thumbOnTouch)
  
  
  def thumbOnTouch(self, event):
    '''
    bring this image bigger to the front & set event handler to remove it
    '''
    self.background = avg.DivNode(id=self.thumb.id+"background", parent=self.parentNode, pos=(0, 0),
                                  size=(self.screenWidth, self.screenHeight))
    self.largeImage = avg.ImageNode(id=self.thumb.id+"large", href=self.thumb.href, parent=self.background,
                                      pos=(self.thumb.x, self.thumb.y), size=(self.thumb.width, self.thumb.height),
                                      sensitive=True)
    animation = ParallelAnim(
      [LinearAnim(self.largeImage, "x", 500, self.largeImage.x, (self.screenWidth - self.imageWidth) / 2),
       LinearAnim(self.largeImage, "y", 500, self.largeImage.y, 15),
       LinearAnim(self.largeImage, "width", 500, self.largeImage.width, self.imageWidth-30),
       LinearAnim(self.largeImage, "height", 500, self.largeImage.height, self.screenHeight-30)])
    animation.start()
    self.background.setEventHandler(avg.CURSORDOWN, avg.MOUSE, self.largeOnTouch)
    
  
  def largeOnTouch(self, event):
    '''
    return to normal view
    '''
    self.largeImage.unlink()
    self.background.unlink()