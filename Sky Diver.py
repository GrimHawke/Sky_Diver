import random, pygame, sys, time, math
from pygame.locals import *
#to do: images

FPS = 60
BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
RED   = (255,   0,   0)
GREEN = (  0, 255,   0)
BLUE  = (  0,   0, 255)
GRAY =  (128, 128, 128)
PURPLE = ( 128, 0, 128)
pygame.mixer.init()
splat = pygame.mixer.Sound('splat.wav')
splat.set_volume(0.3)
fanfare = pygame.mixer.Sound('fanfare.wav')
fanfare.set_volume(0.3)
pygame.mixer.music.load('clouds castle.wav')
pygame.mixer.music.play(-1, 0.0)
pygame.mixer.music.set_volume(0.25)

def main():
    global FPSCLOCK, DISPLAYSURF
    pygame.init()
    pygame.font.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((1000, 800))
    pygame.display.set_caption('Sky Diver')
    value = [1]
    stage = 1
    score = 0
    while True:
        if value[0] == 1:
            value = mainmenu()
            score = 0
        elif value[0] == 2 and stage < 6:
            stage += 1
            hold = runGame(score)
            if hold >= 0:
                score += hold
            else:
                value = [1]
        elif value[0] == 2 and stage == 6:
            endgame(score)
            value[0] = 1
            stage = 1
        elif value[0] == 3:
            value = tutorial()

def runGame(cur_score):
    score = cur_score
    plane1 = Plane()
    wind1 = Wind()
    ground = Background()
    target = Target()
    dash = Dashboard(wind1, score)
    diver = False
    count = 0
    pause_menu = menu2()
    pause = False
    pressed = pygame.key.get_pressed()
    while True:
        for event in pygame.event.get():
            pressed = pygame.key.get_pressed()
            if pressed[K_p]:
                pause = not pause
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        if not pause:
            count+=1
            DISPLAYSURF.fill(WHITE)
            ground.draw()
            target.draw()
            dash.update(wind1, diver if diver else plane1)
            if count == 6:
                count = 0
                wind1.update()
            plane1.update()
            if diver:
                if diver.z > 0:
                    diver.update(wind1)
                else:
                    if diver.scale > 0.9:
                        diver.img = pygame.image.load('splat.png')
                        diver.img.set_colorkey(WHITE)
                        diver.shadow = pygame.image.load('shadow2.png')
                        diver.shadow.set_colorkey(WHITE)
                    diver.draw()
                    return diver.check(target)
            if plane1.x >= 1000 and not diver:
                diver = Diver(plane1)
                return diver.check(target)
            if pressed[K_z]:
                if not diver:
                    diver = Diver(plane1)
            elif pressed[K_x]:
                if diver:
                    diver.parachute = True
                    diver.img = pygame.image.load('diver2.png')
                    diver.img.set_colorkey(WHITE)
            if pressed[K_UP] or pressed[K_DOWN]:
                if pressed[K_UP]:
                    plane1.velo = 5
                elif pressed[K_DOWN]:
                    plane1.velo = -5
            else:
                plane1.velo = 0
            if pressed[K_RIGHT]:
                plane1.velo2 = 1
            else:
                plane1.velo2 = 0
        else:
            hold = pause_menu.update()
            if hold[0] and pause:
                pause = False
            if hold[1]:
                return -1
        FPSCLOCK.tick(FPS)
        pygame.display.update()

