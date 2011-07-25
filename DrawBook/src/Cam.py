'''
DrawBook

To do:
Bugs:
- webcam is not working
'''

#!/usr/bin/env python
# -*- coding: utf-8 -*-

from libavg import avg



class Cam(object):


  def __init__(self, player ,imageWidth, screenWidth, screenHeight, toolBar, n, drawCanvas):
    '''
    starts the cam tracking
    '''
    # sets delivered arguments global
    self.player = player
    self.imageWidth = imageWidth
    self.screenWidth = screenWidth
    self.screenHeight = screenHeight
    self.toolBar = toolBar
    self.n = n
    self.drawCanvas = drawCanvas
    
    # create a container for all the toolbar elements
    self.toolBar = avg.DivNode(parent=player.getRootNode())
    # create the background of the toolbar
    self.toolBarBackground = avg.RectNode(fillcolor="2a2a2a", fillopacity=1.0, parent=self.toolBar, pos=(0, 0),
                                          size=(screenWidth-imageWidth, screenHeight), strokewidth=0)
    # container that holds all the icons
    icons = avg.DivNode(parent=self.toolBar, pos=(10, 0))
    # save button
    camIconSave = avg.ImageNode(href="img/applycam.png", parent=icons, pos=(0, 0), size=(self.n, self.n))
    camIconSave.setEventHandler(avg.CURSORDOWN, avg.TOUCH|avg.MOUSE, self.save)
    # cancel button
    camIconCancel = avg.ImageNode(href="img/cancelcam.png", parent=icons, pos=(0, self.n), size=(self.n, self.n))
    camIconCancel.setEventHandler(avg.CURSORDOWN, avg.TOUCH|avg.MOUSE, self.cancel)
    # center the icons vertically
    print (self.screenHeight - 2*self.n) / 2
    icons.y = (self.screenHeight - 2*self.n) / 2
    
    # create the camera node
    self.camera = avg.CameraNode( id="camera", parent=self.player.getRootNode(),
      pos=(self.screenWidth - self.imageWidth,0), size=(self.imageWidth, self.screenHeight) ,
      driver='directshow', device="", framerate=15, capturewidth=int(self.imageWidth),
      captureheight=int(self.screenHeight), pixelformat="YUV422")
    
    # read this:
    # http://www.libavg.de/reference/current/areanodes.html#libavg.avg.CameraNode
    # http://www.libavg.de/wiki/ProgrammersGuide/CameraNode
    # try first with: avg_showcamera.py !
    # for testing
    self.camera.dumpCameras()       # Dumps a list of available cameras to the console.
    print self.camera.isAvailable() # Returns True if there is a working device that can deliver images attached to the CameraNode
    
    # start the camera
    self.camera.play()
    
    
  def save(self, event):
    '''
    event handler function that takes a snapshot of the webcam and sets the picture as background
    '''
    if self.camera.isAvailable():
      avg.ImageNode(self.camera.getBitmap(), parent=self.drawCanvas.getRootNode(), pos=(self.screenWidth - self.imageWidth,0), 
                    size=(self.imageWidth, self.screenHeight), strokewidth=0)
    self.exit()


  def cancel(self, event):
    '''
    event handler function that cancels the cam
    '''
    self.exit()
  
  
  def exit(self):
    '''
    deletes everything related to the cam
    '''
    self.toolBar.unlink()
    self.camera.unlink()