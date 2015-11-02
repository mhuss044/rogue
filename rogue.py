'''
	Rogue-like game
		Kill enemies; chance to hit, 
		Consume potion from quick bar
		Inventory
		Character equip from ground
		Trade with vendors

		on die anim; circle of chars animated draw
			then chars with deg same rotate colour from 1-7
'''
'''

	fireEngines = False		# press w to engage warp
	speed = 500			# ms to wait before screen update
	engineRad = [0, 5, 15, 25, 35]	# radius of rings, for warp effect
	stars = []		# when not in warp, draw stary bkg 

	# This raises ZeroDivisionError when i == 10.
	for i in range(0, 11):
	    v = i-10
		    stdscr.addstr(i, 0, '10 divided by {} is {}'.format(v, 10/v))
	if curses.can_change_color():
		print "Can use colour"
	elif curses.can_change_color():
	 	print "c"
	else:
	 	print "cc"

	# gen rand star pos
	for i in range(0, 100):		# makes a list; 0 - 99
		stars.append(random.randint(1, winDivide - 1))
	for i in range(1, 100, 2):	# change every 2nd # to a y coord
		stars[i] = random.randint(1, curses.LINES - 1)
#		Draw bkg;
		if fireEngines:		# draw warp effect
			for i in range(0, 5):
				for ang in range(0, 360):
					x = int(mainWin.width/2 + engineRad[i]*cos(radians(ang)))
					y = int(mainWin.height/2 + engineRad[i]*sin(radians(ang)))
					if x > 0 and x < mainWin.width:
						if y > 0 and y < mainWin.height:
							mainWin.winObj.addch(y, x, ord('*'))
				if engineRad[i] < 80:		# 80 max radius of ring
					engineRad[i] += 5
				else:
					engineRad[i] = 0
		else:		# draw reqgular move effect
			for i in range(0, 100, 2):	# returns 0 to 99
				if stars[i] < (winDivide - 2):
					stars[i] = int(stars[i]*1.1)
				else:
				 	stars[i] = random.randint(1, winDivide - 2)		# - 2 so that ch and cursor 2 and 1 away from edge
				if stars[i + 1] < (curses.LINES -1): 
					stars[i + 1] = int(stars[i + 1]*1.1)
				else:
				 	stars[i + 1] = random.randint(1, curses.LINES - 2)
				try: mainWin.winObj.addch(stars[i+1], stars[i], ord('*'))		# Place star		
				# or:
				# addch will fail if try to place ch outside of window bounds, and if ch placed leaves cursor out of bounds.
				except curses.error: pass		# curses.error is an exception raised
				     					# pass does nothing, only placed if syntax requires a statement
			 		 

	ammoStatusWin = gameWindow( winDivide, int(curses.LINES/3)*2, int(curses.LINES/3), 40)
	ammoStatusWin.makeWin( curses.newwin( ammoStatusWin.height, ammoStatusWin.width, ammoStatusWin.yTop, ammoStatusWin.xTop))

'''
	



import random
from math import sin
from math import cos
from math import radians
import curses	# curses lib
from curses import wrapper
from curses.textpad import Textbox

random.seed()	# seed with current system time
mainWindef = { 'xTop' : 0, 'yTop' : 0, 'height' : 1, 'width' : 1, 'mainWin' : 0 }  

class gameInfo(object):
	def __init__(self, state, x):
		self.enemies = []
		self.curLevel = 0
		self.gameState = state		# true; playing game, false; game over; title screen 
		self.maxX = x
	def setmaxLvl(self, lvl):
		self.maxLevels = lvl
	def advLvl():
		if(self.curLevel < self.maxLevels):
			self.curLevel += 1;
		else:
			self.curLevel = 0
	def startNewGame(self):
		self.curLevel = 0
		self.gameState = True

#		Setup enemies
		for i in range(0, 20):		# set x = y = 2
			self.enemies.append(2)
		for i in range(0, 20, 2):	# set x to rand in
			self.enemies[i-1] = random.randint(1, self.maxX)

	def gameOver(self):
		self.curLevel = 0
		self.gameState = False

class player(object):
	def __init__(self, x, y, hp, pName):
		self.xPos = x
		self.yPos = y
		self.hitPoints = hp
		self.playerName = pName 
	def setName(self, pName):
		self.playerName = pName
	def takeDamage(self, dmg):
		if(self.hitPoints > dmg):
			self.hitPoints -= dmg
		else:
			self.hitPoints = 0

