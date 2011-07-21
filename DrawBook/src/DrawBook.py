'''
DrawBook

To do:
- scrolling
- test enlarging (adding more free space)
- (add zoom effect also to the start of drawing)
Bugs:
'''

#!/usr/bin/env python
# -*- coding: utf-8 -*-

from libavg import avg, AVGApp
import os
import Entry, Empty



class DrawBook(AVGApp):
  
  
  def __init__(self, folder):
    '''
    initializes the setting for the draw book
    arguments: width, height (screen resolution to run in full screen mode), relative path
    '''
    self.player = avg.Player.get() # libavg player
    Point2D = self.player.getScreenResolution() #get the resolution of the used screen
    self.height = int(Point2D.y) # height of the screen
    self.width = int(Point2D.x) # width of the screen
    self.imageWidth = int(Point2D.x)*0.9 # width of the image
    self.folder = folder # path to the folder which contains the images
    self.counter = 0 # number of next drawing
    self.configFileName = 'drawbook_config.txt' # file name of the DrawBook configuration   
    self.player.loadString("""<avg size="("""+str(self.width)+""","""+str(self.height)+""")"></avg>""")
    #self.player.enableMultitouch() #uncomment this line to activate multitouch
    self.player.setResolution(True, self.width, self.height, 32)
    self.masterDivNode = avg.DivNode(parent=self.player.getRootNode()) # div node which contains all the images
    self.configuration = []; # list containing the configuration of the scene (sublist for each row)
    self.leftmargin = 0
    self.topmargin = 0
    self.selectiontime = 1000
    self.scrolling = False
    self.touching = False
    self.sc_offset_x = 0
    self.sc_offset_y = 0
    self.captureHolder = None
    
    # check if folder exists
    if not os.path.isdir(self.folder):
      exit('Folder containing the images does not exist!')
    
    # create subfolder for images for current resolution if it does not exist
    if not os.path.isdir(self.folder + "/" + str(self.width) + "x" + str(self.height)):
      os.makedirs(str(self.width) + "x" + str(self.height))
      
  
  def save(self):
    '''
    saves the DrawBook configuration from the list to the file
    '''
    with open(self.folder + "/" + str(self.width) + "x" + str(self.height) + "/" + self.configFileName, "w") as f:
      for sublist in self.configuration:
        for elem in sublist:
          f.write(str(elem) + " ")
        f.write("\n")
  
  
  def load(self):
    '''
    loads the DrawBook configuration from the file to the list
    '''
    self.configuration = []
    if os.path.isfile(self.folder + "/" + str(self.width) + "x" + str(self.height) + "/" + self.configFileName):
      # load data from the configuration file if it exists
      max = 0
      with open(self.folder + "/" + str(self.width) + "x" + str(self.height) + "/" + self.configFileName, "r") as f:
        for line in f:
          sublist = line.split(" ")
          # remove the last element "\n"
          del sublist[-1]
          self.configuration.append(sublist)
          for elem in sublist:
            if int(elem) > max:
              max = int(elem)
      self.counter = max
    else:
      # load minimal empty list because the configuration file does not exist
      self.counter = 0
      self.configuration = [[0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0]]
    self.counter += 1
    
  
  def draw(self):
    '''
    draws the images of the list
    '''
    # calculate y coordinate of first image
    y = (len(self.configuration)*(self.height/5+2)-2-self.height)/-2
    self.leftmargin = abs(y)
    for i in range(len(self.configuration)):
      # calculate x coordinate of first image in each row
      x = (len(self.configuration[i])*(self.imageWidth/5+2)-2-self.width)/-2
      if abs(x) > self.topmargin:
		self.topmargin = abs(x)
      for j in range(len(self.configuration[i])):
        path = self.folder + "/" + str(self.width) + "x" + str(self.height) + "/" + str(self.configuration[i][j]) + ".jpg"
        if self.configuration[i][j] != 0 and os.path.isfile(path):
          # draw image if it exists
          Entry.Entry(path, str(self.configuration[i][j]), self.masterDivNode, x, y,
                      self.width, self.height, self.imageWidth, 0.2, self)
        else:
          # draw rectangle if there is a "0" or image does not exist
          Empty.Empty(i, j, self.masterDivNode, x, y, self.imageWidth/5, self.height/5, self.player, self.imageWidth, self.width,
                      self.height, self.folder + "/" + str(self.width) + "x" + str(self.height) + "/", self)
        x += self.imageWidth/5+2
      y += self.height/5+2
    self.move(500,500)
  
  
  def counterUp(self):
    '''
    set the counter 1 up and checks if there is enough free space left
    '''
    self.counter += 1
    
    # count the rectangles
    free = 0
    for sublist in self.configuration:
      for elem in sublist:
        if int(elem) == 0:
          free += 1
    # make it bigger if there are no more than 2 rectangles
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
  
  
  def setNewDrawing(self, j, i):
    '''
    updates the configuration list with a new image & updates the file and the scene
    arguments: j, i: coordinates in the matrix, n: file name
    '''
    # set the number of the new drawing on the correct place in the matrix
    self.configuration[j][i] = self.counter;
    # save this configuration
    self.save()
    # get the rectangle where the new drawing should be shown now
    rectangle = self.player.getElementByID(str(i) + "x" + str(j))
    # delete this rectangle
    rectangle.unlink()
    # put the drawing on the place where the rectangle was
    Entry.Entry(self.folder + "/" + str(self.width) + "x" + str(self.height) + "/" + str(self.counter) + ".jpg", "entr"+str(self.counter+1),
                self.masterDivNode, rectangle.pos[0], rectangle.pos[1], self.width, self.height, self.imageWidth, 0.2,self)
    # set the counter up and enlarge if necessary
    self.counterUp()
	
  def move(self, x_offset, y_offset):
	'''
	moves over the DrawBook, negative values move the view to the left/up
	'''
	if abs(x_offset) > self.leftmargin:
		x_offset = x_offset/abs(x_offset)*self.leftmargin
	if abs(y_offset) > self.topmargin:
		y_offset = y_offset/abs(y_offset)*self.topmargin
	print("moving "+str(x_offset)+" and "+ str(y_offset))
	self.masterDivNode.x = self.masterDivNode.x + x_offset
	self.masterDivNode.y = self.masterDivNode.y + y_offset

  def start(self):
    '''
    starts the draw book
    '''
    #self.scrolling()
    self.load()
    self.draw()
    self.player.play()
    #RuntimeError: Must call Player.play() before isMultitouchAvailable().
    #if(self.player.isMultitouchAvailable()):  #detects if the system supportes multitouch
    #  self.player.enableMultitouch()          #activate multitouch



def main():

  book = DrawBook('./')
  book.start()

if __name__ == '__main__':
  main()