# Auto-solvers for the 2048 game

import time
import bs4
import re
import random
import os

os.chdir(r'C:\IdeasLiberty\2048')

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary

binary = FirefoxBinary('C:\Program Files (x86)\Mozilla Firefox\Firefox.exe')
browser = webdriver.Firefox(firefox_binary=binary)

browser.get('https://gabrielecirulli.github.io/2048/')

time.sleep(2)

htmlElem = browser.find_element_by_class_name('title')

moves4 = [Keys.UP, Keys.RIGHT,Keys.DOWN,Keys.LEFT]
moves3 = [Keys.UP, Keys.RIGHT,Keys.LEFT]
moves2 = [Keys.RIGHT,Keys.LEFT]

pattern = re.compile(r'''
                     tile\stile\-
                     (\d+)
                     \stile\-position\-
                     (\d)\-(\d)
                     \s?(tile\-(new|merged))?
                     ''', re.VERBOSE)

methods = ["Random", "TopRandom", "TopCircle", "Circle","FirstWin"]

def maxGrid(grid): # Calculates the maximum value of the grid
    maximum = []
    for row in grid:
        maximum.append(max(row))
    return max(maximum)
    
def gridInfo(): # Returns the 4x4 data of the current grid, the maximum value and the sum of the grid
    soup = bs4.BeautifulSoup(browser.page_source)
    cont = str(soup.select('.tile-container')[0])
    grid = pattern.findall(cont)
    currentGrid = [[0 for x in range(4)] for y in range(4)]
    gridSum = 0
    for i in reversed(grid):
        if currentGrid[int(i[2])-1][int(i[1])-1] ==0:
            gridSum += int(i[0])
            currentGrid[int(i[2])-1][int(i[1])-1] = int(i[0])
    return currentGrid, maxGrid(currentGrid), gridSum

def restart(method): # Check whether game needs to restart
    global which, score, maxTile, maximum, solveTime, stallNumber
    if solveTime == 0:
        solveTime = time.time()
    try:
        tryagainElem = browser.find_element_by_class_name('retry-button')
        if int(browser.find_element_by_class_name('score-container').text) < score: # This means that the score has reset and the game has ended
		
            print (str(which) + "," + str(score) + "," + str(maxTile) + "," + str(int(time.time() - solveTime))+"," + str(stallNumber))
            file = open("%s method 2048.txt" % method,"a")
            file.write(str(which) + "," + str(score) + "," + str(maxTile)+","+str(int(time.time() - solveTime)) + \
            "," + str(stallNumber) + "\n")
            file.close()
            which += 1
            stallNumber = 0
            solveTime = time.time()
			
        # When game ends the program will come here and the score will be some value,
        # Marks the value, next iteration it comes here and nulifies
        score = int(browser.find_element_by_class_name('score-container').text) 
        maxTile = maximum
        tryagainElem.click()
    except:
        pass

def printGrid(currentGrid): # Prints the current grid
    for x in currentGrid: 
        for i in x:
            print(str(i).rjust(2), end = " ")
        print("")

def checkStall(): # Checks if movement is stuck and needs to send Down key
    global gridSum, previousSum, timeKeep, startTime, stallNumber
    
    if gridSum == previousSum: # Check when status does not change
        if (time.time() - startTime > 0 and startTime !=0):
            timeKeep+= time.time()-startTime
        startTime = time.time()
        if timeKeep > 2: # If status does not change for 2 seconds - send Down/Up keys
            htmlElem.send_keys(Keys.DOWN)
            htmlElem.send_keys(Keys.UP)
            stallNumber +=1
            timeKeep = 0
    else:
        timeKeep = 0
        startTime = 0
    previousSum = gridSum 

def methodRandom():
    htmlElem.send_keys(random.choice(moves4))

def methodTopRandom():
    checkStall()
    htmlElem.send_keys(random.choice(moves3))

def methodTopCircle():
    checkStall()
    htmlElem.send_keys(Keys.UP)
    htmlElem.send_keys(Keys.RIGHT)
    htmlElem.send_keys(Keys.UP)
    htmlElem.send_keys(Keys.LEFT)
    
