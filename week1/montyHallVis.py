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
            # print('Player Wins (No Switch) - Choosen door #:', playerChoice, 'Original door choice #:', originalPlayerChoice, 'Door with the prize #:', prizyDoor, 'Shown door #:', shownDoor)
            winNoSwitch = winNoSwitch + 1

        elif playerChoice == prizyDoor and switch == True:
            #Then the player wins from switching
            # print('Player Wins (Switch) - Choosen door #:', playerChoice, 'Original door choice #:', originalPlayerChoice, 'Door with the prize #:', prizyDoor, 'Shown door #:', shownDoor)
            winSwitch = winSwitch + 1

        elif playerChoice != prizyDoor and switch == False:
            #Then the player loses from not switching
            # print('Player Wins (No Switch) - Choosen door #:', playerChoice, 'Original door choice #:', originalPlayerChoice, 'Door with the prize #:', prizyDoor, 'Shown door #:', shownDoor)
            loseNoSwitch = loseNoSwitch + 1

        elif playerChoice != prizyDoor and switch == True:
            #Then the player loses from switching
            # print('Player Wins (Switch) - Choosen door #:', playerChoice, 'Original door choice #:', originalPlayerChoice, 'Door with the prize #:', prizyDoor, 'Shown door #:', shownDoor)
            loseSwitch = loseSwitch + 1

        #else:
            #print('schiefgelauft')

    switchWinrate = winSwitch/(testNum/100)
    noSwitchWinrate = winNoSwitch/(testNum/100)

    return switchWinrate, noSwitchWinrate, winNoSwitch, winSwitch, loseNoSwitch, loseSwitch, testNum

testCount = []
winrateBySwitching = []

#Running 1000 simulated games
for i in range(1, 1001):
    testCount.append(i)
    x = montyHallGame(True, i)
    winrateBySwitching.append(x[0])

#visualization
plt.figure(figsize=(12.2, 4.5))
plt.plot (testCount, winrateBySwitching)
plt.title('Monty Hall Problem')
plt.xlabel('Number of Tests')
plt.ylabel('Win Percentage')
plt.show()

# x = montyHallGame(True, 1000)
# print('Winrate by switching: ',x[0], '%')

# y = montyHallGame(False, 1000)
# print('Winrate by not switching: ', y[1], '%')