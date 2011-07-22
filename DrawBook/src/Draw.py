'''
DrawBook

To do:

Bugs:
- strange effects when user is drawing and moves with the finger pressed down right over the tool bar
- webcam may be not working; please test
'''

#!/usr/bin/env python
# -*- coding: utf-8 -*-

from libavg import avg, LinearAnim
import math



class Draw(object):
  
  
  def __init__(self, j, i, player, imageWidth, screenWidth, screenHeight, folder, drawBook):
    '''
    loads the tool bar and the draw surface
    '''
    self.color  = "000000"            # draw color
    self.oldColor = self.color        # previous draw color
    self.colorBarUnlink = True        # variable to prevent the bar to build twice
    self.sizeBarUnlink = True         # variable to prevent the bar to build twice
    self.webcamUnlink = True    
    self.size = 10                    # size of the pencil or eraser (radius)
    self.j = j                        # y-position of the new drawing in the matrix
    self.i = i                        # x-position of the new drawing in the matrix
    self.player = player              # libavg player
    self.imageWidth = imageWidth      # width of the new image
    self.screenWidth = screenWidth    # width of the screen
    self.screenHeight = screenHeight
    self.folder = folder              # folder where the new drawing should be stored
    self.drawBook = drawBook          # instance of the draw book
    self.cursorIDs = {}               # dictionary of all the touches in use with their last position
    
    # create a container for all the toolbar elements
    self.toolBar = avg.DivNode(id="tools", parent=player.getRootNode())
    # create the background of the toolbar
    self.toolBarBackground = avg.RectNode(fillcolor="2a2a2a", fillopacity=1.0, parent=self.toolBar, pos=(0, 0),
                                          size=(screenWidth-imageWidth, screenHeight), strokewidth=0)
    # container that holds all the icons
    icons = avg.DivNode(id="icons", parent=self.toolBar, pos=(5, 5))
    self.icons = icons
    # pace the icons with their functionality on the tool bar
    self.n = screenWidth-imageWidth-10
    # webcam button
    webcam = avg.ImageNode(href="img/webcam.png", parent=icons, pos=(0, 0), size=(self.n, self.n))
    webcam.setEventHandler(avg.CURSORDOWN, avg.TOUCH|avg.MOUSE, self.webcam)
    # pencil button
    tool = avg.ImageNode(href="img/pencil.png", parent=icons, pos=(0, self.n), size=(self.n, self.n))
    self.tool = tool # for dynamic use of the pencil button position
    tool.setEventHandler(avg.CURSORDOWN, avg.TOUCH|avg.MOUSE, self.pencil)
    # color & size chooser
    self.chooserNode = avg.CircleNode(fillcolor=self.color, fillopacity=1.0, parent=icons, pos=(self.n/2, 2*self.n+self.n/2),
                                      r=self.size, strokewidth=3)
    self.chooserNode.setEventHandler(avg.CURSORDOWN, avg.TOUCH|avg.MOUSE, self.chooser)
    # eraser button
    eraser = avg.ImageNode(href="img/eraser.png", parent=icons, pos=(0, 3*self.n), size=(self.n, self.n))
    eraser.setEventHandler(avg.CURSORDOWN, avg.TOUCH|avg.MOUSE, self.eraser)
    self.canelSaveButton()
    # center the icons vertically
    icons.y = (self.screenHeight - 6*self.n) / 2
    
    # create canvas for the drawing surface
    self.drawCanvas = player.loadCanvasString("<canvas id=\"drawing\" width=\""+str(imageWidth)+"\" height=\""+str(screenHeight)+"\"></canvas>")
    avg.RectNode(fillcolor="FFFFFF", fillopacity=1.0, parent=self.drawCanvas.getRootNode(),
                 pos=(0, 0), size=(imageWidth, screenHeight), strokewidth=0)
    self.createDrawingSurface()
    # create a container for cam elements
    self.camIcons = avg.DivNode(id="camIcons", parent=self.toolBar, pos=(5, 5))

  def canelSaveButton(self):
    
    #if self.webcamUnlink == False: # if the cam picture is shown replace the icons
      
    

    #else: # if not shown, draw the old images
      # save button
      #avg.RectNode(fillcolor=self.toolBarBackground.fillcolor, fillopacity=1.0,
      #parent=self.icons, pos=(0, 4*self.n), size=(self.n, self.n), strokewidth=0)
      
      save = avg.ImageNode(href="img/apply.png", parent=self.icons, pos=(0, 4*self.n), size=(self.n, self.n))
      save.setEventHandler(avg.CURSORUP, avg.TOUCH|avg.MOUSE, self.save)
      # cancel button
      #avg.RectNode(fillcolor=self.toolBarBackground.fillcolor, fillopacity=1.0,
      #parent=self.icons, pos=(0, 5*self.n), size=(self.n, self.n), strokewidth=0)
      
      self.cancelIcon = avg.ImageNode(href="img/cancel.png", parent=self.icons, pos=(0, 5*self.n), size=(self.n, self.n))
      self.cancelIcon.setEventHandler(avg.CURSORUP, avg.TOUCH|avg.MOUSE, self.cancel)


  def createDrawingSurface(self):    
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
  
  
  def webcam(self, event):
    '''
    event handler function that starts the webcam and loads the image to the screen
    http://www.libavg.de/reference/current/areanodes.html#libavg.avg.CameraNode
    '''
    if self.webcamUnlink == True:
      self.camara = avg.CameraNode( id="camara", parent=self.player.getRootNode(), 
        pos=(self.screenWidth - self.imageWidth,0), size=(self.imageWidth, self.screenHeight) , 
        driver='directshow', device="", framerate=15, capturewidth=int(self.imageWidth), 
        captureheight=int(self.screenHeight) ) #, pixelformat="RGB")
      self.webcamUnlink = False
      
      
      self.icons.opacity = 0
      self.camIcons.opacity = 1
      
      # save button
      self.camIconSave = avg.ImageNode(href="img/applycam.png", parent=self.camIcons, pos=(0, 4*self.n), size=(self.n, self.n))
      self.camIconSave.setEventHandler(avg.CURSORDOWN, avg.TOUCH|avg.MOUSE, self.save)
      # cancel button
      self.camIconCancel = avg.ImageNode(href="img/cancelcam.png", parent=self.camIcons, pos=(0, 5*self.n), size=(self.n, self.n))
      self.camIconCancel.setEventHandler(avg.CURSORDOWN, avg.TOUCH|avg.MOUSE, self.cancel)
      
      #self.canelSaveButton( ) # swich the save and cancel button
      self.camara.play( )
    
      #self.camara.dumpCameras()       # Dumps a list of available cameras to the console.
      #print self.camara.isAvailable() # Returns True if there is a working device that can deliver images attached to the CameraNode
    
    
  def webcamSnapshot(self): 
    # is called in the save funktion !
    # take snapshot of the webcam and sets the picture as background
    avg.ImageNode(self.camara.getBitmap(), parent=self.drawCanvas.getRootNode(), 
      pos=(self.screenWidth - self.imageWidth,0), 
      size=(self.imageWidth, self.screenHeight), strokewidth=0)
    self.drawingSurface.unlink() #i think the draw surface have to be rebuild so u can draw on the new picture
    self.createDrawingSurface()
    
    self.exit()
    #self.camara.unlink()
    #self.webcamUnlink = True
    #self.canelSaveButton( )
    
    
  def webcamCancel(self):
    if self.webcamUnlink == False:
      self.camara.unlink( )
      self.webcamUnlink = True
      self.canelSaveButton( )
  
  
  def pencil(self, event):
    '''
    event handler function that selects pencil tool
    '''
    self.color = self.oldColor
  
  
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
    sizeCircleArray = [5, 10, 15, 20, 25, 30, 35, 40]
    if self.sizeBarUnlink == True : # only build new sizeBar if previous was unlinked
      self.sizeBar = avg.DivNode( id="size", parent=self.player.getRootNode() ) # container for sizes
      self.sizeBarUnlink = False

    # fill the sizeBar with the given sizes
    countWidth = 0
    count = 0
    
    while (count < len(sizeCircleArray)): # draws one circle for every size
      sizeCircleArray[count] = avg.CircleNode(fillcolor="000000", fillopacity=1.0, parent=self.sizeBar, 
        pos=(self.screenWidth - self.imageWidth + countWidth + (self.n/2), self.tool.y + (self.n*2)), 
        r=sizeCircleArray[count], color = self.toolBarBackground.fillcolor, strokewidth=5)

      sizeCircleArray[count].setEventHandler(avg.CURSORDOWN, avg.TOUCH|avg.MOUSE, self.setSize)
      countWidth = countWidth + self.n
      count = count + 1
    
    
  def setSize (self, event):
    self.size = event.node.r
    self.sizeBar.unlink( )
    self.sizeBarUnlink = True
    self.updateChooserNode()
    
    self.colorBar.unlink( )
    self.colorBarUnlink = True
  
  
  def colorChoose(self):  
    '''
    sets the available colors and builds a container for them
    '''
    # color silver, red, fuchsia, lime, yellow, blue, aqua, black
    colorRecArray = ["c0c0c0", "ff0000", "ff00ff", "00ff00", "ffff00", "0000ff", "00ffff", "000000"]
    if self.colorBarUnlink == True : # only build new colorBar if previous was unlinked
      self.colorBar = avg.DivNode( id="colors", parent=self.player.getRootNode() ) # container for colors
      self.colorBarUnlink = False

    # fill the colorBar with the given colors
    countWidth = 0
    colorCount = 0
    
    while (colorCount < len(colorRecArray)): # draws one rectangle for every color; with the size of n
      colorRecArray[colorCount] = avg.RectNode(fillcolor=colorRecArray[colorCount], fillopacity=1.0, 
          parent=self.colorBar, pos=(self.screenWidth - self.imageWidth + countWidth, self.tool.y), 
          size=(self.n, self.n), color = self.toolBarBackground.fillcolor, strokewidth=2)
      colorRecArray[colorCount].setEventHandler(avg.CURSORDOWN, avg.TOUCH|avg.MOUSE, self.setColor)
      countWidth = countWidth + self.n
      colorCount = colorCount + 1

    
  def setColor ( self, event ):
    '''
    sets the self.color to the color of the chosen rectangle
    '''
    self.color = event.node.fillcolor
    self.colorBar.unlink( )
    self.colorBarUnlink = True
    self.updateChooserNode()

    self.sizeBar.unlink( )
    self.sizeBarUnlink = True
    
  
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
    # previous pencil color (to restore after erasing)
    self.oldColor = self.color
    
    self.color = "FFFFFF"
  
  
  def save(self, event):
    '''
    event handler function that saves the image and returns to the gallery
    '''
    if self.webcamUnlink == False:
      self.webcamSnapshot()
    else:
      # save drawing only when there has been drawn at least one node (remember: one node represents the white background)
      if(self.drawCanvas.getRootNode().getNumChildren() > 1):
        avg.Bitmap(self.player.getCanvas("drawing").screenshot()).save(self.folder + str(self.drawBook.counter) + ".jpg")
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
    if self.webcamUnlink == False: #if cam is activ, canel only the cam picture -> return to drwawing
      self.webcamCancel()
      
      self.icons.opacity = 1
      self.camIcons.opacity = 0
      
      #self.camIconCancel.unlink()
      #self.camIconSave.unlink()
      
    else:
      self.toolBar.unlink()
      self.drawingSurface.unlink()

      if self.colorBarUnlink == False:
        self.colorBar.unlink( )
        self.colorBarUnlink = True
      if self.colorBarUnlink == False:
        self.sizeBar.unlink( )
        self.sizeBarUnlink = True
  
      self.player.deleteCanvas("drawing")