def tutorial():
    ground = Background()
    score = 0
    plane1 = Plane()
    wind1 = Wind(5, 0, 90)
    ground = Background()
    target = Target()
    target.change(700, 500)
    dash = Dashboard(wind1, score)
    diver = Diver(plane1)
    count = 0
    pause_menu = menu2()
    stage = 0 #change this back to 0
    pause = False
    pressed = False
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN or event.type == MOUSEBUTTONDOWN:
                pressed = True
        DISPLAYSURF.fill(WHITE)
        ground.draw()
        target.draw()
        dash.update(wind1, diver if diver else plane1)
        if stage == 0:
            plane1.change(500, 200)
            diver.change(550, 500, 170, True)
            displayText(500, 300, "Welcome to Sky Diver Tutorial!", BLACK, 32)
            displayText(500, 340, "Press any key to continue", BLACK, 32)
            if pressed:
                stage += 1
                pressed = False
        elif stage == 1:
            displayText(500, 300, "The objective of this game is to", BLACK, 32)
            displayText(500, 340, "land your skydiver on this target safely", BLACK, 32)
            hold = pygame.image.load('arrow.png')
            hold.set_colorkey(WHITE)
            #hold = pygame.transform.rotate(hold, -90)
            DISPLAYSURF.blit(hold, (450, 530))
            if pressed:
                stage += 1
                pressed = False
        elif stage == 2:
            displayText(500, 300, "These indicators show wind direction,", BLACK, 32)
            displayText(500, 340, "wind speed, and your fall speed", BLACK, 32)
            hold = pygame.image.load('arrow.png')
            hold.set_colorkey(WHITE)
            hold = pygame.transform.rotate(hold, -90)
            DISPLAYSURF.blit(hold, (265, 500))
            #arrows to display
            if pressed:
                stage += 1
                pressed = False
        elif stage == 3:
            displayText(500, 300, "Use the up and down arrow keys to move you plane", BLACK, 32)
            displayText(500, 340, "Use the right arrow key to speed up your plane", BLACK, 32)
            hold = pygame.image.load("arrow2.png")
            hold.set_colorkey(WHITE)
            hold1 = pygame.transform.rotate(hold, -90)
            hold2 = pygame.transform.rotate(hold, 90)
            DISPLAYSURF.blit(hold, (620, 100))
            DISPLAYSURF.blit(hold1, (500, 160))
            DISPLAYSURF.blit(hold2, (500, 15))
            #display directions
            if pressed:
                stage += 1
                pressed = False
        elif stage == 4:
            displayText(500, 320, "Use the z key to have your sky diver jump", BLACK, 32)
            plane1.change(300, 500)
            diver.change(350, 500, 400, False)
            if pressed:
                stage += 1
                pressed = False
        elif stage == 5:
            displayText(500, 300, "Use the x key to deploy your parachute", BLACK, 32)
            displayText(500, 340, "The parachute slows you down and makes you", BLACK, 32)
            displayText(500, 380, "more vulnerable to being blown by the wind", BLACK, 32)
            diver.change(350, 500, 400, True)
            if pressed:
                stage += 1
                pressed = False
        elif stage == 6:
            diver2 = Diver(plane1)
            diver2.change(500, 400, 0, True)
            diver2.img = pygame.image.load('splat.png')
            diver2.img.set_colorkey(WHITE)
            diver2.shadow = pygame.image.load('shadow2.png')
            diver2.shadow.set_colorkey(WHITE)
            diver.change(700, 600, 0, True)
            diver2.draw()
            displayText(500, 300, "You get points for landing on the target at low speeds", BLACK, 32)
            displayText(500, 340, "Be sure not to be falling too fast or you'll die!", BLACK, 32)
            #display diver on target and dead diver
            if pressed:
                stage += 1
                pressed = False
        elif stage == 7:
            displayText(500, 320, "Good luck and have fun!", BLACK, 36)
            if pressed:
                return [1]
        plane1.draw()
        diver.draw()
        FPSCLOCK.tick(FPS)
        pygame.display.update()

class Background():
    def __init__(self):
        self.img = pygame.image.load('background.png')

    def draw(self):
        DISPLAYSURF.blit(self.img, (0,0))
##        pygame.draw.line(DISPLAYSURF, BLACK, (0,650), (100,500), 1)
##        pygame.draw.line(DISPLAYSURF, BLACK, (100,500), (1000,500), 1)
##        pygame.draw.line(DISPLAYSURF, BLACK, (1000,500), (900,650), 1)
##        pygame.draw.line(DISPLAYSURF, BLACK, (900,650), (0,650), 1)
##
##        pygame.draw.line(DISPLAYSURF, BLACK, (0,150), (100,0), 1)
##        pygame.draw.line(DISPLAYSURF, BLACK, (100,0), (1000,0), 1)
##        pygame.draw.line(DISPLAYSURF, BLACK, (1000,0), (900,150), 1)
##        pygame.draw.line(DISPLAYSURF, BLACK, (900,150), (0,150), 1)

