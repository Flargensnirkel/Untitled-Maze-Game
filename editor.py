from cmu_graphics import *
import math

import tkinter as tk
root = tk.Tk()
root.withdraw()

map = []
char = ['A','B','C','D','E','F','G','H',
        'I','J','K','L','M','N','O','P',
        'Q','R','S','T','U','V','W','X',
        'Y','Z','a','b','c','d','e','f',
        'g','h','i','j','k','l','m','n',
        'o','p','q','r','s','t','u','v',
        'w','x','y','z','0','1','2','3',
        '4','5','6','7','8','9','+','/']
id = 1

color = 'black'
pressed = False
mouse = (0,0)
buffer = Rect(0,0,400,400,visible=False)
tiles = Group()
for y in range(40):
    for x in range(40):
        tiles.add(Rect(x*10,y*10,10,10,fill=None))
for i in range(1600):
    map.append(0)
def onStep():
    if pressed:
        whenMousePressed(mouse[0],mouse[1])
    for i in tiles.children:
        i.border = None
    getShapeAt(mouse[0],mouse[1]).border = 'black'
def whenMousePressed(mouseX,mouseY):
    getShapeAt(mouseX, mouseY).fill = color
    map[getShapeAt(mouseX,mouseY).left/10+getShapeAt(mouseX,mouseY).top*4] = id
def onMousePress(mouseX,mouseY):
    global pressed, mouse
    pressed = True
    mouse = (mouseX,mouseY)
def onMouseRelease(mouseX,mouseY):
    global pressed
    pressed = False
def onMouseMove(mouseX,mouseY):
    global mouse
    mouse = (mouseX,mouseY)
def onMouseDrag(mouseX,mouseY):
    global mouse
    mouse = (mouseX,mouseY)
def onKeyPress(key):
    global color, id
    try:
        id = int(key)
    except:
        pass
    if key == '0':
        color = None
    elif key == '1':
        color = 'black'
    elif key == '2':
        color = 'red'
    elif key == '3':
        color = 'green'
    elif key == 'space':
        print(map)
    elif key == 'enter':
        exportMap(mouse[0]//10,mouse[1]//10)
    elif key == 'l':
        loadMap(root.clipboard_get())
    else:
        color = None
        id = 0
def getShapeAt(x,y):
    return tiles.children[math.floor(x/10)+math.floor(y/10)*40]
def loadMap(data):
    global map
    map = []
    for i in data[4:]:
        try:
            map.append(char.index(i)//4//4%4)
            map.append(char.index(i)//4%4)
            map.append(char.index(i)%4)
        except:
            pass
    for i in range(data[4:].count('=')):
        map.pop()
        map.pop()
    for i in range(len(map)):
        if map[i] == 0:
            color = None
        if map[i] == 1:
            color = 'black'
        if map[i] == 2:
            color = 'red'
        if map[i] == 3:
            color = 'green'
        if tiles.children[i].fill != color:
            tiles.children[i].fill = color
def exportMap(x,y):
    output = ''
    for i in range(4-len(str(x+40*y))):
        output += '0'
    output += str(x+40*y)
    for i in range(len(map)):
        if i % 3 == 0:
            value = 0
            value += 16*map[i]
            try:
                value += 4*map[i+1]
                value += map[i+2]
            except:
                pass
            output += char[value]
    for j in range(len(map)%3):
        output += '='
    print(output)


cmu_graphics.run()