class gameWindow(object):
	def __init__(self, xT, yT, h, w):
		self.xTop = xT
		self.yTop = yT
		self.height = h
		self.width = w
	def makeWin(self, wObj):
		self.winObj = wObj
	def changeDim(self, xT, yT, h, w):
		self.xTop = xT
		self.yTop = yT
		self.height = h
		self.width = w
#		return true
	
def main(stdscr):
	startAnim = True
	stdscr = curses.initscr()	# init curses, return a window obj
	curses.start_color()		# init default colour set, wrapper should have done this
	stdscr.clearok(1)		# makes next call to refresh clear the window as well
	hudXPos = curses.COLS - 40	# x pos of HUDs to draw

	newGame = gameInfo(False, curses.COLS - 40)	# false; goto title screen, num levels to pass
	newPlayer = player( int(curses.COLS/2), curses.LINES - 2, 100, "New Player")

	# setup main window where stuff coming at player is drawn, fire into mid of screen
	mainWin = gameWindow( 0, 0, curses.LINES, hudXPos)
	mainWin.makeWin( curses.newwin( mainWin.height, mainWin.width, mainWin.yTop, mainWin.xTop))

	titleScreen = gameWindow( 0, 0, curses.LINES, curses.COLS)
	titleScreen.makeWin( curses.newwin( titleScreen.height, titleScreen.width, titleScreen.yTop, titleScreen.xTop))

	editwin = curses.newwin( 3, 12, int(titleScreen.height/2), int(titleScreen.width/2))	# edit box with height 3, w 12, mid screen
	box = Textbox(editwin)

	# set HUD windows
	statsWin = gameWindow( hudXPos, 0, int(curses.LINES/3), 40)
	statsWin.makeWin( curses.newwin( statsWin.height, statsWin.width, statsWin.yTop, statsWin.xTop))

	mapWin = gameWindow( hudXPos, int(curses.LINES/3), int(curses.LINES/3), 40)
	mapWin.makeWin( curses.newwin( mapWin.height, mapWin.width, mapWin.yTop, mapWin.xTop))


	# Set some properties
	curses.noecho()			# do not output inputted char to screen
	curses.cbreak()			# dont wait for 'enter' pressed to respond to input
	curses.curs_set(False)		# no blinking cursor
	stdscr.keypad(True)		# allows recog of LEY_LEFT, PAGE_UP
	stdscr.nodelay(True)		# make getch(), and getKey non block

# 	Define colours; for some reason, they arent defined already, access to 0 - 7
	curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)	# colorID to change, forground, background
	curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)	# colorID to change, forground, background
	curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK)	# colorID to change, forground, background
	curses.init_pair(4, curses.COLOR_BLUE, curses.COLOR_BLACK)	# colorID to change, forground, background
	curses.init_pair(5, curses.COLOR_MAGENTA, curses.COLOR_BLACK)	# colorID to change, forground, background
	curses.init_pair(6, curses.COLOR_CYAN, curses.COLOR_BLACK)	# colorID to change, forground, background
	curses.init_pair(7, curses.COLOR_WHITE, curses.COLOR_BLACK)	# colorID to change, forground, background

#	Set bkg to black
	mainWin.winObj.bkgd(' ', curses.color_pair(0))

	var = 1
	x = 1
	y = 1
	rows = 20
	toadd = 0.1

	while( (stdscr.getch() != ord('q')) and (stdscr.getch != curses.KEY_EXIT) ):
		if(newGame.gameState):
			if startAnim:
				titleScreen.winObj.erase()
				if rows < 120:
					rows += 2
				else:
					rows = 20
				for r in range(1, rows):
					for ang in range(0, 360):
						x = int(titleScreen.width/2 + r*cos(radians(ang)))
						y = int(titleScreen.height/2 + r*sin(radians(ang)))
						if titleScreen.winObj.enclose(y, x):	# check that provided coords are in window, so no error`
							titleScreen.winObj.addch(y, x, ord('@'), curses.color_pair(var))
					if var < 7:
						var += 1
					else:
						var = 1

				titleScreen.winObj.addnstr(int(titleScreen.height/2), int(titleScreen.width/2), "Get ready for Fun game!!!", 40, curses.color_pair(4))
				titleScreen.winObj.addnstr(int(titleScreen.height/2)+1, int(titleScreen.width/2), "Press t to start!", 40, curses.color_pair(4))

				if stdscr.getch() == ord('t'):
					startAnim = not startAnim


				titleScreen.winObj.border()	# use default lines, and corners	
				titleScreen.winObj.refresh()
				stdscr.refresh()


			else:
	#			Clear screen so to draw next frame; future performance; draw only whats req
				mainWin.winObj.erase()