def methodCircle():
    htmlElem.send_keys(Keys.UP)
    htmlElem.send_keys(Keys.RIGHT)
    htmlElem.send_keys(Keys.DOWN)
    htmlElem.send_keys(Keys.LEFT)
    
def methodFirstWin():
    checkStall()
    
    if (cg[0][1] == maximum and cg[0][0] == 0): # Get maxTile to top corners
        htmlElem.send_keys(Keys.LEFT)
    elif (cg[0][2] == maximum and cg[0][3] == 0):
        htmlElem.send_keys(Keys.RIGHT)
        
    elif(cg[0][1] == maximum and cg[0][0] != 0 and cg[0][2] == 0 and cg[0][3]==0):
        htmlElem.send_keys(Keys.RIGHT)
        
    elif(cg[0][2] == maximum and cg[0][3] != 0 and cg[0][1] == 0 and cg[0][0]==0):
        htmlElem.send_keys(Keys.LEFT)
    
        # Fill first row if max is in corners
    elif (cg[0][0] == maximum or cg[0][3] == maximum) and \
        ((cg[0][0]==0 and (cg[1][0] != 0 or cg[2][0] != 0 or cg[3][0] != 0)) or \
         (cg[0][1] ==0 and (cg[1][1] != 0 or cg[2][1] != 0 or cg[3][1] != 0)) or \
          (cg[0][2] ==0 and (cg[1][2] != 0 or cg[2][2] != 0 or cg[3][2] != 0)) or \
           (cg[0][3] == 0 and (cg[1][3] != 0 or cg[2][3] != 0 or cg[3][3] != 0))):
        htmlElem.send_keys(Keys.UP)
        
    elif (cg[0][0] !=0 and cg[0][0]==cg[0][1]) or \
        (cg[0][0] !=0 and cg[0][0]==cg[0][2] and cg[0][1] == 0):
        htmlElem.send_keys(Keys.LEFT) # Match top row left

    elif (cg[0][3] !=0 and cg[0][3]==cg[0][2]) or \
        (cg[0][3] !=0 and cg[0][3]==cg[0][1] and cg[0][2] == 0):
        htmlElem.send_keys(Keys.RIGHT) # Match top row right
        
    elif (cg[0][0] !=0 and cg[0][0]==cg[0][3] and cg[0][1] == 0 and cg[0][2] == 0):
        htmlElem.send_keys(random.choice(moves2)) # Match top row corners
    
    elif (cg[0][1]!=0 and cg[0][1]==cg[0][2] and cg[0][0]==0): #Match top row center
        htmlElem.send_keys(Keys.LEFT)
    elif (cg[0][1]!=0 and cg[0][1]==cg[0][2] and cg[0][3]==0):
            htmlElem.send_keys(Keys.RIGHT)
            
    # Between lines match
    elif ((cg[0][0] != 0) and (cg[0][0]==cg[1][0])) or \
    ((cg[0][1] != 0) and (cg[0][1]==cg[1][1])) or \
    ((cg[0][2] != 0) and (cg[0][2]==cg[1][2])) or \
    ((cg[0][3] != 0) and (cg[0][3]==cg[1][3])) or \
    ((cg[1][0] != 0) and (cg[1][0]==cg[2][0])) or \
    ((cg[1][1] != 0) and (cg[1][1]==cg[2][1])) or \
    ((cg[1][2] != 0) and (cg[1][2]==cg[2][2])) or \
    ((cg[1][3] != 0) and (cg[1][3]==cg[2][3])) or \
    ((cg[2][0] != 0) and (cg[2][0]==cg[3][0])) or \
    ((cg[2][1] != 0) and (cg[2][1]==cg[3][1])) or \
    ((cg[2][2] != 0) and (cg[2][2]==cg[3][2])) or \
    ((cg[2][3] != 0) and (cg[2][3]==cg[3][3])) or \
    (cg[0][0]!= 0 and cg[0][0] == cg[2][0] and cg[1][0]==0) or \
    (cg[0][0]!= 0 and cg[0][0] == cg[3][0] and cg[1][0]==0 and cg[2][0]==0) or \
    (cg[0][1]!= 0 and cg[0][1] == cg[2][1] and cg[1][1]==0) or \
    (cg[0][1]!= 0 and cg[0][1] == cg[3][1] and cg[1][1]==0 and cg[2][1]==0) or\
    (cg[0][2]!= 0 and cg[0][2] == cg[2][2] and cg[1][2]==0) or \
    (cg[0][2]!= 0 and cg[0][2] == cg[3][2] and cg[1][2]==0 and cg[2][2]==0) or \
    (cg[0][3]!= 0 and cg[0][3] == cg[2][3] and cg[1][3]==0) or \
    (cg[0][3]!= 0 and cg[0][3] == cg[3][3] and cg[1][3]==0 and cg[2][3]==0):
        htmlElem.send_keys(Keys.UP)
        
    # Top left corner match
    elif (cg[0][0]!= 0 and cg[0][0] == cg[1][1] and cg[1][0] ==0): 
        htmlElem.send_keys(Keys.LEFT)
        htmlElem.send_keys(Keys.UP)
    
    # Top right corner match
    elif (cg[0][3]!= 0 and cg[0][3] == cg[1][2] and cg[1][3] ==0):
        htmlElem.send_keys(Keys.RIGHT)
        htmlElem.send_keys(Keys.UP)
    
	# 2nd line center match and check for doubling
    elif (cg[1][1]!=0 and cg[1][1]==cg[1][2]):
        if (cg[0][1] == int(cg[1][1]*2) and cg[1][0]!=0):
            htmlElem.send_keys(Keys.LEFT)
        elif (cg[0][2] == int(cg[1][2]*2) and cg[1][3] !=0):
            htmlElem.send_keys(Keys.RIGHT) 
        else:
            htmlElem.send_keys(random.choice(moves2))
	
	# 1st/2nd line 2/3 match
	
    elif (cg[1][2] !=0 and cg[1][2] == cg[0][1]) and \
        ((cg[0][0] == 0 and cg [1][0] == 0 and cg[1][1] == 0) or \
         (cg[0][0]!=0 and cg[1][0] !=0 and cg[1][1] == 0) or \
         (cg[0][0]!=0 and cg[1][1] !=0 and cg[1][0] == 0)): 
        htmlElem.send_keys(Keys.LEFT)
    
	# 1st/2nd line 3/2 match
	
    elif (cg[1][1] !=0 and cg[1][1] == cg[0][2]) and \
        ((cg[0][3] == 0 and cg [1][2] == 0 and cg[1][3] == 0) or \
         (cg[0][3]!=0 and cg[1][2] !=0 and cg[1][3] == 0) or \
         (cg[0][3]!=0 and cg[1][3] !=0 and cg[1][2] == 0)):
        htmlElem.send_keys(Keys.RIGHT)

	# Left side matches
	
    elif ((cg[1][0] != 0) and (cg[1][0]==cg[1][1])) or \
    ((cg[2][0] != 0) and (cg[2][0]==cg[2][1])) or \
    ((cg[3][0] != 0) and (cg[3][0]==cg[3][1])): 
        htmlElem.send_keys(Keys.LEFT)
       
	# Right side matches
	
    elif ((cg[1][3] != 0) and (cg[1][3]==cg[1][2])) or \
    ((cg[2][3] != 0) and (cg[2][3]==cg[2][2])) or \
    ((cg[3][3] != 0) and (cg[3][3]==cg[3][2])): 
        htmlElem.send_keys(Keys.RIGHT)
    
	# Left top corner match 3/4
	
    elif (cg[0][0]!= 0 and cg[0][0] == cg[1][2] and cg[1][0] ==0 and cg [1][1] == 0) or \
         (cg[0][0]!= 0 and cg[0][0] == cg[1][3] and cg[1][0] ==0 and cg [1][1] == 0 and cg [1][2] == 0):
        htmlElem.send_keys(Keys.LEFT) 
       
	# Right top corner match 1/2
	
    elif (cg[0][3]!= 0 and cg[0][3] == cg[1][1] and cg[1][3] ==0 and cg[1][2] == 0) or \
         (cg[0][3]!= 0 and cg[0][3] == cg[1][0] and cg[1][3] ==0 and cg[1][2] == 0 and cg[1][1] == 0): 
        htmlElem.send_keys(Keys.RIGHT) 
    
	# 3rd row center + doubling
	
    elif (cg[2][1]!=0 and cg[2][1]==cg[2][2]):
        if (cg[1][1]) == int(cg[2][1]*2): 
            htmlElem.send_keys(Keys.LEFT)
        elif (cg[1][2]) == int(cg[2][2]*2):
            htmlElem.send_keys(Keys.RIGHT)
        else:
            htmlElem.send_keys(random.choice(moves2))
    
	# Bottom row center + doubling
	
    elif (cg[3][1]!=0 and cg[3][1]==cg[3][2]):
        if (cg[2][1]) == int(cg[3][1]*2): 
            htmlElem.send_keys(Keys.LEFT)
        elif (cg[2][2]) == int(cg[3][2]*2):
            htmlElem.send_keys(Keys.RIGHT)
        else:
            htmlElem.send_keys(random.choice(moves2)) 
	
	# Bottom left corner matches
	
    elif (cg[1][0]!= 0 and cg[1][0] == cg[2][1] and cg[2][0] ==0) or \
    (cg[2][0]!= 0 and cg[2][0] == cg[3][1] and cg[3][0] ==0): 
        htmlElem.send_keys(Keys.LEFT)
    
	# Bottom right corner matches	
	
    elif (cg[1][3]!= 0 and cg[1][3] == cg[2][2] and cg[2][3] ==0) or \
    (cg[2][3]!= 0 and cg[2][3] == cg[3][2] and cg[3][3] ==0): 
        htmlElem.send_keys(Keys.RIGHT)
    
	# If no previous conditions met then send UP, RIGHT or LEFT
    else:
        htmlElem.send_keys(random.choice(moves3))

    checkStall()
    
    if (cg[0][1] == maximum and cg[0][0] == 0): # Get maxTile to top corners
        htmlElem.send_keys(Keys.LEFT)
    elif (cg[0][2] == maximum and cg[0][3] == 0):
        htmlElem.send_keys(Keys.RIGHT)
        
    elif(cg[0][1] == maximum and cg[0][2] == 0 and cg[0][3]==0):
        htmlElem.send_keys(Keys.RIGHT)
        
    elif(cg[0][2] == maximum and cg[0][1] == 0 and cg[0][0]==0):
        htmlElem.send_keys(Keys.LEFT)
    
        # Fill first row if max is in corners
    elif (cg[0][0] == maximum or cg[0][3] == maximum) and \
        ((cg[0][0]==0 and (cg[1][0] != 0 or cg[2][0] != 0 or cg[3][0] != 0)) or \
         (cg[0][1] ==0 and (cg[1][1] != 0 or cg[2][1] != 0 or cg[3][1] != 0)) or \
          (cg[0][2] ==0 and (cg[1][2] != 0 or cg[2][2] != 0 or cg[3][2] != 0)) or \
           (cg[0][3] == 0 and (cg[1][3] != 0 or cg[2][3] != 0 or cg[3][3] != 0))):
        htmlElem.send_keys(Keys.UP)
    
    elif (cg[0][0] !=0 and cg[0][0]==cg[0][1]) or \
	(cg[0][0] !=0 and cg[0][0]==cg[0][2] and cg[0][1] == 0):
	    htmlElem.send_keys(Keys.LEFT) # Match top row left

    elif (cg[0][3] !=0 and cg[0][3]==cg[0][2]) or \
        (cg[0][3] !=0 and cg[0][3]==cg[0][1] and cg[0][2] == 0):
        htmlElem.send_keys(Keys.RIGHT) # Match top row right
        
    elif (cg[0][0] !=0 and cg[0][0]==cg[0][3] and cg[0][1] == 0 and cg[0][2] == 0):
        htmlElem.send_keys(random.choice(moves2)) # Match top row corners
    
    elif (cg[0][1]!=0 and cg[0][1]==cg[0][2] and cg[0][0]==0): #Match top row center if corners are free
        htmlElem.send_keys(Keys.LEFT)
    elif (cg[0][1]!=0 and cg[0][1]==cg[0][2] and cg[0][3]==0):
            htmlElem.send_keys(Keys.RIGHT)
	
	 # Between lines match
    elif ((cg[0][0] != 0) and (cg[0][0]==cg[1][0])) or \
    ((cg[0][1] != 0) and (cg[0][1]==cg[1][1])) or \
    ((cg[0][2] != 0) and (cg[0][2]==cg[1][2])) or \
    ((cg[0][3] != 0) and (cg[0][3]==cg[1][3])) or \
    ((cg[1][0] != 0) and (cg[1][0]==cg[2][0])) or \
    ((cg[1][1] != 0) and (cg[1][1]==cg[2][1])) or \
    ((cg[1][2] != 0) and (cg[1][2]==cg[2][2])) or \
    ((cg[1][3] != 0) and (cg[1][3]==cg[2][3])) or \
    ((cg[2][0] != 0) and (cg[2][0]==cg[3][0])) or \
    ((cg[2][1] != 0) and (cg[2][1]==cg[3][1])) or \
    ((cg[2][2] != 0) and (cg[2][2]==cg[3][2])) or \
    ((cg[2][3] != 0) and (cg[2][3]==cg[3][3])) or \
    (cg[0][0]!= 0 and cg[0][0] == cg[2][0] and cg[1][0]==0) or \
    (cg[0][0]!= 0 and cg[0][0] == cg[3][0] and cg[1][0]==0 and cg[2][0]==0) or \
    (cg[0][1]!= 0 and cg[0][1] == cg[2][1] and cg[1][1]==0) or \
    (cg[0][1]!= 0 and cg[0][1] == cg[3][1] and cg[1][1]==0 and cg[2][1]==0) or\
    (cg[0][2]!= 0 and cg[0][2] == cg[2][2] and cg[1][2]==0) or \
    (cg[0][2]!= 0 and cg[0][2] == cg[3][2] and cg[1][2]==0 and cg[2][2]==0) or \
    (cg[0][3]!= 0 and cg[0][3] == cg[2][3] and cg[1][3]==0) or \
    (cg[0][3]!= 0 and cg[0][3] == cg[3][3] and cg[1][3]==0 and cg[2][3]==0):
        htmlElem.send_keys(Keys.UP)
		
    # Top left corner match
    elif (cg[0][0]!= 0 and cg[0][0] == cg[1][1] and cg[1][0] ==0): 
        htmlElem.send_keys(Keys.LEFT)
        htmlElem.send_keys(Keys.UP)
    
    # Top right corner match
    elif (cg[0][3]!= 0 and cg[0][3] == cg[1][2] and cg[1][3] ==0):
        htmlElem.send_keys(Keys.RIGHT)
        htmlElem.send_keys(Keys.UP)
    
    elif (cg[1][1]!=0 and cg[1][1]==cg[1][2]):
        if (cg[0][1] == int(cg[1][1]*2) and cg[1][0]!=0):
            htmlElem.send_keys(Keys.LEFT)
        elif (cg[0][2] == int(cg[1][2]*2) and cg[1][3] !=0):
            htmlElem.send_keys(Keys.RIGHT) # 2nd line center match and check for doubling
        else:
            htmlElem.send_keys(random.choice(moves2))

    elif (cg[1][2] !=0 and cg[1][2] == cg[0][1]) and \
        ((cg[0][0] == 0 and cg [1][0] == 0 and cg[1][1] == 0) or \
         (cg[0][0]!=0 and cg[1][0] !=0 and cg[1][1] == 0) or \
         (cg[0][0]!=0 and cg[1][1] !=0 and cg[1][0] == 0)): # 1st/2nd line 2/3 match
        htmlElem.send_keys(Keys.LEFT)
    
    elif (cg[1][1] !=0 and cg[1][1] == cg[0][2]) and \
        ((cg[0][3] == 0 and cg [1][2] == 0 and cg[1][3] == 0) or \
         (cg[0][3]!=0 and cg[1][2] !=0 and cg[1][3] == 0) or \
         (cg[0][3]!=0 and cg[1][3] !=0 and cg[1][2] == 0)): # 1st/2nd line 3/2 match
        htmlElem.send_keys(Keys.RIGHT)

    elif ((cg[1][0] != 0) and (cg[1][0]==cg[1][1])) or \
    ((cg[2][0] != 0) and (cg[2][0]==cg[2][1])) or \
    ((cg[3][0] != 0) and (cg[3][0]==cg[3][1])): # Left side matches
        htmlElem.send_keys(Keys.LEFT)
        
    elif ((cg[1][3] != 0) and (cg[1][3]==cg[1][2])) or \
    ((cg[2][3] != 0) and (cg[2][3]==cg[2][2])) or \
    ((cg[3][3] != 0) and (cg[3][3]==cg[3][2])): # Right side matches
        htmlElem.send_keys(Keys.RIGHT)
    
    elif (cg[0][0]!= 0 and cg[0][0] == cg[1][2] and cg[1][0] ==0 and cg [1][1] == 0) or \
         (cg[0][0]!= 0 and cg[0][0] == cg[1][3] and cg[1][0] ==0 and cg [1][1] == 0 and cg [1][2] == 0):
        htmlElem.send_keys(Keys.LEFT) # Left top corner match 3/4
        
    elif (cg[0][3]!= 0 and cg[0][3] == cg[1][1] and cg[1][3] ==0 and cg[1][2] == 0) or \
         (cg[0][3]!= 0 and cg[0][3] == cg[1][0] and cg[1][3] ==0 and cg[1][2] == 0 and cg[1][1] == 0): 
        htmlElem.send_keys(Keys.RIGHT) # Right top corner match 1/2
        
    elif (cg[2][1]!=0 and cg[2][1]==cg[2][2]):
        if (cg[1][1]) == int(cg[2][1]*2): # 3rd row center + doubling
            htmlElem.send_keys(Keys.LEFT)
        elif (cg[1][2]) == int(cg[2][2]*2):
            htmlElem.send_keys(Keys.RIGHT)
        else:
            htmlElem.send_keys(random.choice(moves2))
    
    elif (cg[3][1]!=0 and cg[3][1]==cg[3][2]):
        if (cg[2][1]) == int(cg[3][1]*2): # Bottom row center + doubling
            htmlElem.send_keys(Keys.LEFT)
        elif (cg[2][2]) == int(cg[3][2]*2):
            htmlElem.send_keys(Keys.RIGHT)
        else:
            htmlElem.send_keys(random.choice(moves2))
	
    elif (cg[1][0]!= 0 and cg[1][0] == cg[2][1] and cg[2][0] ==0) or \
    (cg[2][0]!= 0 and cg[2][0] == cg[3][1] and cg[3][0] ==0): # Bottom left corner matches
        htmlElem.send_keys(Keys.LEFT)
    
    elif (cg[1][3]!= 0 and cg[1][3] == cg[2][2] and cg[2][3] ==0) or \
    (cg[2][3]!= 0 and cg[2][3] == cg[3][2] and cg[3][3] ==0): # Bottom right corner matches
        htmlElem.send_keys(Keys.RIGHT)
	
    else:
        htmlElem.send_keys(random.choice(moves3))
for method in methods:
	print("Iterating " + method)
	attempts = 60
	which = 1
	score = 0
	maxTile = 0
	previousSum = 0
	timeKeep = 0
	startTime = 0
	solveTime = 0
	stallNumber = 0
		
	while True:
		if which > attempts:
			break
		cg, maximum, gridSum = gridInfo() # Collects the information of the current Grid
    
		globals()["method"+method]() # Runs the current method

		restart(method) # Checks whether needs to restart game
