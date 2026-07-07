from cmu_graphics import *
import math, random
app.map = []
char = ['A','B','C','D','E','F','G','H',
        'I','J','K','L','M','N','O','P',
        'Q','R','S','T','U','V','W','X',
        'Y','Z','a','b','c','d','e','f',
        'g','h','i','j','k','l','m','n',
        'o','p','q','r','s','t','u','v',
        'w','x','y','z','0','1','2','3',
        '4','5','6','7','8','9','+','/']
tiles = Group()
lengths = [
    161,
    144,
    54,
    87,
    149,
    145,
    120,
    69,
    69
    ]
light = Circle(0,0,600,border='black',borderWidth=550,fill=None,visible=False)
app.loadedMap = 0
for y in range(40):
    for x in range(40):
        tiles.add(Rect(x*10,y*10,10,10,fill=None))
app.songPlaying = random.randint(0,8)
player = RegularPolygon(0,0,5,3,fill='limeGreen',border='black',borderWidth = 1)
player.height *= 1.5
player.lives = 3
fade = Rect(0,0,400,400)
fade.fading = False
fade.timer = 0
fade2 = Rect(0,0,400,400,opacity=100)
fade2.fading = False
fade2.timer = 0
damage = Rect(0,0,400,400,fill=gradient('red','fireBrick'),opacity=0)
damage.timer = 0
deathMessage = Label('You Died!',200,200,size=260,fill='red',font='cinzel',opacity=0)
app.songTimer = 0
player.moveTimer = 0
app.gameStarted = False
app.menuTimer = 0
title = Group(
    Label('Maze or',200,100,size=40,fill='white',font='cinzel',bold=True),
    Label('something idk',200,150,size=40,fill='white',font='cinzel',bold=True)
    )
play = Group(
    Rect(105,205,200,50,fill='paleGreen'),
    Rect(100,200,200,50,fill='white'),
    Label('Play',200,225,size=20,font='cinzel',bold=True),
    )
hard = Group(
    Rect(105,295,200,50,fill='paleGreen'),
    Rect(100,290,200,50,fill='white'),
    Label('Hard Mode',200,315,size=20,font='cinzel',bold=True)
    )