class button(object):
    def __init__(self, text, x, y, xlen, ylen, fontsize):
        self.fontObj = pygame.font.Font('freesansbold.ttf', fontsize)
        self.text = self.fontObj.render(text, True, WHITE)
        self.rect = self.text.get_rect()
        self.rect.center = (x,y)
        self.xlen = xlen
        self.ylen = ylen
        self.color = RED

    def draw(self):
        pygame.draw.rect(DISPLAYSURF, self.color, (self.rect.center[0] - self.xlen/2, self.rect.center[1]- self.ylen/2, self.xlen, self.ylen))
        DISPLAYSURF.blit(self.text, self.rect)

    def check(self):
        coord = pygame.mouse.get_pos()
        if coord[0] >= self.rect.center[0]-self.xlen/2 and coord[0] <= self.rect.center[0]+self.xlen/2 and coord[1] >= self.rect.center[1]-self.ylen/2 and coord[1] <= self.rect.center[1]+self.ylen/2:
            self.color = GREEN
            if pygame.mouse.get_pressed()[0]:
                return True
        else:
            self.color = RED
        return False

    def update(self):
        self.draw()
        return self.check()

class Cloud():
    def __init__(self):
        self.img = pygame.image.load('cloud.png')
        self.img.set_colorkey(PURPLE)
        self.x = 1100
        self.y = random.randrange(90, 710)
        self.rect = self.img.get_rect(center = (self.x, self.y))
        self.velo = random.randrange(-20, -5)/10.0

    def draw(self):
        DISPLAYSURF.blit(self.img, self.rect)

    def update(self):
        self.x += self.velo
        self.rect = self.img.get_rect(center = (self.x, self.y))

class menu1():
    def __init__(self):
        self.img = pygame.image.load('title.png')
        self.rect = self.img.get_rect(center = (500, 160))
        self.img.set_colorkey(WHITE)
        self.button_start = button('Play Game', 800, 500, 200, 80, 26)
        self.button_tutor = button('Tutorial', 800, 580, 200, 80, 26)
        self.button_quit = button('Quit', 800, 660, 200, 80, 26)
        self.last_cloud = 0

    def update(self):
        DISPLAYSURF.blit(self.img, self.rect)
        return [self.button_start.update(), self.button_tutor.update(), self.button_quit.update()]

class menu2():
    def __init__(self):
        self.button_resume = button('Resume', 500, 250, 200, 80, 26)
        self.button_quit = button('Quit', 500, 400, 200, 80, 26)

    def update(self):
        return [self.button_resume.update(), self.button_quit.update()]

def mainmenu():
    start_menu = menu1()
    cloudlist = list()
    last_cloud = 0
    while True:
        #pygame.draw.rect(DISPLAYSURF, (192,192,255), (0,0,1000,800))
        DISPLAYSURF.fill((192,192,255))
        if pygame.time.get_ticks() - last_cloud >= 2000 and len(cloudlist) < 7:
            cloudlist.append(Cloud())
            last_cloud = pygame.time.get_ticks()
        for thing in cloudlist:
            thing.update()
            thing.draw()
            if thing.x <= -100:
                cloudlist.remove(thing)
                last_cloud = pygame.time.get_ticks()
        hold = start_menu.update()
        if hold[0]:
            return [2]
        elif hold[1]:
            return [3]
        elif hold[2]:
            pygame.quit()
            sys.exit()
        FPSCLOCK.tick(FPS)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

def displayText(x,y,text,color, size):
    fontObj = pygame.font.Font('freesansbold.ttf', size)
    textSurfaceObj = fontObj.render(text, True, color)
    textRectObj = textSurfaceObj.get_rect()
    textRectObj.center = (x, y)
    DISPLAYSURF.blit(textSurfaceObj, textRectObj)

def endgame(score):
    DISPLAYSURF.fill(BLACK)
    displayText(500, 300, "Game over", WHITE, 30)
    displayText(500, 360, "Score: " + str(score), WHITE,30)
    displayText(500, 750, "Press any key to return to main menu", WHITE,26)
    pygame.display.update()
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                return

