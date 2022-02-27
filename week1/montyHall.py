from cgi import test
import random
import matplotlib.pyplot as plt
plt.style.use('fivethirtyeight')

def revealFunc(prizyDoor, doorCount, playerChoice):
    i = 1
    while (i==prizyDoor or i==playerChoice):
        i = (i+1)%(doorCount)
    return i

def switchFunc(shownDoor, doorCount, playerChoice):
    i = 1
    while (i==shownDoor or i==playerChoice):
        i = (i+1)%(doorCount)

    return i

def montyHallGame(switch, testNum):
    winSwitch = 0
    winNoSwitch = 0
    loseSwitch = 0
    loseNoSwitch = 0
    
    doors = [0,1,2]
    doorCount = len(doors)
    
    #Loop through the number of times the contestant can play the game
    for i in range(0, testNum):
        prizyDoor = random.randint(0, doorCount-1) #randomly choose the correct door
        playerChoice = random.randint(0, doorCount-1)
        originalPlayerChoice = playerChoice
        shownDoor = revealFunc(prizyDoor, doorCount, playerChoice)

        #if the user selects to always switch, allow the user
        #to switch other than original choice

        if switch == True:
            playerChoice = switchFunc(shownDoor, doorCount, playerChoice)

        if playerChoice == prizyDoor and switch == False:
            #Then the player wins from not switching
            winNoSwitch = winNoSwitch + 1

        elif playerChoice == prizyDoor and switch == True:
            #Then the player wins from switching
            winSwitch = winSwitch + 1

        elif playerChoice != prizyDoor and switch == False:
            #Then the player loses from not switching
            loseNoSwitch = loseNoSwitch + 1

        elif playerChoice != prizyDoor and switch == True:
            #Then the player loses from switching
            loseSwitch = loseSwitch + 1

        else:
            print('err.. error')

    switchWinrate = winSwitch/(testNum/100)
    noSwitchWinrate = winNoSwitch/(testNum/100)

    return switchWinrate, noSwitchWinrate, winNoSwitch, winSwitch, loseNoSwitch, loseSwitch, testNum

x = montyHallGame(False, 1000)
print('Winrate by not switching: ', x[1], '%')

y = montyHallGame(True, 1000)
print('Winrate by switching: ',y[0], '%')

