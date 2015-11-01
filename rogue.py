'''
	Rogue-like game
		Kill enemies; chance to hit, 
		Consume potion from quick bar
		Inventory
		Character equip from ground
		Trade with vendors
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
			 		 

		# Key input needs to be in another thread, bcs waiting for prog to get out of nap
		if stdscr.getch() == ord('w'):
			fireEngines = True
		if stdscr.getch() == ord('s'):
			fireEngines = False
		if stdscr.getch() == ord('r'):
			if speed > 50:
				speed -= 100
		if stdscr.getch() == ord('f'):
			if speed < 500:
				speed += 100

	oriWin = gameWindow( winDivide, int(curses.LINES/3), int(curses.LINES/3), 40)
	oriWin.makeWin( curses.newwin( oriWin.height, oriWin.width, oriWin.yTop, oriWin.xTop))

	ammoStatusWin = gameWindow( winDivide, int(curses.LINES/3)*2, int(curses.LINES/3), 40)
	ammoStatusWin.makeWin( curses.newwin( ammoStatusWin.height, ammoStatusWin.width, ammoStatusWin.yTop, ammoStatusWin.xTop))

'''
	



import random
from math import sin
from math import cos
from math import radians
import curses	# curses lib
from curses import wrapper

random.seed()	# seed with current system time
mainWindef = { 'xTop' : 0, 'yTop' : 0, 'height' : 1, 'width' : 1, 'mainWin' : 0 }  

class player(object):
	def __init__(self, x, y, hp):
		self.xPos = x
		self.yPos = y
		self.hitPoints = hp
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
	stdscr = curses.initscr()	# init curses, return a window obj
	curses.start_color()		# init default colour set, wrapper should have done this
	stdscr.clearok(1)		# makes next call to refresh clear the window as well
	hudXPos = curses.COLS - 40	# x pos of HUDs to draw

	# setup main window where stuff coming at player is drawn, fire into mid of screen
	mainWin = gameWindow( 0, 0, curses.LINES, hudXPos)
	mainWin.makeWin( curses.newwin( mainWin.height, mainWin.width, mainWin.yTop, mainWin.xTop))

	# set HUD windows
	statsWin = gameWindow( hudXPos, 0, int(curses.LINES/3), 40)
	statsWin.makeWin( curses.newwin( statsWin.height, statsWin.width, statsWin.yTop, statsWin.xTop))

	# Set some properties
	curses.noecho()			# do not output inputted char to screen
	curses.cbreak()			# dont wait for 'enter' pressed to respond to input
	curses.curs_set(False)		# no blinking cursor
	stdscr.keypad(True)		# allows recog of LEY_LEFT, PAGE_UP
	stdscr.nodelay(True)		# make getch(), and getKey non block
	strr = "fffff"

	while( (stdscr.getch() != ord('q')) and (stdscr.getch != curses.KEY_EXIT) ):
#		Clear screen so to draw next frame; future performance; draw only whats req
		mainWin.winObj.erase()

		mainWin.winObj.addch(int(curses.LINES/2), int(curses.COLS/2), ord('*'), curses.A_STANDOUT)
		mainWin.winObj.addch(10, 10, ord('t'))
#		statsWin.winObj.addnstr(y, x, str, n[, attr])
		statsWin.winObj.addnstr(1, 1, "playerName", 10)
				


		mainWin.winObj.border('x','x','x','x','*','*','*','*')	# ls, rs, ts, bs, tl, tr, bl, br	
#		mainWin.winObj.box(1, 160)
		statsWin.winObj.border('x','x','x','x','*','*','*','*')	# ls, rs, ts, bs, tl, tr, bl, br	
#		oriWin.winObj.border('x','x','x','x','*','*','*','*')	# ls, rs, ts, bs, tl, tr, bl, br	
#		ammoStatusWin.winObj.border('x','x','x','x','*','*','*','*')	# ls, rs, ts, bs, tl, tr, bl, br	

#		mainWin.winObj.addch(10, 10, ord('*'))

		mainWin.winObj.refresh()
		statsWin.winObj.refresh()
#		oriWin.winObj.refresh()
#		ammoStatusWin.winObj.refresh()
		stdscr.refresh()
		curses.napms(100);		# draw every second

	curses.endwin()			# deinit curses,& return terminal to previous state;echo,cbreak,keypad
wrapper(main)			# wrapper ensures that terminal is returned to its org state, incase main fails to restore state
  		
