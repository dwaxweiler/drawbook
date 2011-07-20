#!/usr/bin/env python
# -*- coding: utf-8 -*-

from libavg import avg

class ListNode (avg.DivNode):
	
	def __init__ (self, stringlist, visibleEntries,parent='',fontsize=15, selectColor='FF0000', entryColor='FFFFFF', inputMethod = avg.TOUCH, clickTime = 1000):
				"""
				initializes a ListNode object
				@param stringlist: a list of strings to display
				@param visibleEntries: number of Entries that should be visible
				@param parent: a node to set as parent of this node (optional)
				@param fontsize: the fontsize of the list entries (default: 15)
				@param selectColor: the color a selected entry should change to (default: FF0000)
				@param entryColor: the color of non-selected entries
				@param inputMethod: avg.MOUSE, avg.TOUCH etc. (default: avg.TOUCH)
				@param clickTime: amount of time an entry needs to be clicked to be selected [ms] (default: 1000)
				"""
				if hasattr(avg.DivNode, '__init__'):
					avg.DivNode.__init__(self, parent=parent, elementoutlinecolor='', mediadir='',pos=(0,0),size=(100,100))
				self.__fontsize = fontsize #list entry font size
				self.__inputMethod = inputMethod
				self.selectColor = selectColor #color to highlight the selected entry
				self.entryColor = entryColor #color of the other entries
				self.longClickTime = clickTime
				self.addList(stringlist) #create WordsNodes from list
				self.__entryHeight = self.getChild(0).height 
				self.__slideOffset = 0
				self.__selEntry = -1 #no entry selected at start
				self.__delSelEntry = -1
				if visibleEntries < 0:
					visibleEntries = 0
				if visibleEntries > self.getNumChildren():
					visibleEntries = self.getNumChildren()	
				self.__visEntries = visibleEntries #number of entries to display
				self.__top = 0 #first displayed entry 
				self.__captureHolder = None
				self.__held = False				
				self.height = self.__entryHeight*visibleEntries
				self.__updateVisible(0)
				
	def addList(self,list): #adds the items of a stringlist as WordsNodes to the list
		old = self.getNumChildren()
		for item in list:
			self.appendChild(avg.WordsNode(text=item,fontsize=self.__fontsize,opacity=1))
			for x in range(old,self.getNumChildren()):
				self.getChild(x).setEventHandler(avg.CURSORDOWN, self.__inputMethod, self.__click)
				self.getChild(x).setEventHandler(avg.CURSORMOTION, self.__inputMethod, self.__slide)
				self.getChild(x).setEventHandler(avg.CURSORUP, self.__inputMethod, self.__release)
				if self.getChild(x).getMediaSize()[0] > self.width:
					self.width = self.getChild(x).getMediaSize()[0]
	
	def clear(self): #removes the WordNodes
		for x in range (0,self.getNumChildren()):
			self.removeChild(x)
		self.__visEntries = 0			
			
	def delayedSelection(self):
		#long click selection requires the lmb to remain pressed and the entry to be visible
		if self.__held and self.__delSelIndex >= self.__top and self.__delSelIndex < self.__top+self.__visEntries:
			self.selectEntry(self.__delSelIndex)
	
	def selectEntry (self,index,click=False):
		same = index == self.__selEntry
		if index >= 0 and index <= self.getNumChildren():
			if self.__selEntry <> -1:
				self.getChild(self.__selEntry).variant = ''
				self.getChild(self.__selEntry).color = self.entryColor
				self.__selEntry = -1
			if not same:		
				self.__selEntry = index
				self.getChild(index).variant = 'bold'
				self.getChild(index).color = self.selectColor
			
	def getSelectedEntry (self):
		return self.getChild(self.__selEntry).text
		
	def update(self, list): #removes the old list and displays the new one
		self.clear()
		self.addList(list)
		self.__selEntry = -1
		self.__updateVisible(0)
		
	def __updateVisible(self,index): #updates the displayed list
		if index < 0:
			index = 0
		if self.getNumChildren() - index < self.__visEntries:
			index = self.getNumChildren() - self.__visEntries
		x = 0
		while x < index:
			self.getChild(x).active = False
			x += 1
		x = index
		while x <= index+self.__visEntries-1:
			self.getChild(x).active = True
			self.getChild(x).y = (x-index)*self.__entryHeight
			x += 1
		while x < self.getNumChildren():
			self.getChild(x).active = False
			x += 1
		self.__top = index
			
	def __click(self, event):
		if self.__captureHolder is None:
			self.__captureHolder = event.cursorid
			self.__slideOffset = event.pos.y
			event.node.setEventCapture(event.cursorid)
			player = avg.Player.get()
			self.__delSelIndex = self.indexOf(event.node)
			self.__held = True
			player.setTimeout(self.longClickTime,self.delayedSelection)
			
	def __slide(self, event):
		if event.cursorid == self.__captureHolder:
			if self.__slideOffset <> 0:
				slidedist = event.pos.y - self.__slideOffset
				index = int(self.__top + slidedist/self.__entryHeight)
				self.__updateVisible(index)
			
	def __release(self, event):
		if event.cursorid == self.__captureHolder:	
			self.__slideOffset = 0
			event.node.releaseEventCapture(event.cursorid)
			self.__captureHolder = None
		self.__held = False