def loadMap(data):
    for i in tiles.children:
        i.fill = None
    player.centerX,player.centerY = int(data[:4])%40*10+5,int(data[:4])//40%40*10+5
    player.spawn = (player.centerX,player.centerY)
    app.map = []
    for i in data[4:]:
        try:
            app.map.append(char.index(i)//4//4%4)
            app.map.append(char.index(i)//4%4)
            app.map.append(char.index(i)%4)
        except:
            pass
    for i in range(data[4:].count('=')):
        app.map.pop()
        app.map.pop()
    for i in range(len(app.map)):
        if app.map[i] == 0:
            color = None
        if app.map[i] == 1:
            color = 'black'
        if app.map[i] == 2:
            color = 'red'
        if app.map[i] == 3:
            color = 'green'
        if tiles.children[i].fill != color:
            tiles.children[i].fill = color
    fade.fading = False
    fade2.fading = False
    light.toFront()
maps = [
    '0082VUAAAAAAAAAAAEBQAAAAAAAAAABAFAAAAAAAAAAAQAUAAAAAAAAAAFABQAAAAAAAAAAUAFAAAAAAAAAABQAUAAAAAAAAAAFABQAAAAAAAAAAUAFAAAAAAAAAABQAUAAAAAAAAAAFABQAAAAAAAAAAUAFAAAAAAAAAABQAUAAAAAAAAAAFABQAAAAAAAAAAUAFAAAAAAAAAABQAUAAAAAAAAAAFABQAAAAAAAAAAUAFAAAAAAAAAABQAUAAAAAAAAAAFABQAAAAAAAAAAUAFAAAAAAAAAABQAUAAAAAAAAAAFABQAAAAAAAAAAUAFAAAAAAAAAABQAUAAAAAAAAAAFABQAAAAAAAAAAUAFAAAAAAAAAABQAUAAAAAAAAAAFABQAAAAAAAAAAUAFAAAAAAAAAABQAUAAAAAAAAAAFABQAAAAAAAAAAUAFAAAAAAAAAABQAUAAAAAAAAAAFABQAAAAAAAAAAUAFAAAAAAAAAABQAQAAAAAAAAAAFDEAAAAAAAAAAAUBAAAAAAAAAAABVQ=',
    '0164AAAAAAAAAAAAAAAAAAAAAAAAAAAFVVVVVVVVVVVQBAEAABAAAQAAEAQBAAAQAAEAABAEAQAAEAABAAAQBAEAABAAAQAAEAQBAFVVVAEAVVAEAQAAAAAAAAAQBAEAAAAAAAAAEAQBAAAAAAAAABAEAQAAAAAAAAAQBAEAVVVUAQBAEAQAAEAAAAEAQBAEAABAAAABAEAQBAAAQAAAAQBAEAQAAEAAAAEAQBAFVVVAFVQBAFVQBAAAQBAAAQAAEAQAAEAQAAEAABAEAABAEAABAAAQBAAAQBAAAQAAEAQBAFVQBVVVVVAEAQAAAAQAAAAQBAEAAAAEAAAAEAQBAAAABAAAABAEAQAAAAQAAAAQBVUAVVVUAVVAEAQAAAAAAAEAQBAEAAAAAAABAEAQBAAAAAAAAQBAEAQAAAAAAAEAQBAFVQBVVVVVAEAQBAAAAAAAAABAEAQAAAAAAAAATxAEAAAAAAAAAE8QBAAAAAAAAABAEAVVVVVVVVVVVVAAAAAAAAAAAAAAAAAAAAAAAAAAAA=',
    '0164AAAAAAAAAAAAAAAAAAAAAAAAAAAFVVVVVVVVVVVQBAAAABAAAAAAEAQAAAAQAAAAABAEAAAAEAAAAAAQBAAAABAAAAAAEAVVVUAVVAFVVVAEAAAAAAQAAAAQBAAAAAAEAAAAEAQAAAAABAAAABAEAAAAAAQAAAAQBAEAVVVUAQBAEAQBAEAAAAEAQBAEAQBAAAABAEAQBAEAQAAAAQBAEAQBAEAAAAEAQBAEAQBVUAVVAFVQBAEAABAAAQAAEAQBAAAQAAEAABAEAQAAEAABAAAQBAEAABAAAQAAEAQBAFVQBAEAQBAEAQBAEAQBAEAQBAEAQBAEAQBAEAQBAEAQBAEAQBAEAQBAEAQBAEAQBVUAQBAFVQBAEAQAAAAAAAEAQBAEAAAAAAABAEAQBAAAAAAAAQBAEAQAAAAAAAEAQBAEAVVVUAVVAEAQBAAAQAAEAABAEAQAAEAABAAATxAEAABAAAQAAE8QBAAAQAAEAABAEAVVVVVVVVVVVVAAAAAAAAAAAAAAAAAAAAAAAAAAAA=',
    '0804AAAAAAAAAAAAAAAAAAAAAAAAAAAFVVVVVVVVVVVQBqqqqoAEAABAEAYAAAAABAAAQBAGAAAAAAQAAEAQBgqqqoAEAABAEAYJVVVQBAFVQBAGCQAqgAQAAAAQBgkAAAAEAAAAEAYJAAAABAAAABAGCQAqgAQAAAAQBgkAVVAEAVVAEAYJAGqAJACqQBAGCQBgACQAAkAQBgkAYAAkAAJAEAYJAGCqpqqCQBAGCVVAlVVVgECQBgkAAJAAAYBCkAYJAACQAAGAQpAGCQAAkAABgEKQBqkAKpAAAYBCkAVVAFVVVAEAQJAEAAAACqAAAEAQBAAAAAAAAABAEAQAAAAAAAAAQBAEAAAACqAAAEAQBVWCVVVUAVVgEAQAAAAABgkAaBAEAAAAAAYJAGgQBAAAAAAGCQBoEAQAAAAABgkAaBAGCVVglVQBAGAQBAAAQBAAAABAEAQAAEAQAAAATxAEAABAEAAAAE8QBAAAQBAAAABAEAVVVVVVVVVVVVAAAAAAAAAAAAAAAAAAAAAAAAAAAA=',
    '0041VVVVVVVVVVVVVUEAAAAGAAAmkClBKoAoBqoAphAJQVVQVQVVQVQVQWCmgCmAAACkAkFoJgAJgAAAJApBVSQQVQVVVQQVQWkkkGgACmAGAAFhJpBgAAJoBoABQQVQQVVQVQVQQUECkkkCkGgCmEFBAJpJAJBgAJpBQQQVQVQQVVVVQUAmCgCgkGimgAFAJoAAApBgJgABQSVVVVVQQVQVQWEmgICAgAAAmgFpJggICAgAAJgBVSQVVVVVVVSVQWgkGqmgACgAmAlgpBgJgqoAoJopQVQQQQVVQVSVVUGgEkGGiEEAmmlBgBpBpgBBApJhQQQVQVQSQQVQYUAkGgAAEEGAAGFApBgqoBhBoABhQVQQVVQQQVQVQWCmAGikEmCmAAFoJoBgJBBoJoABVQVQQVQYVVVVQWgAkkCkECAmimFgqppAJBICBgJhQVVVQQQVVQQQYWCmmgGACmmAEGFoJJgBoAJhoBBpVQQQQVVQQVQQVWAAmGAAmACgmD1qqppoApoAApo9VVVVVVVVVVVVVQ=',
    '0041VVVVVVVVVVVVVUIoCiAAAoAgIIFAAoIiKiAKAoKBSIggAiCigKgAoUgqCiKCCAgAqCFIgIIgCICKqgoBSoggCogioACAKUACIiAiIgKoigFqqCoiIgIoCIKpQIiAIiCgIKgiAWiIqKIICgIIgCFIiAiAiIIgiIqBQIqCigoIKAiAoUgAIIIgKIooIgFiiggICiCAAiKhYgIioKgiKIggIUIiICIAogggiiFKCAiAIgIAgoAJQCCgiggoKgoKgWqCIggggIAooCFACiIgogiKAAKhSIIiCoKCiCooAUgiIIAICgKCgKlCKCIqoKAgIgoBYgCCIAICoiAgKUCoCAKoKAIIgoFoCiCKAKCIgAgJQCICCCiCAKqAoWogIiCIqqoAIgFAIiIiiAAAKIIhaoIgIAKqqoCIIUAiCIigAAAKCKFKoIiIgqqqoCAhQAiIiogAICIKoWKoKICKqgIAgAFgIgiCAACqqKqhQiAooKqoAAAAKWIAgAgCAqKqqgFCIgiCICAAAACNVVVVVVVVVVVVVQ='
    ]
loadMap(maps[app.loadedMap])
player.targetAngle = 0
title.toFront()
play.toFront()
hard.toFront()
fade2.toFront()
keys = []
def onMousePress(mouseX,mouseY):
    if play.children[1].hits(mouseX,mouseY):
        fade2.toFront()
        fade2.timer = 50
        fade2.fading = True
    if hard.children[1].hits(mouseX,mouseY):
        fade2.toFront()
        fade2.timer = 50
        fade2.fading = True
        light.visible = True
def onMouseMove(mouseX,mouseY):
    play.rotateAngle = 0
    hard.rotateAngle = 0
    if play.children[1].hits(mouseX,mouseY):
        play.children[1].width = 220
        play.children[0].width = 220
        play.children[1].height = 70
        play.children[0].height = 70
        play.children[1].centerX = 200
        play.children[0].centerX = 205
        play.children[1].centerY = 225
        play.children[0].centerY = 230
        play.children[2].size = 30
    else:
        play.children[1].width = 200
        play.children[0].width = 200
        play.children[1].height = 50
        play.children[0].height = 50
        play.children[1].centerX = 200
        play.children[0].centerX = 205
        play.children[1].centerY = 225
        play.children[0].centerY = 230
        play.children[2].size = 20
    if hard.children[1].hits(mouseX,mouseY):
        hard.children[1].width = 220
        hard.children[0].width = 220
        hard.children[1].height = 70
        hard.children[0].height = 70
        hard.children[1].centerX = 200
        hard.children[0].centerX = 205
        hard.children[1].centerY = 315
        hard.children[0].centerY = 320
        hard.children[2].size = 30
    else:
        hard.children[1].width = 200
        hard.children[0].width = 200
        hard.children[1].height = 50
        hard.children[0].height = 50
        hard.children[1].centerX = 200
        hard.children[0].centerX = 205
        hard.children[1].centerY = 315
        hard.children[0].centerY = 320
        hard.children[2].size = 20
    play.rotateAngle = 5*math.sin(app.menuTimer/50)
    hard.rotateAngle = 5*math.cos(app.menuTimer/50)
def onKeyPress(key):
    if not key in keys:
        keys.append(key)
def onKeyRelease(key):
    if key in keys:
        keys.remove(key)
def onStep():
    if app.gameStarted:
        light.centerX,light.centerY = player.centerX,player.centerY
        if player.moveTimer > 0:
            if player.moveTimer < 1.5 * app.stepsPerSecond:
                player.moveTimer += 1
            else:
                player.moveTimer = 0
        app.songTimer += 1
        if app.songTimer == lengths[app.songPlaying]*app.stepsPerSecond:
            app.songPlaying = random.randint(0,8)
            app.songTimer = 0
        if 0 < damage.timer:
            try:
                fade.opacity += 5
            except: fade.opacity = 100
            if damage.timer <= 19:
                try:
                    deathMessage.opacity += 6
                except: deathMessage.opacity = 100
                deathMessage.size -= damage.timer
                deathMessage.rotateAngle = random.uniform(-5,5)
                damage.timer += 1
            else:
                deathMessage.rotateAngle = 0
                sleep(10)
                app.stop()
            return
        if fade.opacity >= 2 and not fade.fading:
            fade.opacity -= 2
        if fade.fading and fade.opacity <= 98:
            fade.opacity += 2
        if damage.opacity != 0:
            damage.opacity -= 1
        player.velocity = [0,0]
        if player.moveTimer <= 0:
            if 'left' in keys:
                player.velocity[0] -= 2
            if 'right' in keys:
                player.velocity[0] += 2
            if 'up' in keys:
                player.velocity[1] -= 2
            if 'down' in keys:
                player.velocity[1] += 2
        player.centerX += player.velocity[0]
        if app.map[player.centerX//10 + player.centerY//10*40] == 1:
            player.centerX -= player.velocity[0]
        if app.map[player.centerX//10 + player.centerY//10*40] == 2:
            takeDamage()
        if app.map[player.centerX//10 + player.centerY//10*40] == 3:
            app.map = [0 if x == 3 else x for x in app.map]
            fade.timer = 50
            fade.fading = True
        player.centerY += player.velocity[1]
        if app.map[player.centerX//10 + player.centerY//10*40] == 1:
            player.centerY -= player.velocity[1]
        if app.map[player.centerX//10 + player.centerY//10*40] == 2:
            takeDamage()
        if app.map[player.centerX//10 + player.centerY//10*40] == 3:
            app.map = [0 if x == 3 else x for x in app.map]
            fade.timer = 50
            fade.fading = True
        try:
            player.targetAngle = math.degrees(-math.atan(player.velocity[0]/player.velocity[1]))
        except:
            pass
        if player.velocity[1] == 0:
            if player.velocity[0] > 0:
                player.targetAngle = 90
            if player.velocity[0] < 0:
                player.targetAngle = -90
        if player.velocity[1] > 0:
            player.targetAngle += 180
        if player.rotateAngle - player.targetAngle > 180:
            player.rotateAngle -= 360
        if player.rotateAngle - player.targetAngle < -180:
            player.rotateAngle += 360
        if abs(player.rotateAngle - player.targetAngle) < 1:
            player.rotateAngle = player.targetAngle
        else:
            player.rotateAngle += 0.3*(player.targetAngle - player.rotateAngle)
        if fade.timer > 0:
            fade.timer -= 1
            if fade.timer == 0:
                try:
                    app.loadedMap += 1
                    loadMap(maps[app.loadedMap])
                    fade.fading = False
                    player.moveTimer = 1
                except:
                    tiles.clear()
                    fade.visible = False
                    app.background = gradient('red','orange','yellow','chartreuse','cyan','violet',start='top-left')
                    Label('You Win!',200,200,size=70,fill='limeGreen',font='cinzel')
                    app.songTimer = 5000
                    app.group.remove(player)
                    light.visible = False
                    sleep(10)
                    app.stop()
    else:
        app.menuTimer += 1
        play.rotateAngle = 5*math.sin(app.menuTimer/50)
        hard.rotateAngle = 5*math.cos(app.menuTimer/50)
        title.rotateAngle = -2*math.cos(25+app.menuTimer/50)
        if fade2.opacity >= 2 and not fade2.fading:
            fade2.opacity -= 2
        if fade2.fading and fade2.opacity <= 98:
            fade2.opacity += 2
        if fade2.timer > 0:
            fade2.timer -= 1
            if fade2.timer == 0:
                title.visible = False
                play.visible = False
                hard.visible = False
                fade2.visible = False
                app.gameStarted = True
def takeDamage():
    player.lives -= 1
    if player.lives <= 0:
        player.centerX, player.centerY = player.spawn
        tiles.clear()
        damage.timer = 1
        damage.toFront()
        damage.opacity = 25
        app.group.remove(player)
        light.visible = False
        app.songTimer = 5000
    else:
        player.moveTimer = 1
        player.centerX, player.centerY = player.spawn
        damage.toFront()
        damage.opacity = 50 / player.lives
        if player.fill == 'yellow':
            player.fill = 'red'
        if player.fill == 'limeGreen':
            player.fill = 'yellow'
cmu_graphics.run()
