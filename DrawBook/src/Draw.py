'''
DrawBook

To do:
Bugs:
'''

#!/usr/bin/env python
# -*- coding: utf-8 -*-

from libavg import avg, LinearAnim
import math, Cam, Image



class Draw(object):
  
  
  def __init__(self, j, i, player, imageWidth, screenWidth, screenHeight, folder, drawBook):
    '''
    loads the tool bar and the draw surface
    '''
    self.color  = "000000"            # draw color
    self.oldColor = self.color        # previous draw color
    self.colorBarUnlinked = True      # variable to prevent the bar to build twice
    self.sizeBarUnlinked = True       # variable to prevent the bar to build twice
    self.size = 10                    # size of the pencil or eraser (radius)
    self.j = j                        # y-position of the new drawing in the matrix
    self.i = i                        # x-position of the new drawing in the matrix
    self.player = player              # libavg player
    self.imageWidth = imageWidth      # width of the new image
    self.screenWidth = screenWidth    # width of the screen
    self.screenHeight = screenHeight  # height of the screen
    self.folder = folder              # folder where the new drawing should be stored
    self.drawBook = drawBook          # instance of the draw book
    self.cursorIDs = {}               # dictionary of all the touches in use with their last position
    
    # create a container for all the toolbar elements
    self.toolBar = avg.DivNode(parent=player.getRootNode())
    # create the background of the toolbar
    self.toolBarBackground = avg.RectNode(fillcolor="2a2a2a", fillopacity=1.0, parent=self.toolBar, pos=(0, 0),
                                          size=(screenWidth-imageWidth, screenHeight), strokewidth=0)
    # stop drawing if over toolbar
    self.toolBarBackground.setEventHandler(avg.CURSORMOTION, avg.TOUCH|avg.MOUSE, self.endDrawing)
    # container that holds all the icons
    icons = avg.DivNode(parent=self.toolBar, pos=(10, 0))
    self.icons = icons
    # pace the icons with their functionality on the tool bar
    self.n = screenWidth-imageWidth-20
    # webcam button -> calls the camclass
    cam = avg.ImageNode(href="img/webcam.png", parent=icons, pos=(0, 0), size=(self.n, self.n))
    cam.setEventHandler(avg.CURSORDOWN, avg.TOUCH|avg.MOUSE, self.cam)
    # pencil button
    pencil = avg.ImageNode(href="img/pencil.png", parent=icons, pos=(0, self.n), size=(self.n, self.n))
    pencil.setEventHandler(avg.CURSORDOWN, avg.TOUCH|avg.MOUSE, self.pencil)
    # color & size chooser
    self.chooserNode = avg.CircleNode(fillcolor=self.color, fillopacity=1.0, parent=icons, pos=(self.n/2, 2*self.n+self.n/2),
                                      r=self.size, strokewidth=3)
    self.chooserNode.setEventHandler(avg.CURSORDOWN, avg.TOUCH|avg.MOUSE, self.chooser)
    # eraser button
    eraser = avg.ImageNode(href="img/eraser.png", parent=icons, pos=(0, 3*self.n), size=(self.n, self.n))
    eraser.setEventHandler(avg.CURSORDOWN, avg.TOUCH|avg.MOUSE, self.eraser)
    # save button
    save = avg.ImageNode(href="img/apply.png", parent=self.icons, pos=(0, 4*self.n), size=(self.n, self.n), sensitive=True)
    save.setEventHandler(avg.CURSORUP, avg.TOUCH|avg.MOUSE, self.save)
    # cancel button
    cancel = avg.ImageNode(href="img/cancel.png", parent=self.icons, pos=(0, 5*self.n), size=(self.n, self.n))
    cancel.setEventHandler(avg.CURSORUP, avg.TOUCH|avg.MOUSE, self.cancel)
    # center the icons vertically
    icons.y = (self.screenHeight - 6*self.n) / 2
    
    # create canvas for the drawing surface
    self.drawCanvas = player.loadCanvasString("<canvas id=\"drawing\" width=\""+str(imageWidth)+"\" height=\""+str(screenHeight)+"\"></canvas>")
    avg.RectNode(fillcolor="FFFFFF", fillopacity=1.0, parent=self.drawCanvas.getRootNode(),
                 pos=(0, 0), size=(imageWidth, screenHeight), strokewidth=0)
      
    # load canvas in the scene
    self.drawingSurface = avg.ImageNode(id="surface", href="canvas:drawing", parent=self.player.getRootNode(),
                                 pos=(self.screenWidth-self.imageWidth, 0), size=(self.imageWidth, self.screenHeight))
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
    avg.CircleNode(fillcolor=self.color, fillopacity=1.0, parent=self.drawCanvas.getRootNode(), pos=(x, y), r=self.size, strokewidth=0)
  
  
  def drawLineNode(self, x1, y1, x2, y2):
    '''
    draws a line node between the two given positions
    arguments: x1, y1: start position; x2, y2: end position
    '''
    avg.LineNode(color=self.color, parent=self.drawCanvas.getRootNode(), pos1=(x1, y1), pos2=(x2, y2), strokewidth=self.size*2)
  
  
  def cam(self, event):
    '''
    event handler function that starts cam
    '''
    Cam.Cam(self.player, self.imageWidth, self.screenWidth, self.screenHeight, self.toolBar, self.n, self.drawCanvas, self.drawBook)
  
 
  def pencil(self, event):
    '''
    event handler function that selects pencil tool
    '''
    self.color = self.oldColor
    self.updateChooserNode()
  
  
  def chooser(self, event):
    '''
    event handler function that lets choose color and size
    '''
    self.colorChoose()
    self.sizeChoose()
    
    
  def sizeChoose(self):  
    '''
    sets the available sizes and builds a container for them
    '''
    sizeCircleArray = [10, 15, 20, 25, 30, 35, 40]
    if self.sizeBarUnlinked: # only build new sizeBar if previous was unlinked
      self.sizeBar = avg.DivNode( id="size", parent=self.player.getRootNode() ) # container for sizes
      avg.RectNode(fillcolor=self.toolBarBackground.fillcolor, fillopacity=1.0, parent=self.sizeBar,
                   pos=(self.screenWidth-self.imageWidth, self.chooserNode.pos[1] + self.n/2 + 1),
                   size=(len(sizeCircleArray)*self.n + 1, self.n), strokewidth=0)
      self.sizeBarUnlinked = False
      # stop drawing if over size bar
      self.sizeBar.setEventHandler(avg.CURSORMOTION, avg.TOUCH|avg.MOUSE, self.endDrawing)

      # fill the sizeBar with the given sizes
      countWidth = 0
      count = 0
      
      while (count < len(sizeCircleArray)): # draws one circle for every size
        sizeCircleArray[count] = avg.CircleNode(fillcolor="000000", fillopacity=1.0, parent=self.sizeBar, 
          pos=(self.screenWidth - self.imageWidth + countWidth + (self.n/2), self.chooserNode.pos[1] + self.n), 
          r=sizeCircleArray[count], color = "FFFFFF", strokewidth=3)
        sizeCircleArray[count].setEventHandler(avg.CURSORDOWN, avg.TOUCH|avg.MOUSE, self.setSize)
        countWidth = countWidth + self.n
        count = count + 1
    else:
      self.sizeBar.unlink()
      self.sizeBarUnlinked = True
    
    
  def setSize (self, event):
    '''
    sets the self.size to the color of the chosen cirle
    '''
    self.size = event.node.r # sets the new size
    
    #unlink the choosebars
    self.sizeBar.unlink( )
    self.sizeBarUnlinked = True
    self.updateChooserNode()
    
    self.colorBar.unlink( )
    self.colorBarUnlinked = True
  
  
  def colorChoose(self):  
    '''
    sets the available colors and builds a container for them
    '''
    # 6 most important colors of Johannes Itten's Farbkreis
    colorRecArray = ["F4E500", "F19101", "E32322", "6D3889", "2671B2", "008E5B", "000000"]
    if self.colorBarUnlinked: # only build new colorBar if previous was unlinked
      self.colorBar = avg.DivNode( id="colors", parent=self.player.getRootNode() ) # container for colors
      self.colorBarUnlinked = False
      # stop drawing if over color bar
      self.colorBar.setEventHandler(avg.CURSORMOTION, avg.TOUCH|avg.MOUSE, self.endDrawing)
      
      # fill the colorBar with the given colors
      countWidth = 0
      colorCount = 0
      
      while (colorCount < len(colorRecArray)): # draws one rectangle for every color; with the size of n
        colorRecArray[colorCount] = avg.RectNode(fillcolor=colorRecArray[colorCount], fillopacity=1.0, 
            parent=self.colorBar, pos=(self.screenWidth - self.imageWidth + countWidth, self.chooserNode.pos[1] - self.n/2), 
            size=(self.n, self.n), color = self.toolBarBackground.fillcolor, strokewidth=2)
        colorRecArray[colorCount].setEventHandler(avg.CURSORDOWN, avg.TOUCH|avg.MOUSE, self.setColor)
        countWidth = countWidth + self.n
        colorCount = colorCount + 1
    else:
      self.colorBar.unlink()
      self.colorBarUnlinked = True

    
  def setColor ( self, event ):
    '''
    sets the self.color to the color of the chosen rectangle
    '''
    #unlink the choosebars
    self.color = event.node.fillcolor
    self.colorBar.unlink( )
    self.colorBarUnlinked = True
    self.updateChooserNode()

    self.sizeBar.unlink( )
    self.sizeBarUnlinked = True
    
  
  def updateChooserNode(self):
    '''
    updates the chooser node to the set size and color
    '''
    if self.chooserNode.r != self.size:
      # animate the size change
      LinearAnim(self.chooserNode, "r", 500, self.chooserNode.r, self.size).start()
    if self.chooserNode.fillcolor != self.color:
      self.chooserNode.fillcolor = self.color
  

  def eraser(self, event):
    '''
    event handler function that selects eraser tool
    '''
    if self.color != "FFFFFF":
      # previous pencil color (to restore after erasing)
      self.oldColor = self.color
      
      self.color = "FFFFFF"
      self.updateChooserNode()
  
  
  def save(self, event):
    '''
    event handler function that saves the image and returns to the gallery
    '''
    # save drawing only when there has been drawn at least one node (remember: one node represents the white background)
    if(self.drawCanvas.getRootNode().getNumChildren() > 1):
      imagePathName = self.folder + str(self.drawBook.counter) + ".jpg"
      self.player.getCanvas("drawing").screenshot().save(imagePathName)
      # create thumb
      im = Image.open(imagePathName)
      im.thumbnail((int(self.imageWidth/5), int(self.screenWidth/5)))
      im.save(self.folder + "thumbs/" + str(self.drawBook.counter) + ".jpg", "JPEG")
      # set the new drawing in the configuration and display it
      self.drawBook.setNewDrawing(self.j, self.i)
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
    if not self.colorBarUnlinked:
      self.colorBar.unlink()
      self.colorBarUnlinked = True
    if not self.sizeBarUnlinked:
      self.sizeBar.unlink()
      self.sizeBarUnlinked = True
    self.player.deleteCanvas("drawing")