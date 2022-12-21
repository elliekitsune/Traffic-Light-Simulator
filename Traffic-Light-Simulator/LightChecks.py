
import time
from enum import Enum

gameRunning = False

beginningtimemillis = None
checktimemillis = None
totaltimemillis = None

currentSetSignalTime = None
turnSignal = 7
straightSignal = 3
stopSlowSignal = 1

pole = None
section = None
light = None
state = None

lightlist = [#   red,  yellow,    green lights              
					[          #POLE NORTH
					 [1,0,0],     #NORTH left turn
					 [1,0,0],     #NORTH middle straight
					 [1,0,0]      #NORTH right straight
					],
					
					[          #POLE EAST
					 [1,0,0],     #EAST left turn
					 [0,0,1],     #EAST middle straight
					 [0,0,1]      #EAST right straight
					],
					
					[          #POLE SOUTH
					 [1,0,0],     #SOUTH left turn
					 [1,0,0],     #SOUTH middle straight
					 [1,0,0]     #SOUTH right straight
					],  
					
					[          #POLE WEST
					 [1,0,0],     #WEST left turn
					 [0,0,1],     #WEST middle straight
					 [0,0,1]      #WEST right straight
					], 
						
				]

class LightState(Enum):
	TURNGO       = 1
	TURNSLOW     = 2
	TURNSTOP     = 3
	STRAIGHTGO   = 4
	STRAIGHTSLOW = 5
	STRAIGHTSTOP = 6

def onStartTime():
	global beginningtimemillis
	beginningtimemillis = time.perf_counter()


def onCheckTime():
	if(beginningtimemillis != None and currentSetSignalTime != None):
		global checktimemillis
		global totaltimemillis
		checktimemillis = time.perf_counter()
		totaltimemillis = checktimemillis - beginningtimemillis

		print("Set Time: " + str(currentSetSignalTime))
		print("start time: " + str(beginningtimemillis))
		print("time now: " + str(checktimemillis))
		print("Time since start time: " + str(totaltimemillis))
		if(totaltimemillis >= currentSetSignalTime):
			return True
		else:
			return False
	elif(beginningtimemillis == None):
		print("Beginning time not set")
	elif(currentSetSignalTime == None):
		print("Signal time not set")

def getBeginningTime():
	if(beginningtimemillis == None):
		return None
	return beginningtimemillis

def getCurrentTime():
	if(checktimemillis == None):
		return None
	return checktimemillis

def getTotalCurrentTime():
	if(totaltimemillis == None):
		return None
	return totaltimemillis

def getSetTime():
	if(currentSetSignalTime == None):
		return None
	return currentSetSignalTime

def setCurrentSignalTime(settime):
	global currentSetSignalTime
	currentSetSignalTime = settime

def isGameRunning():
	return gameRunning

def setGameRunning(running):
	global gameRunning
	gameRunning = running

def getLightSection():
	return section

def setLightSection(sect):
	global section
	section = sect

def getLightPole():
	return pole

def setLightPole(pol):
	global pole
	pole = pol

def getLightState():
	return state

def setLightState(stat):
	global state
	state = stat

def getLightList():
	return lightlist

def getLightList(lightpole):
	return lightlist[lightpole]

#def getLightList(lightpole, lightsection, trafficlight):
	#return lightlist[lightpole][lightsection][trafficlight]

def setLightList(lightpole, lightsection, trafficlight, value):
	global lightlist
	lightlist[lightpole][lightsection][trafficlight] = value

def setLightState(xpole, xstate):
	global state

	#make sure there is a street to refer to
	if(xstate != None):
		state = xstate
		setLightPole(xpole)

		poles = [None] * 2

		if(xpole == 1 or xpole == 3):
			poles[0] = 0
			poles[1] = 2
		elif(xpole == 2 or xpole == 4):
			poles[0] = 1
			poles[1] = 3


		#check if the lights are the straight lights or the turn signal lights to handle them differently
		if(state.value > 0 and state.value < 4):
			onTurn(poles, 0, state)

		elif(state.value > 3 and state.value < 7):
			onStraight(poles, 1, state)
		else:
			print("Not enough lights for value")

def onTurn(p, signal, light):     
	clearTrafficLights()

	print("[" + str(p) + "][" + str(signal) + "][" + str(light.value - 1) + "]")

	setLightList(p[0], signal, light.value, 1)
	setLightList(p[1], signal, light.value, 1)

def onStraight(p, section, light):
	clearTrafficLights()

	print("[" + str(p) + "][" + str(section) + "][" + str(light.value - 1) + "]")

	#get first selected pole with 3 sections (left, straight left, and straight right) and 6 different states that lights can go through and set to on
	setLightList(p[0], section    , light.value - 4, 1)
	setLightList(p[0], section + 1, light.value - 4, 1)

	setLightList(p[1], section    , light.value - 4, 1)
	setLightList(p[1], section + 1, light.value - 4, 1)
	
def clearTrafficLights():
	global lightlist

	#go through each light one by one and set to 0. Am realizing is probably slow. Will change possibly later
	for v in range(0, len(lightlist)):
		print("range of poles" + str(len(lightlist)))
		for w in range(0, len(lightlist[v])):
			print("range of sections" + str(len(lightlist[v])))
			for x in range(0, len(lightlist[v][w])):
				print("range of lights" + str(len(lightlist[v][w])))
				lightlist[v][w][x] = 0

#sets up all the variables for the lights before the simulator starts running
def startTrafficLights():
	setLightState(1, LightState.TURNGO) #Start signal on pole saying to turn left
	setCurrentSignalTime(turnSignal) #set time for how long the lights stay in a state before changing
	setGameRunning(True) #Start simulator after initial settings set

#run this everytime in the game loop to check how much time has went by and switch to the next state and pole and start a new timer
def checkTrafficLights():
	if(onCheckTime()):

		if(pole == 4):
			setLightPole(1)
		elif(pole > 0 and pole < 4):
			setLightPole( pole + 1)

		if(state.value == 6): #if state 
			setLightState(pole, LightState.TURNGO)
		else:
			setLightState(pole, LightState(state.value))

		setNextSignal()
		onStartTime()


def setNextSignal():
	print("Next Signal time being set and Light state")
	if(state == LightState.STRAIGHTSLOW or 
		state == LightState.STRAIGHTSTOP or 
		state == LightState.TURNSTOP     or
		state == LightState.TURNSLOW):
		setCurrentSignalTime(stopSlowSignal)

	elif(state == LightState.TURNGO):
		setCurrentSignalTime(turnSignal)

	elif(state == LightState.STRAIGHTGO):
		setCurrentSignalTime(straightSignal)

	else:
		print("Error in next signal switch")