class Dashboard():
    def __init__(self, wind, score):
        self.game_score = score
        
        self.compass = pygame.image.load('compass.png')
        self.c_pin = pygame.image.load('compass_pin.png')
        self.compass.set_colorkey(WHITE)
        self.c_pin.set_colorkey(WHITE)
        self.const_pin = self.c_pin.copy()
        self.compass_rect = self.compass.get_rect(center = (400,725))
        self.pin_rot = 0
        self.pin_rect1 = self.c_pin.get_rect(center = (400, 725))

        self.altitude = pygame.image.load('speed.png')
        self.a_pin = pygame.image.load('altitude_pin.png')
        self.altitude.set_colorkey(WHITE)
        self.a_pin.set_colorkey(WHITE)
        self.alt_rect = self.altitude.get_rect(center = (140,725))
        self.pin_displace = 0
        self.pin_rect2 = self.a_pin.get_rect(center = (140,725+self.pin_displace))

        self.wind_level = int(wind.velo/2.01)
        self.wind = pygame.image.load('wind_' + str(self.wind_level) + '.png')
        self.wind.set_colorkey(WHITE)
        self.wind_rect = self.wind.get_rect(center = (660,725))

    def update(self, wind, diver):
        pygame.draw.rect(DISPLAYSURF, GRAY, (0,650,1000,150))
        self.pin_rot = wind.direc
        self.const_pin = pygame.transform.rotate(self.c_pin, -self.pin_rot)
        self.pin_rect1 = self.const_pin.get_rect(center = (400, 725))
        DISPLAYSURF.blit(self.compass, self.compass_rect)
        DISPLAYSURF.blit(self.const_pin, self.pin_rect1)
        displayText(300, 710, "Wind", BLACK, 18)
        displayText(300, 730, "Direction", BLACK, 18)

        self.pin_displace = (500-diver.scale*1250/3)/5.9
        self.pin_rect2 = self.a_pin.get_rect(center = (140,725+self.pin_displace))
        DISPLAYSURF.blit(self.altitude, self.alt_rect)
        DISPLAYSURF.blit(self.a_pin, self.pin_rect2)
        displayText(70, 710, "Fall", BLACK, 18)
        displayText(70, 730, "Speed", BLACK, 18)
        
        hold = int(wind.velo/2.01)
        if hold != self.wind_level:
            self.wind_level = hold
            self.wind = pygame.image.load('wind_' + str(self.wind_level) + '.png')
            self.wind.set_colorkey(WHITE)
        DISPLAYSURF.blit(self.wind, self.wind_rect)
        displayText(900, 770, "Score: " + str(self.game_score), BLACK, 30)
        displayText(580, 710, "Wind", BLACK, 18)
        displayText(580, 730, "Speed", BLACK, 18)

class Plane():
    def __init__(self):
        self.x = 50
        self.y = random.randrange(175,825)
        self.z = 500
        self.velo = 0
        self.velo2 = 0
        self.img = pygame.image.load('plane2.png')
        self.img.set_colorkey((255,255,254))
        self.scale = 1.2
        self.rect = self.img.get_rect(center = (self.x*900/1000 + self.y*100/1000, (1000-self.y)*150/1000 + 500 - self.z))

    def change(self, x, y):
        self.x = x
        self.y = y
        self.rect = self.img.get_rect(center = (self.x*900/1000 + self.y*100/1000, (1000-self.y)*150/1000 + 500 - self.z))

    def draw(self):
        DISPLAYSURF.blit(self.img, self.rect)

    def update(self):
        self.x += 1 + self.velo2
        self.y += self.velo
        self.rect = self.img.get_rect(center = (self.x*900/1000 + self.y*100/1000, (1000-self.y)*150/1000 + 500 - self.z))
        if self.y <= 175:
            self.y = 175
        elif self.y >= 825:
            self.y = 825
        self.draw()

