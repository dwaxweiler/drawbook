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
  
  
  def __init__(self, width, height, folder):
    '''
    initializes the setting for the draw book
    arguments: width, height (screen resolution to run in full screen mode), relative path
    '''
    self.height = height # height of the screen
    self.width = width # width of the screen
    self.folder = folder # path to the folder which contains the images
    self.counter = 0 # number of drawn images
    self.player = avg.Player.get() # libavg player
    self.configFileName = 'drawbook_config.txt' # file name of the DrawBook configuration 
    self.player.loadString("""<avg size="("""+str(self.width)+""","""+str(self.height)+""")"></avg>""")
    self.player.setResolution(True, self.width, self.height, 32)
    self.masterDivNode = avg.DivNode(parent=self.player.getRootNode()) # div node which contains all the images
    self.configuration = []; # list containing the configuration of the scene
    
    # check if folder exists
    if not os.path.isdir(self.folder):
      exit('Folder containing the images does not exist!')
    
    # create subfolder for current resolution if it does not exist
    if not os.path.isdir(self.folder + "/" + str(self.width) + "x" + str(self.height)):
      os.makedirs(str(self.width) + "x" + str(self.height))
      
    # create configuration file if it does not exist
    if not os.path.isfile(self.folder):
      fopj = open(self.configFileName, "w")
      fopj.close()
  
  
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
    # calculate y coordinate of first image
    y = (len(self.configuration)*(self.height/5+2)-2-self.height)/-2
    for i in range(len(self.configuration)):
      # calculate x coordinate of first image in each row
      x = (len(self.configuration[i])*(self.width/5+2)-2-self.width)/-2
      for j in range(len(self.configuration[i])):
        path = self.folder + "/" + str(self.width) + "x" + str(self.height) + "/" + str(self.configuration[i][j]) + ".jpg"
        if self.configuration[i][j] != 0 and os.path.isfile(path):
          # draw image if it exists
          avg.ImageNode(id=str(self.configuration[i][j]), href=path, parent=self.masterDivNode,
                        pos=(x, y), size=(self.width/5, self.height/5))
        else:
          # draw rectangle if there is a "0" or image does not exist
          avg.RectNode(id=str(i)+"x"+str(j), fillcolor="FFFFFF", fillopacity=1.0, parent=self.masterDivNode, 
                       pos=(x, y), size=(self.width/5, self.height/5), strokewidth=0)
        x += self.width/5+2
      y += self.height/5+2
  
  
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
    self.draw()
    self.player.play()
  
  
  def scrolling(self):
    '''
    enables scrolling with event handlers (moves the master divNode)
    '''
    return 0



def main():
  book = DrawBook(1440, 900, './')
  book.start()

if __name__ == '__main__':
  main()