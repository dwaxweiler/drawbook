'''
DrawBook

To do:
- perhaps show a smooth overlay "Touch to return/go back" after a few seconds
- change from MOUSE to TOUCH
Bugs:
'''

#!/usr/bin/env python
# -*- coding: utf-8 -*-

from libavg import avg, ParallelAnim, LinearAnim



class Entry(object):
  
  
  def __init__(self, path, id, parentNode, x, y, screenWidth, screenHeight, imageWidth, factor):
    '''
    draws the image & sets event handler
    '''
    self.parentNode = parentNode # parent node for the nodes of the larger view
    self.imageWidth = imageWidth # width of the image
    self.screenWidth = screenWidth # with of the screen
    self.screenHeight = screenHeight # height of the screen
    
    self.thumb = avg.ImageNode(id=id, href=path, parent=parentNode, pos=(x, y), size=(imageWidth*factor, screenHeight*factor))
    self.thumb.setEventHandler(avg.CURSORDOWN, avg.TOUCH|avg.MOUSE, self.thumbOnTouch)
  
  
  def thumbOnTouch(self, event):
    '''
    bring this image bigger to the front & set event handler to remove it
    '''
    self.container = avg.DivNode(parent=self.parentNode, pos=(0, 0), size=(self.screenWidth, self.screenHeight))
    background = avg.RectNode(fillcolor="000000", fillopacity=0, parent=self.container, pos=(0, 0),
                              size=(self.screenWidth, self.screenHeight), strokewidth=0, sensitive=True)
    largeImage = avg.ImageNode(href=self.thumb.href, parent=self.container, pos=(self.thumb.x, self.thumb.y),
                               size=(self.thumb.width, self.thumb.height), sensitive=True)
    animation = ParallelAnim([LinearAnim(largeImage, "x", 500, largeImage.x, (self.screenWidth - self.imageWidth) / 2),
                              LinearAnim(largeImage, "y", 500, largeImage.y, 15),
                              LinearAnim(largeImage, "width", 500, largeImage.width, self.imageWidth-30),
                              LinearAnim(largeImage, "height", 500, largeImage.height, self.screenHeight-30),
                              LinearAnim(background, "fillopacity", 500, background.fillopacity, 0.5)])
    animation.start()
    self.container.setEventHandler(avg.CURSORDOWN, avg.TOUCH|avg.MOUSE, self.largeOnTouch)
    
  
  def largeOnTouch(self, event):
    '''
    return to normal view
    '''
    self.container.unlink()