class Diver():
    def __init__(self, plane):
        self.x = plane.x
        self.y = plane.y
        self.z = plane.z - 10
        self.scale = 1.2
        self.img = pygame.image.load('diver1.png')
        self.img.set_colorkey(WHITE)
        self.rect = self.img.get_rect(center = (self.x*900/1000 + self.y*100/1000, (1000-self.y)*150/1000 + 500 - self.z))
        self.parachute = False
        self.shadow = pygame.image.load('shadow.png')
        self.shadow.set_colorkey(WHITE)
        self.rect2 = self.img.get_rect(center = (self.x*900/1000 + self.y*100/1000, (1000-self.y)*150/1000 + 500))

    def change(self, x, y, z, chute):
        self.x = x
        self.y = y
        self.z = z
        self.parachute = chute
        self.rect = self.img.get_rect(center = (self.x*900/1000 + self.y*100/1000, (1000-self.y)*150/1000 + 500 - self.z))
        self.rect2 = self.img.get_rect(center = (self.x*900/1000 + self.y*100/1000, (1000-self.y)*150/1000 + 500))
        if self.parachute:
            self.img = pygame.image.load('diver2.png')
        else:
            self.img = pygame.image.load('diver1.png')

    def draw(self):
        self.img.set_colorkey(WHITE)
        DISPLAYSURF.blit(self.shadow, self.rect2)
        DISPLAYSURF.blit(self.img, self.rect)

    def check(self, target):
        points = 0
        holdx = self.x*9/10 + self.y/10
        holdy = (1000-self.y)*150/1000 + 520
        targetx = target.rect.center[0]
        targety = target.rect.center[1]
        if (holdx+75-targetx >= 0 and holdx-75-targetx <= 0) and (holdy + 35 - targety >= 0 and holdy - 35 - targety <= 0 and self.scale <= 0.9):
            fanfare.play()
            if self.scale <= 0.3:
                points = 50
            elif self.scale <= 0.9:
                points = int(50*(1.3-self.scale))
            displayText(500, 340, "POINTS GET", BLACK, 50)
            displayText(500, 385, "+" + str(points) + " Points", BLACK, 44)
            pygame.display.update()
            pygame.time.delay(3000)
            return points
        elif self.z != 0:
            displayText(500, 400, "YOU FAIL", BLACK, 70)
            pygame.display.update()
            pygame.time.delay(3000)
            return 0
        else:
            if self.scale > 0.9:
                splat.play()
            displayText(500, 400, "YOU FAIL", BLACK, 70)
            pygame.display.update()
            pygame.time.delay(3000)
            return 0

    def update(self, wind):
        self.z -= self.scale + 1
        if self.parachute and self.scale > 0:
            self.scale -= 0.01
        self.x+= math.sin(math.radians(wind.direc))*(0.15-self.scale/18)*wind.velo
        self.y+= math.cos(math.radians(wind.direc))*(0.15-self.scale/18)*wind.velo

        if self.x <= 0:
            self.x = 0
        elif self.x >= 950:
            self.x = 950
        
        if self.y <= 175:
            self.y = 175
        elif self.y >= 825:
            self.y = 825

        self.rect = self.img.get_rect(center = (self.x*900/1000 + self.y*100/1000, (1000-self.y)*150/1000 + 500 - self.z))
        self.rect2 = self.img.get_rect(center = (self.x*900/1000 + self.y*100/1000, (1000-self.y)*150/1000 + 500))
        self.draw()
        if self.z <= 0:
            self.z = 0

class Target():
    def __init__(self):
        self.x = random.randrange(500, 900)
        self.y = random.randrange(250, 750)
        self.z = 0
        self.img = pygame.image.load('target2.png')
        self.img.set_colorkey(WHITE)
        self.rect = self.img.get_rect(center = (self.x*900/1000 + self.y*100/1000, (1000-self.y)*150/1000 + 500 - self.z))

    def change(self, x, y):
        self.x = x
        self.y = y
        self.rect = self.img.get_rect(center = (self.x*900/1000 + self.y*100/1000, (1000-self.y)*150/1000 + 500 - self.z))
    
    def draw(self):
        DISPLAYSURF.blit(self.img, self.rect)

class Wind():
    def __init__(self, velo = random.randrange(0,7), accel = random.randrange(-3,4)/10, direc = random.randrange(0,360)):
        self.velo = velo
        self.accel = accel
        self.direc = direc
        
    def update(self):
        self.velo += self.accel
        if self.velo > 6:
            self.velo = 6
        elif self.velo < 0:
            self.velo = abs(self.velo)
            self.direc = self.direc + 180
            self.accel = -self.accel
        
        self.accel += random.randrange(-1,2)/15.0
        
        if self.accel < -0.3:
            self.accel = -0.3
        if self.accel > 0.3:
            self.accel = 0.3
        
        self.direc+= random.randrange(-5,6)
        if self.direc < 0:
            self.direc+= 360
        elif self.direc > 360:
            self.direc-= 360
        
    def __str__(self):
        return str((self.velo, self.accel))

if __name__ == '__main__':
    main()
