'''
DrawBook

To do:
- methods
- in the beginning whole screen should be filled with empty "boxes"
Bugs:
'''

#!/usr/bin/env python
# -*- coding: utf-8 -*-

from libavg import avg, AVGApp
import os
import Entry, Empty



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
    self.configFileName = 'drawbook_config.txt' # file name of the DrawBook configuration
    self.player = avg.Player.get() # libavg player
    self.player.loadString("""<avg size="("""+str(self.width)+""","""+str(self.height)+""")"></avg>""")
    #self.player.enableMultitouch()
    self.player.setResolution(True, self.width, self.height, 32)
    self.masterDivNode = avg.DivNode(parent=self.player.getRootNode()) # div node which contains all the images
    self.configuration = [[1,0,0,0,0,0], [0,0,0,0,0,2]]; # list containing the configuration of the scene (sublist for each row)
    
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
    raise NotImplementedError
  
  
  def load(self):
    '''
    loads the DrawBook configuration from the file to the list
    '''
    raise NotImplementedError
  
  
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
          Entry.Entry(path, str(self.configuration[i][j]), self.masterDivNode, x, y, self.width/5, self.height/5, self.width, self.height, self.player)
        else:
          # draw rectangle if there is a "0" or image does not exist
          Empty.Empty(str(i)+"x"+str(j), self.masterDivNode, x, y, self.width/5, self.height/5)
        x += self.width/5+2
      y += self.height/5+2
  
  
  def counterUp(self):
    '''
    set the counter 1 up and checks if there is enough free space left
    '''
    self.counter += 1
    
    # count the free "boxes"
    free = 0
    for sublist in self.configuration:
      for elem in sublist:
        if elem == 0:
          free += 1
    # make it bigger if there are no more than 2 free "boxes"
    if free <= 2:
      self.enlarge()
      self.save()
      self.draw()
  
  def enlarge(self):
    '''
    adds new empty space around the images
    '''
    temp = self.configuration
    x_len = len(temp[0])
    y_len = len(temp)
    
    # set new matrix 2 images bigger vertically and horizontally
    self.configuration = []
    # add sublists
    for y in range(y_len+2):
      self.configuration.append([])
    # fill with zeros
    for y in range(y_len+2):
      for x in range(x_len+2):
        self.configuration[y].append(0)
    
    # copy old values from the temporary matrix to the new one
    for y in range(y_len):
      for x in range(x_len):
        self.configuration[y+1][x+1] = temp[y][x]
  
  
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
    # -> last "Uebungsblatt (ListNode)" (but for touches)
    raise NotImplementedError
  



def main():
  book = DrawBook(1440, 900, './')
  book.start()

if __name__ == '__main__':
  main()