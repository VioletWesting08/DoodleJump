from cmu_graphics import *
from PIL import Image
from random import randint
import math
# The above was to use random number generation, found here:
'''https://machinelearningmastery.com/how-to-generate-random-numbers
-in-python/#:~:text=Random%20integer%20values%20can%20be,interval%20%
5Bstart%2C%20end%5D.'''

import os, pathlib

def onAppStart(app):
    highScoreFile = 'high_scores.txt'
    

    app.highScore = 0

    ##### IMAGE INITIALIZATION ##########

    ### Note: the images below were found at 
    # https://custom-cursor.com/en/collection/games/doodle-jump-doodler

    app.doodleJump = Image.open("TP_Images/doodleJump.png")
    app.doodleJump = app.doodleJump.resize((50, 50))
    app.doodleJumpWidth, app.doodleJumpHeight = (
        app.doodleJump.width, app.doodleJump.height)
    app.doodleJump = CMUImage(app.doodleJump)
    
    app.doodleShoot = Image.open("TP_Images/doodleShoot.png")
    app.doodleShootWidth, app.doodleShootHeight = (
        app.doodleShoot.width, app.doodleShoot.height)
    app.doodleShoot = CMUImage(app.doodleShoot)

    ########## PAUSE IMAGE INITIALIZATION #############
    app.pauseLogo = Image.open('TP_Images/pause.png')  
    ## drawn by Victoria Li (fluffy fish)
    app.pauseLogoWidth, app.pauseLogoHeight = (
        app.pauseLogo.width, app.pauseLogo.height)
    app.pauseLogo = (app.pauseLogo.resize((app.pauseLogoWidth//3, 
                                           app.pauseLogoHeight//3)))
    app.pauseLogo = CMUImage(app.pauseLogo)

    ############ GAME OVER IMAGE INTIIALIZATION #######
    app.gameOverImage = Image.open('TP_Images/game over.png')  
    ## drawn by Victoria Li (fluffy fish)
    app.gameOverImageWidth, app.gameOverImageHeight = (
        app.gameOverImage.width, app.gameOverImage.height)
    app.gameOverImage = app.gameOverImage.resize((
        app.gameOverImageWidth//3, app.gameOverImageHeight//3))
    app.gameOverImage = CMUImage(app.gameOverImage)
    
    ############### START SCREEN IMAGE INITIALIZATION ###########
    # background found at 
    ''' https://www.freepik.com/premium-photo/crumpled-graph-
    paper-texture-background_38709411.htm '''
    app.graphImage = Image.open('TP_Images/graph paper.png')  
    ## drawn by Victoria Li (fluffy fish)
    app.graphImageWidth, app.graphImageHeight = (
        app.graphImage.width, app.graphImage.height)
    app.graphImage = app.graphImage.resize((
        app.graphImageWidth, app.graphImageHeight))
    app.graphImage = CMUImage(app.graphImage)

    app.score = 0 
    # initializating score

    restartGame(app)
    

def restartGame(app):
    ############ HIGH SCORE INITIALIZATION ###########
    with open("high_scores.txt", encoding='utf-8') as f:
        fileString = f.read()
        f.close()
                    
    app.highScoreList = fileString.split("\n")


    print()
    for i in range(0, 5): ## stepping backwards through the scores
        print(app.score, app.highScoreList[i])
        if app.score > int(app.highScoreList[i]):
            print("YEEHAW")
            app.highScoreList.insert(i, str(int(app.score)))
            app.highScoreList.pop()
            break
        if app.score == int(app.highScoreList[i]):
            break

    scoreString = ''
    for score in app.highScoreList:
        if scoreString == '':
            scoreString = score
        else: scoreString = scoreString + '\n' + score

    with open('high_scores.txt', "r+") as f:
        data = f.read()
        f.seek(0)
        f.write(scoreString)
        f.truncate()
        ## https://stackoverflow.com/questions/6648493/
        # how-to-open-a-file-for-both-reading-and-writing
        # #comment97020595_15976014

    ############## START SCREEN INITIALIZATION ##########
    app.single = Platform(app.width//2, app.height - 50, 
                          'TP_Images/platform.png', -1, -1)

    ############## MOVEMENT INITIALIZATION ##############
    app.cx = app.width//2
    app.cy = 350
    app.dx = 0
    app.dy = -1
    app.ddx = 0
    app.ddy = 0.1
    app.buttonAccel = 0.1
    app.difficulty = 1
    app.stepsPerSecond = 45

    ############# GAME INITIALIZATION ############
    app.gameOver = False
    app.gamePaused = False
    app.scrollMargin = app.height - 200
    app.scrollDivider = 70
    app.scrollY = 0
    app.scrolling = False
    app.movingPlatformIndex = None
    app.startScreen = True
    
    ############## MONSTER INITIALIZATION ###########
    app.counter = 0
    app.monsterProjectiles = []
    app.monsterProbability = 10
    app.bulletFrequency = 3

    ########## POWERUP INITIALIZATION #################
    ## portal intialization
    app.portalProbability = 10
    app.teleportDistance = app.height

    ############### PLATFORM INITIALIZATION ###################
    app.cloudPlatform = Platform(app.width//2, app.height - 50, 
                                 'TP_Images/colorful platform.png', 
                                 app.monsterProbability, app.portalProbability)
    ## platfroms above drawn by the Great and Honourable Steven Yi Yang (SCS 27)
    app.normalPlatform = Platform(app.width//2, app.height - 50, 
                                  'TP_Images/sliding platform.png', 
                                  app.monsterProbability, app.portalProbability)
    ## platform above drawn by me
    app.movingPlatform = Platform(app.width//2, app.height - 50, 
                                  'TP_Images/caution platform.png', 
                                  app.monsterProbability, app.portalProbability)
    ### platform above drawn by Allen Wu

    ############ PROJECTILE INITIALIZATION ##############################
    app.projectiles = []
    app.radius = 5
    app.projectileSpeed = 3

    ########### SCORE INITIALIZATION ###########################
    app.score = 0
    app.displayScore = 0
    app.scoreX = app.width//2
    app.scoreY = 10
    app.monsterKillPoints = 500
    app.highScoreScreen = False

    ################ TUTORIAL INITIALIZATION ##################
    app.tutorial = False

def redrawAll(app):
    
    ### REDRAW PLATFORMS ####
    app.cloudPlatform.draw(app.width, app.height, app.difficulty, app.monsterProbability)
    app.movingPlatform.draw(app.width, app.height, app.difficulty, app.monsterProbability)
    app.normalPlatform.draw(app.width, app.height, app.difficulty, app.monsterProbability)
    
    ### REDRAW MONSTERS ###
    app.normalPlatform.drawMonster()

    ### REDRAW PORTALS ###
    for portal in app.movingPlatform.portalList:
        portal.draw()

    ### REDRAW PROJECTILES ####
    for projectile in app.projectiles:
        projectile.drawProjectile()
    for projectile in app.monsterProjectiles:
        projectile.drawProjectile()

    ### REDRAW DOODLE ####
    drawImage(app.doodleJump, app.cx, app.cy, align = 'center')

    ### REDRAW SCORE ####
    drawRect(0, 0, app.width, 20, fill = 'white')
    drawLabel(f'Score: {int(app.displayScore)}', app.scoreX, 
              app.scoreY, font = 'Ink Free', align = 'center', size = 18)
    
    ############ REDRAW GAME OVER SCREEN #########
    if app.gameOver == True:
        drawRect(0, 0, app.width, app.height, fill = 'white', opacity = 80)
        drawImage(app.gameOverImage, app.width//2, app.height//2, 
                  align = 'center')
        drawRect(0, 0, app.width, app.height, fill = 'red', opacity = 20)
        drawLabel(f'Your Score: {int(app.score)}', app.width//2, 
                  app.height //2 + 200, size = 25, align = 'center', 
                  font = 'Ink Free')
        
    ### REDRAW START SCREEN #####
    if app.startScreen == True:
        drawStartScreen(app)
    
    ############ REDRAW TUTORIAL SCREEN #############
    if app.tutorial == True:
        drawTutorialScreen(app)

    ######### REDRAW PAUSE BUTTON ############
    if app.gamePaused == True:
        drawRect(0, 0, app.width, app.height, fill = 'white', opacity = 80)
        drawImage(app.pauseLogo, app.width//2, app.height//2, align = 'center')

    ######### REDRAW HIGH SCORE LIST ############
    if app.highScoreScreen == True:
        drawRect(0, 0, app.width, app.height, fill = 'white')
        drawImage(app.graphImage, app.width//2, app.height//2, 
                  align = 'center', opacity = 50)
        drawLabel('High Scores:', app.width//2, app.height//2 - 200, font = 'Ink Free', size = 36, bold = True)
        i = 0
        while i < len(app.highScoreList):
            drawLabel(f'{i + 1}: {app.highScoreList[i]}', app.width//2, app.height//2 - 125 + i*50, font = 'Ink Free', size = 18, bold = True)
            i += 1
        drawLabel("press 'r' to go back to the start screen", app.width//2, app.height//2 - 125 + i*50, font = 'Ink Free', size = 18)

def onStep(app):
    if app.score > app.highScore:
        app.highScore = app.score
    if app.startScreen == True:
        stepStartScreen(app)
    ########## DIFFICULTY STEP ##########
    app.difficulty = int(app.score) // 1000
    ### Comment me out to manually toggle difficulty!

    if app.difficulty > 10:
        app.difficulty = 10

    app.monsterProbability = 10 - app.difficulty
    ### comment me out to manually toggle probability!

        ############## PLATFORM STEP #############
    if (app.gameOver == False and app.startScreen == False 
        and app.gamePaused == False):
        app.movingPlatform.jitter(app.width)
        app.cloudPlatform.moveSideways(app.width)

        ############## MONSTER STEP #############
        if app.normalPlatform.monsterStep(app.cx, app.cy) == True:
            app.gameOver = True
        if app.normalPlatform.monsterList != []:
            if app.normalPlatform.monsterList[0].cy > app.height:
                app.normalPlatform.monsterList.pop(0)
        app.counter += 1
        if app.counter == app.bulletFrequency * app.stepsPerSecond:
            for monster in app.normalPlatform.monsterList:
                app.monsterProjectiles.append(Projectile(monster.cx, 
                monster.cy, app.cx, app.cy, app.radius, app.projectileSpeed, 
                'TP_Images/monster projectile.png')) ## Steven Yi Yang
            app.counter = 0

        ############### DOODLE STEP ###########
        app.cy += app.scrollY
        app.dx *= 0.99
        if app.scrolling == False:
            app.cy += app.dy
            app.dy += app.ddy
        app.cx += app.dx
        app.dx += app.ddx
        # bouncing off of bottom
        if app.cy + 20 >= app.height:
            app.gameOver = True

        ######### WRAPAROUND DOODLE #############

        if app.cx < 0:### if the doodle went to the left
            app.cx = app.width

        if app.cx > app.width:
            app.cx = 0

        # setting acceleration back to zero if the key got pressed
        app.ddx = 0  

        ################ PLATFORM STEP ############
        #### NORMAL PLATFORM BOUNCING ############
        if app.dy > 0: 
            for platform in app.normalPlatform.location:
                platformX = platform[0]
                platformY = platform[1]
                leftBound = platformX - app.normalPlatform.imageWidth//15 
                rightBound = platformX + app.normalPlatform.imageWidth//15

                if ((app.cx > leftBound) and (app.cx < rightBound)and 
                    (platformY - app.cy >= 0)  and (platformY - app.cy <= 22)): 
                    app.dy = -6
                    app.scrolling = False

        ####### MOVING PLATFORM BOUNCING #########
            i = 0
            while i < len(app.movingPlatform.location):
                platform = app.movingPlatform.location[i]
                platformX = platform[0]
                platformY = platform[1]
                leftBound = platformX - app.normalPlatform.imageWidth//15 
                rightBound = platformX + app.normalPlatform.imageWidth//15

                if ((app.cx > leftBound) and (app.cx < rightBound)and 
                    (platformY - app.cy >= 0)  and (platformY - app.cy <= 22)): 
                    app.dy = -6
                    app.movingPlatformIndex = i
                    app.movingPlatform.disappear(app.movingPlatformIndex)
                    app.scrolling = False
                i += 1

        ######### CLOUD PLATFORM BOUNCING #######      
            for platform in app.cloudPlatform.location:
                platformX = platform[0]
                platformY = platform[1]
                leftBound = platformX - app.normalPlatform.imageWidth//15 
                rightBound = platformX + app.normalPlatform.imageWidth//15

                if ((app.cx > leftBound) and (app.cx < rightBound)and 
                    (platformY - app.cy >= 0)  and (platformY - app.cy <= 22)): 
                    app.dy = -6
                    app.scrolling = False

        ############ SIDE SCROLLING #################### 
        # (based off of the 112 notes)
        if (app.cy <= app.scrollMargin):
            app.scrollY = (app.scrollMargin - app.cy)//app.scrollDivider
            app.cloudPlatform.scroll(app.scrollY)
            app.movingPlatform.scroll(app.scrollY)
            app.normalPlatform.scroll(app.scrollY)
            app.scrolling = True
            app.scrolling = False
        
        ############# PROJECTILE STEP ########### 
        for projectile in app.projectiles:
            projectile.moveProjectile()
        for projectile in app.monsterProjectiles:
            projectile.moveProjectile()
        if len(app.projectiles) >= 15:
            app.projectiles.pop(0)
        if len(app.monsterProjectiles) >= 20:
            app.monsterProjectiles.pop(0)

        ## scrolling projectiles
        for projectile in app.projectiles:
            projectile.scroll(app.scrollY)
        for projectile in app.monsterProjectiles:
            projectile.scroll(app.scrollY)

        ### checking projectile collision
        ########### projectile doodle collision
        for projectile in app.monsterProjectiles:
            leftBound = app.cx - 25
            rightBound = app.cx + 25
            lowerBound = app.cy - 35
            upperBound = app.cy + 35
            if leftBound < projectile.cx < rightBound and\
                lowerBound < projectile.cy < upperBound:
                app.gameOver = True
            pass
        ########### projectile monster collision
        for projectile in app.projectiles:
            for monster in app.normalPlatform.monsterList:
                leftBound = monster.cx - 35
                rightBound = monster.cx + 35
                lowerBound = monster.cy - 35
                upperBound = monster.cy + 35
                if leftBound < projectile.cx < rightBound and\
                    lowerBound < projectile.cy < upperBound:
                    index = app.normalPlatform.monsterList.index(monster)
                    app.normalPlatform.monsterList.pop(index)
                    ## gaining score for killing monsters
                    app.score += app.monsterKillPoints
                    app.displayScore += 500

        ############# SCORE STEP #################
        app.score += app.scrollY
        if app.displayScore < app.score:
            app.displayScore = min(app.score, app.displayScore 
                                   + int(2*app.scrollY + 1))
        
        ### POWERUP STEP #########
        # portal scrolling
        for portal in app.movingPlatform.portalList:
            portal.scroll(app.scrollY)

            ## ensuring you don't land on top of enemies
            if distance(portal.cx, portal.cy, app.cx, app.cy) < 30:
                cx, cy = portal.teleport(app.cx, app.cy, app.width)
                for monster in app.normalPlatform.monsterList:
                    if distance(cx, cy, monster.cx, monster.cy) < 50:
                        cx, cy = portal.teleport(app.cx, app.cy, app.width)
                for projectile in app.monsterProjectiles:
                    if distance(cx, cy, projectile.cx, projectile.cy) < 10:
                        cx, cy = portal.teleport(app.cx, app.cy, app.width)
                index = app.movingPlatform.portalList.index(portal)
                app.movingPlatform.portalList.pop(index)
                app.cx = cx
                app.cy = cy
        
        if (app.movingPlatform.portalList != [] and 
            app.movingPlatform.portalList[0].cy > app.height):
            app.movingPlatform.portalList.pop(0)
            
        if app.normalPlatform.portalList != []:
            app.normalPlatform.portalList.pop()
        if app.cloudPlatform.portalList != []:
            app.cloudPlatform.portalList.pop()


def onKeyPress(app, key):
    if app.gameOver == False:
        app.dx = 0
    if key == 'r':
        restartGame(app)
    if key == 's':
        app.startScreen = False
        app.tutorial = False
    if app.startScreen == False and app.gameOver == False:
        if key == 'p':
            app.gamePaused = not app.gamePaused
    if app.startScreen == True and key == 't':
        app.tutorial = True
    if app.startScreen == True and key == 'h':
        app.highScoreScreen = True

    ###### Testing difficulty ######
    if key == '0':
        app.difficulty = 0
    if key == '1':
        app.difficulty = 1
    if key == '2':
        app.difficulty = 2
    if key == '3':
        app.difficulty = 3
    if key == '4':
        app.difficulty = 4
    if key == '5':
        app.difficulty = 5
    if key == '6':
        app.difficulty = 6
    if key == '7':
        app.difficulty = 7
    if key == '8':
        app.difficulty = 8
    if key == '9':
        app.difficulty = 9


def onKeyHold(app, key):
    if (app.gameOver == False and app.startScreen == False and 
        app.gamePaused == False):
        if 'right' in key or 'd' in key:
            app.ddx = app.buttonAccel
        if 'left' in key or 'a' in key: 
            app.ddx = -app.buttonAccel

def onMousePress(app, mouseX, mouseY):
    if app.startScreen == False and app.gamePaused == False:
        app.projectiles.append(Projectile(app.cx, app.cy, mouseX, mouseY, 
        app.radius, app.projectileSpeed, 'TP_Images/projectile.png')) ## Gene Yang, SCS 27 (112>122)

def drawTutorialScreen(app):
    ## variables
    portalX = app.width//2
    portalY = 75
    tutorialPortal = Portal(0,0,0)

    monsterX = app.width//2 + 100
    mProjectileX = monsterX - 100
    monsterY = portalY + 125
    tutorialMonster = Monster(0, 0)
    tutorialMonsterProjectile = Projectile(1, 1, 0, 0, 1, 1,
                                            'TP_Images/monster projectile.png')

    puddingPlatformX = 100
    puddingPlatformY = app.height//2 + 100
    puddingPlatform = app.normalPlatform.image

    shakingPlatformX = app.width - 100
    shakingPlatformY = puddingPlatformY + 50
    shakingPlatform = app.movingPlatform.image

    slidingPlatformX = 100
    slidingPlatformY = shakingPlatformY + 50
    slidingPlatform = app.cloudPlatform.image

    drawRect(0, 0, app.width, app.height, fill = 'white')
    ## background
    drawImage(app.graphImage, app.width//2, app.height//2, 
              align = 'center', opacity = 50)
    ## instructions
    drawLabel("click the screen to shoot monsters", app.width//2, 
              app.height//2 - 40, size = 18, align = 'center', 
              font = 'Ink Free')
    drawLabel("Press 's' to start", app.width//2, app.height//2, 
              size = 18, align = 'center', font = 'Ink Free')
    drawLabel("Press 'r' to go back to the start screen!", 
              app.width//2, app.height//2 + 40, size = 18, 
              align = 'center', font = 'Ink Free')
    ## portal stuff
    drawImage(tutorialPortal.image, portalX - 100, 
              portalY, align = 'center')
    drawLabel('jump through here to get teleported to a random location 0.0', 
              portalX, portalY + 30, rotateAngle = -10, size = 14, 
              bold = True, font = 'Ink Free')
    ## monster stuff
    drawImage(tutorialMonster.image, app.width - 100, 
              monsterY, align = 'center')
    drawLabel('touch me and you die!', monsterX, monsterY + 30, 
              rotateAngle = 5, size = 14, bold = True, font = 'Ink Free')
    drawImage(tutorialMonsterProjectile.image, 
              mProjectileX, monsterY+5, align = 'center')
    drawLabel('Radioactive monster spit ->', mProjectileX - 100, 
              monsterY, size = 14, bold = True, 
              font = 'Ink Free', align = 'center')
    ## platform stuff
    # pudding platform
    drawImage(puddingPlatform, puddingPlatformX, 
              puddingPlatformY, align = 'center')
    drawLabel('<- spawns monsters', puddingPlatformX + 100, 
              puddingPlatformY, size = 14, bold = True, 
              font = 'Ink Free', align = 'center')
    # shaking platform
    drawImage(shakingPlatform, shakingPlatformX, 
              shakingPlatformY, align = 'center')
    drawLabel('disappears when you jump on it! ->',
               shakingPlatformX - 150, shakingPlatformY, 
               size = 14, bold = True, font = 'Ink Free', align = 'center')
    # sliding platform
    drawImage(slidingPlatform, slidingPlatformX, 
              slidingPlatformY, align = 'center')
    drawLabel('<- moving platforms :D', slidingPlatformX + 100, 
              slidingPlatformY, size = 14, bold = True, 
              font = 'Ink Free', align = 'center')

def drawStartScreen(app):
        drawRect(0, 0, app.width, app.height, fill = 'white')
        drawImage(app.graphImage, app.width//2, app.height//2, 
                  align = 'center', opacity = 50)
        drawLabel('Doodle Jump!', app.width//2, 100, size = 40, 
                  bold = True, align = 'center', font = 'Ink Free')
        drawLabel("Use arrow keys or 'a' and 'd' to control your doodle :)", 
                  app.width//2, app.height//2 + 80, size = 16, align = 'center',
                    font = 'Ink Free')
        drawLabel("Press 's' to start", app.width//2, app.height//2, 
                  size = 18, align = 'center', font = 'Ink Free')
        drawLabel("Press 'p' to pause", app.width//2, app.height//2 + 20, 
                  size = 18, align = 'center', font = 'Ink Free')
        drawLabel("Press 't' to see how to play!", app.width//2, 
                  app.height//2 + 40, size = 18, align = 'center',
                   font = 'Ink Free')
        drawLabel("Press 'h' to see the high scores", app.width//2, 
                  app.height//2 + 60, size = 18, align = 'center',
                   font = 'Ink Free')
        drawLabel(f'Your high score: {int(app.highScore)}', 
                  app.width//2, 200, size = 30, align = 'center', 
                  font = 'Ink Free')
        drawImage(app.doodleJump, app.cx, app.cy, align = 'center')
        app.single.drawSingle(app.width, app.height)

def stepStartScreen(app):
    ############### DOODLE STEP ###########
        app.cy += app.scrollY
        app.dx *= 0.99
        if app.scrolling == False:
            app.cy += app.dy
            app.dy += app.ddy
        app.cx += app.dx
        app.dx += app.ddx
        # falling game over condition
        if app.cy + 20 >= app.height:
            app.gameOver = True

        if app.dy > 0: 
                for platform in app.single.location:
                    platformX = platform[0]
                    platformY = platform[1]
                    leftBound = platformX - app.normalPlatform.imageWidth//15 
                    rightBound = platformX + app.normalPlatform.imageWidth//15


                    if ((app.cx > leftBound) and (app.cx < rightBound)and 
                        (platformY - app.cy >= 0)  and (platformY - app.cy <= 22)): 
                        app.dy = -6
                        app.scrolling = False

def main():
    runApp(width=400,height=600)

class Platform:
    def __init__(self, initX, initY, pathToImage, monsterProbability, portalProbability):
        self.image = Image.open(pathToImage) # I drew this myself :)
        # self.movingPlatform = Image.open('TP_Images/moving platform.png') # I drew this myself :)
        # self.cloudPlatform = Image.open('TP_Images/cloud platform.png') # I drew this myself :)
        self.imageWidth, self.imageHeight = self.image.width, self.image.height
        ## Resizing Images : https://pillow.readthedocs.io/en/stable/reference/Image.html
        self.image = self.image.resize((self.imageWidth//10, self.imageHeight//10))
        self.image = CMUImage(self.image)
        self.location = [[initX, initY, 0, 0]] 
        # width, height, movement (monster presence), jitter initial direction
        self.monsterProbability = monsterProbability
        self.portalProbability = portalProbability
        self.monsterList = []
        self.portalList = []

        self.teleportationDistance = 500

    def drawSingle(self, canvasWidth, canvasHeight):
        for platform in self.location:
            platformX = platform[0]
            platformY = platform[1]
            drawImage(self.image, platformX, platformY, align = 'center')
    
    def draw(self, canvasWidth, canvasHeight, difficulty, monsterProbability):
        self.generate(canvasWidth, canvasHeight, difficulty, monsterProbability) 
        self.drawSingle(canvasWidth, canvasHeight)

    def generate(self, canvasWidth, canvasHeight, difficulty, monsterProbability):
        lastPlatformY = self.location[-1][1]
        firstPlatformY = self.location[0][1]
        if lastPlatformY > 0:
            direction = [-1, 1]
            monster = randint(0, monsterProbability)
            dx = direction[randint(0, 1)]
            nextPlatformY = randint(rounded(lastPlatformY - 100 - 
                difficulty*10), rounded(lastPlatformY - 60 - difficulty * 10))
            nextPlatformX = randint(0, canvasWidth)
            self.location.append([nextPlatformX, nextPlatformY, dx, dx])

            if monster == 0: ## if the integer is 0, we intialize a monster class
                self.monsterList.append(Monster(nextPlatformX, nextPlatformY - 30))

            portal = randint(0, self.portalProbability)
            if portal == 0:
                self.portalList.append(Portal(nextPlatformX, 
                    nextPlatformY - 35, self.teleportationDistance))

        if firstPlatformY > canvasHeight:
            self.location.pop(0)
            

    def scroll(self, scrollY):
        for platform in self.location:
            platform[1] += scrollY
        for monster in self.monsterList:
            monster.cy += scrollY

    def moveSideways(self, canvasWidth):
        for platform in self.location:
            if platform[0] == 0:
                platform[2] = 1
            if platform[-0] == canvasWidth:
                platform[2] = -1
            platform[0] += platform[2]

    def jitter(self, canvasWidth):
        direction = [-1, 1]
        for platform in self.location:
            if platform[3] == 0:
                dx= 0
            if platform[3] == -1:
                dx = -2
            if platform[3] == 1:
                dx = 2
            platform[0] += dx
            platform[3] *= -1

    def disappear(self, platformIndex):
        self.location.pop(platformIndex)

    def drawMonster(self):
        for monster in self.monsterList:
            monster.draw()

    def monsterStep(self, doodleX, doodleY):
        for monster in self.monsterList:
            leftBound = monster.cx - 35
            rightBound = monster.cx + 35
            lowerBound = monster.cy - 35
            upperBound = monster.cy + 35
            if (leftBound < doodleX) and (doodleX < rightBound) and\
                (lowerBound < doodleY) and (doodleY < upperBound):
                return True

class Monster:
    def __init__(self, cx, cy):
        self.image = Image.open('TP_Images/pudding.png') # Kailey x Hua SCS 27
        self.imageWidth, self.imageHeight = self.image.width, self.image.height
        ## Resizing Images : https://pillow.readthedocs.io/en/stable/reference/Image.html
        self.image = self.image.resize((self.imageWidth//25, self.imageHeight//25))
        self.image = CMUImage(self.image)
        self.cx = cx
        self.cy = cy

    def draw(self):
        drawImage(self.image, self.cx, self.cy, align = 'center')

########### PROJECTILES ##########

class Projectile:
    def __init__(self, doodleX, doodleY, mouseX, mouseY, radius, speed, pathToImage):
        self.cx = doodleX
        self.cy = doodleY
        self.radius = radius
        self.speed = speed
        slope = self.slope(doodleX, doodleY, mouseX, mouseY, self.speed)
        self.dx = slope[0]
        self.dy = slope[1]

        ### projectile image

        self.image = Image.open(pathToImage) 
        self.imageWidth, self.imageHeight = self.image.width, self.image.height
        self.image = self.image.resize((self.imageWidth//8, self.imageHeight//8))
        self.image = CMUImage(self.image)
        pass

    def drawProjectile(self):
        drawImage(self.image, self.cx, self.cy)
        pass

    def slope(self, doodleX, doodleY, mouseX, mouseY, bulletSpeed): 
        # initial point -> target point
        dx = doodleX - mouseX
        dy = doodleY - mouseY
        magnitude = math.sqrt(dx**2 + dy**2)
        dx *= (bulletSpeed/magnitude)
        dy *= (bulletSpeed/magnitude)
        return [dx, dy]
    
    def scroll(self, scrollY):
        self.cy += scrollY
        
    def moveProjectile(self):
        self.cx -= self.dx
        self.cy -= self.dy

class Portal:
    def __init__(self, selfX, selfY, teleportDistance):
        # initialize portal image 
        self.image = Image.open('TP_Images/portal.png') ## Gene Yang, SCS 27 (112>122)
        self.imageWidth, self.imageHeight = self.image.width, self.image.height
        self.image = self.image.resize((self.imageWidth//18, self.imageHeight//18))
        self.image = CMUImage(self.image)

        self.cx = selfX
        self.cy = selfY
        self.teleportDistance = teleportDistance

    def draw(self):
        drawImage(self.image, self.cx, self.cy, align = 'center')

    def teleport(self, doodleX, doodleY, screenWidth):
        newX = randint(10, screenWidth-1)
        dy = randint(100, self.teleportDistance)
        newY = doodleY - dy
        return [newX, newY]
    
    def scroll(self, scrollY):
        self.cy += scrollY

main()