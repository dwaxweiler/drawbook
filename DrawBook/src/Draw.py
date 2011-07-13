'''
DrawBook

To do:
- do drawing with an interval which tracks all the touches every xx ms -> faster reaction
Bugs:
'''

#!/usr/bin/env python
# -*- coding: utf-8 -*-

from libavg import avg



class Draw(object):
  
  
  def __init__(self, j, i, player, imageWidth, screenWidth, screenHeight, imageNumber, folder, drawBook):
    '''
    loads the tool bar and the draw surface
    '''
    self.j = j # y-position of the new drawing in the matrix
    self.i = i # x-position of the new drawing in the matrix
    self.player = player # libavg player
    self.imageWidth = imageWidth # width of the new image
    self.screenWidth = screenWidth # width of the screen
    self.imageNumber = imageNumber # number that of the new drawing
    self.folder = folder # folder where the new drawing should be stored
    self.drawBook = drawBook
    self.cursorIDs = [] # list of all the touches in use
    
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
    self.drawCanvas = player.loadCanvasString("<canvas id=\"drawing\" width=\""+str(imageWidth)+"\" height=\""+str(screenHeight)+"\"></canvas>")
    avg.RectNode(fillcolor="FFFFFF", fillopacity=1.0, parent=player.getCanvas("drawing").getRootNode(),
                 pos=(0, 0), size=(imageWidth, screenHeight), strokewidth=0)
    # load canvas in the scene
    self.drawingSurface = avg.ImageNode(id="surface", href="canvas:drawing", parent=player.getRootNode(),
                                 pos=(screenWidth-imageWidth, 0), size=(imageWidth, screenHeight))
    # set event handlers
    self.drawingSurface.setEventHandler(avg.CURSORDOWN, avg.TOUCH|avg.MOUSE, self.startDrawing)
    self.drawingSurface.setEventHandler(avg.CURSORMOTION, avg.TOUCH|avg.MOUSE, self.doDrawing)
    self.drawingSurface.setEventHandler(avg.CURSORUP, avg.TOUCH|avg.MOUSE, self.endDrawing)
  
  
  def startDrawing(self, event):
    '''
    event handler function that starts the drawing
    '''
    self.cursorIDs.append(event.cursorid)
    self.drawCircleNode(event.pos)
  
  
  def doDrawing(self, event):
    '''
    event handler function that does the drawing
    '''
    if event.cursorid in self.cursorIDs:
      self.drawCircleNode(event.pos)
  
  
  def endDrawing(self, event):
    '''
    event handler function that stops the drawing
    '''
    if event.cursorid in self.cursorIDs:
      self.drawCircleNode(event.pos)
      self.cursorIDs.remove(event.cursorid)
  
  
  def drawCircleNode(self, pos):
    '''
    draws a circle node on the given position
    '''
    avg.CircleNode(fillcolor="000000", fillopacity=1.0, parent=self.drawCanvas.getRootNode(),
                   pos=(pos[0]-self.screenWidth+self.imageWidth, pos[1]), r=10, sensitive=True, strokewidth=0)
  
  
  def save(self, event):
    '''
    event handler function that saves the image and returns to the gallery
    '''
    avg.Bitmap(self.player.getCanvas("drawing").screenshot()).save(self.folder + str(self.imageNumber) + ".jpg")
    self.drawBook.setNewDrawing(self.j, self.i, self.imageNumber)
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
    self.drawingSurface.unlink()
    self.player.deleteCanvas("drawing")