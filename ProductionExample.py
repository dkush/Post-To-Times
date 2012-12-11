#!/usr/bin/python

#get access to pyepl stuff and other modules
import random
import sys
from pyepl.locals import *

#####################################################
def readItems(filename): 
  """
	This function reads in the items from the list file specified.
	"""                               
	items1 = open(filename,'r')
	items = [line.split(",") for line in items1]                    
	for line in items:                              
		line[2] = line[2].rstrip()   
	items1.close()               
	return items                                    

def presentTxt(txt):
	"""
	This function collapses loading text and presenting it into one.
	"""
    stim = Text(txt,size=.024)
    ts = stim.present(clk=clk,duration=15000,bc=bc)
    return ts

def doInstruct(filename):
	"""
	Collapses series of instruction functions into one
	"""
    instructions = open(filename)
    instruct(instructions.read(),clk = clk,size=.05)
    instructions.close()

def pseudoRandomize(origList,conds,fillername):
	"""
	Pseudorandomizes order of test and filler items such that test items do not appear consecutively. 
	Obviously #Fillers must be > #Test.
	'origList' is the name of the items file.
	Argument 'fillername' is a string, which should be the condition name for fillers in your items list.
	'conds' is a list containing all the condition names in your experiment.
	"""
	items = readItems(origList)
	random.shuffle(items)
	doubleFills = []
	doubleTest = []
	output = []
	#find instances of two test items next to one another
	for ind in range(0,len(items)-1):
		if items[ind][1] in conds and items[ind+1][1] in conds:
				doubleTest.append(items[ind])
				origList.remove(items[ind])
	#find instances of two fillers next to one another
	for ind in range(0,len(items)-1):
		if items[ind][1] == fillername and items[ind+1][1] == fillername:
			doubleFills.append(ind)
	random.shuffle(doubleFills)
	for item in doubleTest:
		origList.insert(doubleFills[0]+1,item)
		doubleFills.remove(0)


def instructions():
	doInstruct("instruct.txt")
	doInstruct("instructformat.txt")
	waitForAnyKey(clk, Text("Here's an example in the format that you'd get it.", size=.05))
	stim = FileAudioClip("foxhuntcut.wav")
	ts = stim.present(clk=clk)
	clk.delay(2000)
	stim = FileAudioClip("example.wav")
	ts = stim.present(clk=clk)
	waitForAnyKey(clk, Text("Here's one for you to practice with."))
	stim = FileAudioClip("ghostscut.wav")
	ts = stim.present(clk=clk)
	clk.delay(3000)
	waitForAnyKey(clk, Text("Was your response something like this?:"))
	stim = FileAudioClip("ghostscomplete.wav")
	ts = stim.present(clk=clk)
	waitForAnyKey(clk, Text("Great. One more:"))
	stim = FileAudioClip("margaretcut.wav")
	ts = stim.present(clk=clk)
	clk.delay(3000)
	waitForAnyKey(clk, Text("Was your response something like?:"))
	stim = FileAudioClip("margaretcomplete.wav")
	ts = stim.present(clk=clk)
	waitForKeySeq("startexp.txt")

######### Change These Values ##################

conds = ["COND1","COND2",'COND3',"COND4"]
fillName = "FILLER"
itemFile = 'itemsshort.txt'

#####################################################


# This bit takes in the items from the file and 
# pseudorandomizes their order
#items = readItems('itemsshort.txt')
#random.shuffle(items)
pseudoRandomize(itemFile,conds,fillname)

################# Objects that we need
exp = Experiment() # You can change the resolution of the screen by passing an argument like "resolution=(1920,1080)" to Experiment()
vt = VideoTrack("video")
at = AudioTrack("audio")
kt = KeyTrack("key")
log = LogTrack("session")
clk = PresentationClock()
bc = ButtonChooser(Key("R"),Key("U")) # Change to whichever buttons you'd like.
exp.setBreak()
itemNo = 0

# Clear the Screen
vt.clear("black")

#instructions and examples go here.



# Run Trials##############

# loop through items in items file
while itemNo <= len(items)-1:
	
	# log the start of a trial 
	log.logMessage('%s\t%s\t%d' % (items[itemNo][0],items[itemNo][1],itemNo+1))
	
	#display cross to signal trial start
	waitForAnyKey(clk, Text("+", size = .2))
	
	#load test sentence from current item and present it. 
	stim = FileAudioClip(items[itemNo][2])
	ts = stim.present(clk=clk)
	clk.wait()
	
	#display prompt for repetition or recording
	vt.show(Text("Press R to repeat or U to respond."),.5,.5)
	vt.updateScreen()
	b = bc.wait()
	
	# repeat if "R" pressed
	if b==Key("R"):
		while b==Key("R"):
			ts = stim.present(clk=clk)
			log.logMessage('%s\t%s\t%d' % ('REPEAT',items[itemNo][1],itemNo+1))
			b = bc.wait()
			
	#begin recording if "U" pressed		
	if b == Key("U"):
		vt.clear("black")
		vt.show(Text("... recording ..."),.5,.5)
		vt.updateScreen()
		#record for 8 sec, save file to directory with name of cond,item
		recClip,tsRec = at.record(duration=8000,t=clk,basename="Response"+str(items[itemNo][0])+str(items[itemNo][1]))
		clk.wait()
	
	#wait for end
	clk.wait()
	vt.clear("black")
	
	#increment item counter
	itemNo+=1

doInstruct("endtext.txt")






