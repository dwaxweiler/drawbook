'''
DrawBook

To do:
- add possibility to change colour
- add possibility to change size
- add possibility to erase (instead of pencil icon -> eraser icon, depending on mode)
- add possibility to take webcam photos
- center toolbar icons vertically
Bugs:
- strange effects when user is drawing and moves with the finger pressed down right over the tool bar
'''

#!/usr/bin/env python
# -*- coding: utf-8 -*-

from libavg import avg
import math



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
    self.drawBook = drawBook # instance of the draw book
    self.cursorIDs = {} # dictionary of all the touches in use with their last position
    
    # create a container for all the tool bar elements
    self.toolBar = avg.DivNode(id="tools", parent=player.getRootNode())
    # create the background of the tool bar
    avg.RectNode(fillcolor="000000", fillopacity=1.0, parent=self.toolBar, pos=(0, 0),
                 size=(screenWidth-imageWidth, screenHeight), strokewidth=0)
    # pace the icons with their functionality on the tool bar
    n = screenWidth-imageWidth-10
    # webcam button
    webcam = avg.ImageNode(href="img/webcam.png", parent=self.toolBar, pos=(5, 50), size=(n, n))
    webcam.setEventHandler(avg.CURSORDOWN, avg.TOUCH|avg.MOUSE, self.webcam)
    # tool button
    tool = avg.ImageNode(href="img/pencil.png", parent=self.toolBar, pos=(5, 200), size=(n, n))
    tool.setEventHandler(avg.CURSORDOWN, avg.TOUCH|avg.MOUSE, self.pencil)
    # save button
    save = avg.ImageNode(href="img/apply.png", parent=self.toolBar, pos=(5, 350), size=(n, n))
    save.setEventHandler(avg.CURSORDOWN, avg.TOUCH|avg.MOUSE, self.save)
    # cancel button
    cancel = avg.ImageNode(href="img/cancel.png", parent=self.toolBar, pos=(5, 500), size=(n, n))
    cancel.setEventHandler(avg.CURSORDOWN, avg.TOUCH|avg.MOUSE, self.cancel)
    
    # create canvas for the drawing surface
    self.drawCanvas = player.loadCanvasString("<canvas id=\"drawing\" width=\""+str(imageWidth)+"\" height=\""+str(screenHeight)+"\"></canvas>")
    avg.RectNode(fillcolor="FFFFFF", fillopacity=1.0, parent=self.drawCanvas.getRootNode(),
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
    self.cursorIDs[event.cursorid] = event.pos
    self.drawCircleNode(event.pos[0]-self.screenWidth+self.imageWidth, event.pos[1])
  
  
  def doDrawing(self, event):
    '''
    event handler function that does the drawing
    '''
    if event.cursorid in self.cursorIDs.keys():
      self.draw(self.cursorIDs[event.cursorid], event.pos)
      self.cursorIDs[event.cursorid] = event.pos
  
  
  def endDrawing(self, event):
    '''
    event handler function that stops the drawing
    '''
    if event.cursorid in self.cursorIDs.keys():
      self.draw(self.cursorIDs[event.cursorid], event.pos)
      del self.cursorIDs[event.cursorid]
  
  def draw(self, pos1, pos2):
    '''
    decides what to draw
    arguments: x1, y1: old position; x2, y2: new position
    '''
    # assign coordinates and translate x coordinates
    x1 = pos1[0]-self.screenWidth+self.imageWidth
    y1 = pos1[1]
    x2 = pos2[0]-self.screenWidth+self.imageWidth
    y2 = pos2[1]
    # use Pythagorean theorem to calculate the distance between the two points and draw a LineNode if it is to far
    if(math.sqrt((x1-x2)**2+(y1-y2)**2) > 5):
      self.drawLineNode(x1, y1, x2, y2)
    self.drawCircleNode(x2, y2)
  
  
  def drawCircleNode(self, x, y):
    '''
    draws a circle node on the given position
    arguments: x, y: position
    '''
    avg.CircleNode(fillcolor="000000", fillopacity=1.0, parent=self.drawCanvas.getRootNode(), pos=(x, y), r=10, strokewidth=0)
  
  
  def drawLineNode(self, x1, y1, x2, y2):
    '''
    draws a line node between the two given positions
    arguments: x1, y1: start position; x2, y2: end position
    '''
    avg.LineNode(color="000000", parent=self.drawCanvas.getRootNode(), pos1=(x1, y1), pos2=(x2, y2), strokewidth=20)
  
  
  def webcam(self, event):
    '''
    event handler function that starts the webcam and loads the image to the screen
    '''
    # http://www.libavg.de/reference/current/areanodes.html#libavg.avg.CameraNode
    return 0
  
  
  def pencil(self, event):
    '''
    event handler function that selects pencil tool
    '''
    return 0
  
  
  def save(self, event):
    '''
    event handler function that saves the image and returns to the gallery
    '''
    # save drawing only when there has been drawn at least one node (remember: one node represents the white background)
    if(self.drawCanvas.getRootNode().getNumChildren() > 1):
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