#				Draw player:
				if mainWin.winObj.enclose(newPlayer.yPos, newPlayer.xPos):	# check that provided coords are in window, so no error`
					mainWin.winObj.addch(newPlayer.yPos, newPlayer.xPos, ord('@'), curses.A_STANDOUT)
#				Draw Enemies:
				for i in range(1, 20, 2): 
					if mainWin.winObj.enclose( newGame.enemies[i], newGame.enemies[i-1]):
						mainWin.winObj.addch(newGame.enemies[i], newGame.enemies[i-1], ord('e'))
				for i in range(1, 20, 2): 
					if(newGame.enemies[i] + 2 < curses.LINES - 1):
						toadd += 0.0001
						newGame.enemies[i] += int(toadd)
					else:
						startAnim = not startAnim
#				statsWin.winObj.addnstr(y, x, str, n[, attr])
				statsWin.winObj.addnstr(1, 1, newPlayer.playerName, 10, curses.color_pair(4))
				statsWin.winObj.addnstr(2, 1, "Health:"+str(newPlayer.hitPoints), 20, curses.color_pair(4))
				statsWin.winObj.addnstr(3, 1, "Damage:", 10, curses.color_pair(4))

						
				mapWin.winObj.addnstr(1, 1, "Map", 10, curses.color_pair(5))
				mapWin.winObj.vline(1, int(mapWin.width/2), '=', int(mapWin.height - 2))


		#		mainWin.winObj.border('x','x','x','x','*','*','*','*')	# ls, rs, ts, bs, tl, tr, bl, br	
				mainWin.winObj.border()	# use default lines, and corners	
#				mainWin.winObj.box(1, 160)
				statsWin.winObj.border('x','x','x','x','*','*','*','*')	# ls, rs, ts, bs, tl, tr, bl, br	
				mapWin.winObj.border('x','x','x','x','*','*','*','*')	# ls, rs, ts, bs, tl, tr, bl, br	
#				ammoStatusWin.winObj.border('x','x','x','x','*','*','*','*')	# ls, rs, ts, bs, tl, tr, bl, br	

# 				Key input needs to be in another thread, bcs waiting for prog to get out of nap
				if stdscr.getch() == ord('a'):
					if newPlayer.xPos > 0:
						newPlayer.xPos -= 10
				if stdscr.getch() == ord('d'):
					if newPlayer.xPos < hudXPos:
						newPlayer.xPos += 10
				if stdscr.getch() == ord('w'):
					if newPlayer.yPos > 0:
						newPlayer.yPos -= 10
					else:
						newGame.advLvl()
				if stdscr.getch() == ord('s'):
					if newPlayer.yPos < curses.LINES - 1:
						newPlayer.yPos += 10
				if stdscr.getch() == ord('t'):
					startAnim = not startAnim

				# Collision detect, if x = x, y = y

				mainWin.winObj.refresh()
				statsWin.winObj.refresh()
				mapWin.winObj.refresh()
				stdscr.refresh()
				curses.napms(100);		# draw every second
				
		else:	# Draw title screen
			titleScreen.winObj.addnstr(1, 1, "Enter your name: ", 30, curses.color_pair(5))
			titleScreen.winObj.addnstr(2, 1, "Press Ctrl-G when done.", 30, curses.color_pair(5))
			titleScreen.winObj.border()	# use default lines, and corners	
			titleScreen.winObj.refresh()

#			User edits until press ctrl-g:
			box.edit()
			newPlayer.setName(box.gather())
			newGame.startNewGame()
	
#			done enter name, set max level
			titleScreen.winObj.border()	# use default lines, and corners	
			titleScreen.winObj.refresh()
			stdscr.refresh()

		curses.napms(100);		# draw every second
	curses.endwin()			# deinit curses,& return terminal to previous state;echo,cbreak,keypad
wrapper(main)			# wrapper ensures that terminal is returned to its org state, incase main fails to restore state
  		
