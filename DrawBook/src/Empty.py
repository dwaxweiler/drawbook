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
  
  
  def __init__(self,j, i, parentNode, x, y, width, height, player, imageWidth, screenWidth, screenHeight, folder, drawBook):
    '''
    draws the rectangle & sets event handler
    '''
    self.j = j # y position of the rectangle
    self.i = i # x position of the rectangle
    self.player = player # libavg player
    self.imageWidth = imageWidth # width of the image
    self.screenWidth = screenWidth # width of the screen
    self.screenHeight = screenHeight # height of the screen
    self.folder = folder # folder where the new drawing should be saved
    self.drawBook = drawBook # instance of the draw book
    self.parentNode = parentNode
    self.moved = False
    
    # create container
    container = avg.DivNode(id=str(i)+"x"+str(j), parent=parentNode, pos=(x, y), size=(width, height))
    container.setEventHandler(avg.CURSORDOWN, avg.TOUCH|avg.MOUSE, self.onTouch)
    container.setEventHandler(avg.CURSORMOTION, avg.TOUCH|avg.MOUSE, self.scroll)
    container.setEventHandler(avg.CURSORUP, avg.TOUCH|avg.MOUSE, self.release)
    # create white rectangle
    avg.RectNode(fillcolor="FFFFFF", fillopacity=1.0, parent=container, pos=(0, 0), size=(width, height), strokewidth=0)
    # create info text
    text = avg.WordsNode(color="000000", fontsize=20, parent=container, pos=(0, 0), text="Touch to draw here")
    # center text
    text.x = (width - text.width) / 2
    text.y = (height - text.height) / 2


  def onTouch(self, event):
    p = self.drawBook
    if p.captureHolder is None:
		p.captureHolder = event.cursorid
		p.sc_offset_y = event.pos.y
		p.sc_offset_x = event.pos.x
		event.node.setEventCapture(event.cursorid)
		p.touching = True
	
  def startDrawing(self):
	'''
	start to draw on this position
	'''
	if self.drawBook.scrolling or self.moved:
		return
	Draw.Draw(self.j, self.i, self.player, self.imageWidth, self.screenWidth, self.screenHeight, self.folder, self.drawBook)
  
  def release(self,event):
	p = self.drawBook
	if event.cursorid == p.captureHolder:
		p.sc_offset_x = 0
		p.sc_offset_y = 0
		event.node.releaseEventCapture(event.cursorid)
		p.captureHolder = None
	p.touching = False
	p.scrolling = False
	self.startDrawing()
	self.moved = False
	
  def scroll(self, event):
	p = self.drawBook
	if event.cursorid == p.captureHolder and p.touching:
		p.scrolling = True
		self.moved = True
		y_dist = event.pos.y - p.sc_offset_y
		x_dist = event.pos.x - p.sc_offset_x
		p.sc_offset_x = event.pos.x
		p.sc_offset_y = event.pos.y
		p.move(x_dist,y_dist)