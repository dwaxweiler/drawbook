
from libavg import avg

class Cam(object):

  def __init__(self, player ,imageWidth, screenWidth, screenHeight, iconContainer, toolBar, n):
    # sets delivered arguments global
    self.player = player
    self.imageWidth = imageWidth
    self.screenWidth = screenWidth
    self.screenHeight = screenHeight
    self.icons = iconContainer
    self.toolBar = toolBar
    self.n = n
    
    # create a container for cam elements
    self.camIcons = avg.DivNode(id="camIcons", parent=toolBar, pos=(5, 5))
    self.webcamUnlink = True

    webcam = avg.ImageNode(href="img/webcam.png", parent=iconContainer, pos=(0, 0), size=(self.n, self.n))
    webcam.setEventHandler(avg.CURSORDOWN, avg.TOUCH|avg.MOUSE, self.webcam)

  def webcam(self,event):
    '''
    starts the cam tracking
    http://www.libavg.de/reference/current/areanodes.html#libavg.avg.CameraNode
    '''
    if self.webcamUnlink == True:
      self.camara = avg.CameraNode( id="camara", parent=self.player.getRootNode(), 
        pos=(self.screenWidth - self.imageWidth,0), size=(self.imageWidth, self.screenHeight) , 
        driver='directshow', device="", framerate=15, capturewidth=int(self.imageWidth), 
        captureheight=int(self.screenHeight) ) #, pixelformat="RGB")
      self.webcamUnlink = False

      # save button
      camIconSave = avg.ImageNode(href="img/applycam.png", parent=self.camIcons, pos=(0, 4*self.n), size=(self.n, self.n))
      camIconSave.setEventHandler(avg.CURSORDOWN, avg.TOUCH|avg.MOUSE, self.webcamSnapshot)
      # cancel button
      camIconCancel = avg.ImageNode(href="img/cancelcam.png", parent=self.camIcons, pos=(0, 5*self.n), size=(self.n, self.n))
      camIconCancel.setEventHandler(avg.CURSORDOWN, avg.TOUCH|avg.MOUSE, self.webcamCancel)

      # switch the icons to camicons
      self.icons.opacity = 0
      self.camIcons.opacity = 1
      
      self.camara.play( )
    
      # for testing
      #self.camara.dumpCameras()       # Dumps a list of available cameras to the console.
      #print self.camara.isAvailable() # Returns True if there is a working device that can deliver images attached to the CameraNode
    
    
  def webcamSnapshot(self, event): 
    # is called in the save funktion !
    # take snapshot of the webcam and sets the picture as background
    avg.ImageNode(self.camara.getBitmap(), parent=self.drawCanvas.getRootNode(), 
      pos=(self.screenWidth - self.imageWidth,0), 
      size=(self.imageWidth, self.screenHeight), strokewidth=0)
    #self.drawingSurface.unlink() #i think the draw surface have to be rebuild so u can draw on the new picture
    #self.createDrawingSurface()
    self.webcamCancel()
    
    
  def webcamCancel(self, event):
    if self.webcamUnlink == False:
      self.camara.unlink( )
      self.webcamUnlink = True
      # switch from the camicons back to the normal icons
      self.icons.opacity = 1
      self.camIcons.opacity = 0
      