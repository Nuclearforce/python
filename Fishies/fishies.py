import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation
import sys

fig = plt.figure()
fig.set_dpi(100)
fig.set_size_inches(9, 8)
x=0
y=0
ax = plt.axes(xlim=(0, 100), ylim=(0, 100))
fishRed = plt.Circle((x, y), 1, fc='r')
fishYellow = plt.Circle((x, y), 1, fc='y')
fishBlue = plt.Circle((x, y), 1, fc='b')
fishGreen = plt.Circle((x, y), 1, fc='g')

def init():
    startBiasYellow=np.floor(np.random.uniform()*(99))+1
    fishYellow.center = (0, startBiasYellow)
    ax.add_patch(fishYellow)
    startBiasRed=np.floor(np.random.uniform()*(99))+1
    fishRed.center = (startBiasRed, 0)
    ax.add_patch(fishRed)
    startBiasBlue=np.floor(np.random.uniform()*(99))+1
    fishBlue.center = (startBiasBlue, 100)
    ax.add_patch(fishBlue)
    startBiasGreen=np.floor(np.random.uniform()*(99))+1
    fishGreen.center = (100, startBiasGreen)
    ax.add_patch(fishGreen)

def randomDirection(x,y):
    direction=np.random.uniform()
    if direction<0.25:
        if x>100:
            x-=1
        else: x+=1
    elif direction<0.5:
        if x<0:
            x+=1
        else: x-=1
    elif direction<0.75:
        if y>100:
            y-=1
        else:y+=1
    elif direction<1.0:
        if y<0:
            y+=1
        else:y-=1
    return x,y

def ball(fish):
    x, y = fish.center
    x, y = randomDirection(x,y)
    fish.center = (x, y)

def animate(i):
    ball(fishYellow)
    ball(fishRed)
    ball(fishGreen)
    ball(fishBlue)

def runAnimation():
    anim = animation.FuncAnimation(fig, animate, 
                            init_func=init, 
                            frames=5000, 
                            interval=100,
                            repeat=False,
                            blit=False)                        
    plt.show()

if __name__ == '__main__':
    runAnimation()