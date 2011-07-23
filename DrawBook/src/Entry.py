'''
DrawBook

To do:
Bugs:
'''

#!/usr/bin/env python
# -*- coding: utf-8 -*-

from libavg import avg, ParallelAnim, LinearAnim



class Entry(object):
  
  
  def __init__(self, path, id, parentNode, x, y, screenWidth, screenHeight, imageWidth, factor, DBook):
    '''
    draws the image & sets event handler
    '''
    self.path = path                   # path of the folder where the drawings are saved
    self.id = id                       # identifier of the drawing
    self.parentNode = parentNode       # parent node for the nodes of the larger view
    self.imageWidth = imageWidth       # width of the image
    self.screenWidth = screenWidth     # with of the screen
    self.screenHeight = screenHeight   # height of the screen
    self.db = DBook
    self.moved = False
    
    self.thumb = avg.ImageNode(id=id, href=path + "thumbs/" + id + ".jpg", parent=parentNode, pos=(x, y),
                               size=(imageWidth*factor, screenHeight*factor))
    self.thumb.setEventHandler(avg.CURSORDOWN, avg.TOUCH|avg.MOUSE, self.thumbOnTouch)
    self.thumb.setEventHandler(avg.CURSORMOTION, avg.TOUCH|avg.MOUSE, self.scroll)
    self.thumb.setEventHandler(avg.CURSORUP, avg.TOUCH|avg.MOUSE, self.release)
  
  
  def thumbOnTouch(self, event):
    p = self.db
    if p.captureHolder is None:
      p.captureHolder = event.cursorid
      p.sc_offset_y = event.pos.y
      p.sc_offset_x = event.pos.x
      event.node.setEventCapture(event.cursorid)
      p.touching = True

   
  def largeView(self):
    '''
    bring this image bigger to the front & set event handler to remove it
    '''
    if self.db.scrolling or self.moved:
      return
    self.container = avg.DivNode(parent=self.parentNode, pos=(-self.parentNode.x, -self.parentNode.y), size=(self.screenWidth, self.screenHeight))
    background = avg.RectNode(fillcolor="000000", fillopacity=0, parent=self.container, pos=(0, 0),
                              size=(self.screenWidth, self.screenHeight), strokewidth=0, sensitive=True)
    largeImage = avg.ImageNode(href=self.path + self.id + ".jpg", parent=self.container, pos=(self.thumb.x, self.thumb.y),
                               size=(self.thumb.width, self.thumb.height), sensitive=True)
    animation = ParallelAnim([LinearAnim(largeImage, "x", 500, largeImage.x, (self.screenWidth - self.imageWidth) / 2),
                              LinearAnim(largeImage, "y", 500, largeImage.y, 15),
                              LinearAnim(largeImage, "width", 500, largeImage.width, self.imageWidth-30),
                              LinearAnim(largeImage, "height", 500, largeImage.height, self.screenHeight-30),
                              LinearAnim(background, "fillopacity", 500, background.fillopacity, 0.5)])
    animation.start()
    self.container.setEventHandler(avg.CURSORUP, avg.TOUCH|avg.MOUSE, self.largeOnTouch)
  
  
  def largeOnTouch(self, event):
    '''
    return to normal view
    '''
    self.container.unlink()


  def release(self,event):
    p = self.db
    if event.cursorid == p.captureHolder:
      p.sc_offset_x = 0
      p.sc_offset_y = 0
      event.node.releaseEventCapture(event.cursorid)
      p.captureHolder = None
    p.touching = False
    p.scrolling = False
    self.largeView()
    self.moved = False


  def scroll(self, event):
    p = self.db
    if event.cursorid == p.captureHolder and p.touching:
      p.scrolling = True
      self.moved = True
      y_dist = event.pos.y - p.sc_offset_y
      x_dist = event.pos.x - p.sc_offset_x
      p.sc_offset_x = event.pos.x
      p.sc_offset_y = event.pos.y
      p.move(x_dist,y_dist)