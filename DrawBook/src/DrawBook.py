'''
DrawBook

To do:
Bugs:
'''

#!/usr/bin/env python
# -*- coding: utf-8 -*-

from libavg import avg, AVGApp
import os



class DrawBook(AVGApp):
  
  
  def __init__(self, width, height, imageFolder, configFileName):
    '''
    initializes the setting for the draw book
    arguments: width, height (screen resolution to run in full screen mode), path
    '''
    self.height = height # height of the screen
    self.width = width # width of the screen
    self.imageFolder = imageFolder # path to the folder which contains the images
    self.counter = 0 # number of drawn images
    self.player = avg.Player.get() # libavg player
    self.configFileName = configFileName # file name of the DrawBook configuration 
    self.player.loadString("""<avg size="("""+str(self.width)+""","""+str(self.height)+""")"></avg>""")
    self.player.setResolution(True, self.width, self.height, 32)
    self.masterDivNode = avg.DivNode(parent=self.player.getRootNode()) # div node which contains all the images
    
    # check if folder of images exists
    if not os.path.isdir(self.imageFolder):
      exit('Folder containing the images does not exist!')
    
    # create folder for resolution if it does not exist
    if not os.path.isdir(self.imageFolder + "/" + str(self.width) + "x" + str(self.height)):
      os.makedirs(str(self.width) + "x" + str(self.height))
  
  
  def save(self):
    '''
    saves the DrawBook configuration from the list to the file
    '''
    return 0
  
  
  def load(self):
    '''
    loads the DrawBook configuration from the file to the list
    '''
    return 0
  
  
  def draw(self):
    '''
    draws the images of the list
    '''
    return 0
    ''' delete this if not helpful
    y = -self.height/10
    for i in range(6):
      x = -self.width/10
      for j in range(6):
        avg.RectNode(fillcolor="FFFFFF", fillopacity=1.0, parent=self.player.getRootNode(), 
                     pos=(x, y), size=(self.width/5, self.height/5), strokewidth=0)
        avg.WordsNode(color="000000", fontsize=25, parent=self.player.getRootNode(),
                      pos=(x+50, y+self.height/10-25), text="Touch to draw here")
        x += self.width/5+2
      y += self.height/5+2
    '''
  
  
  def counterUp(self):
    '''
    set the counter 1 up and checks if there enough free space left
    '''
    return 0
  
  def enlarge(self):
    '''
    adds new empty space around the images
    '''
    return 0
  
  
  def start(self):
    '''
    starts the draw book
    '''
    self.player.play()
  
  
  def scrolling(self):
    '''
    enables scrolling with event handlers (moves the master divNode)
    '''
    return 0



def main():
  book = DrawBook(1440, 900, './', '')
  book.start()

if __name__ == '__main__':
  main()