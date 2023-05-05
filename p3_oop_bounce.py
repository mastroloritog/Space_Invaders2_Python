#!/usr/bin/env python3
'''
@author  Michele Tomaiuolo - http://www.ce.unipr.it/people/tomamic
@license This software is free - http://www.gnu.org/licenses/gpl.html
'''

import random
from time import time, sleep
from actor import Actor, Arena
import g2d

class Ball(Actor):
    def __init__(self, pos):
        self._x, self._y = pos
        self._w, self._h = 255-170, 107-48
        self._speed = 2
        self._dx, self._dy = self._speed, self._h-self._speed
        self._xmin, self._xmax = self._x, self._x + 600
        self._myList = [0, 5, 10, 15, 20, 25]
        self._myList2 = [0, 2, 4, 6, 8, 10]
        self._myList3 = [0, 3, 6, 9, 12]
        self._startTime = time() + random.choice(self._myList)   #  appena l'oggetto viene creato prende l'orario di adesso
        self._endTime = 0          #
        self._visible = 0
        
        self._startChange = time()
        self._endChange = 0

    def move(self, arena: Arena):
        arena_w, arena_h = arena.size()
        self._endChange = time()
        if (self._endChange-self._startChange > 0 and self._endChange-self._startChange < 1):
            self._visible = 0
        elif (self._endChange-self._startChange > 1 and self._endChange-self._startChange < 2):
            self._visible = 1
        elif (self._endChange-self._startChange > 2 and self._endChange-self._startChange < 3):
            self._visible = 2
        elif (self._endChange-self._startChange > 3 and self._endChange-self._startChange < 4):
            self._visible = 1
        elif (self._endChange-self._startChange > 4 and self._endChange-self._startChange < 5):
            self._startChange = time()
        

        if (self._x + self._dx < self._xmin or self._x + self._dx + self._w > self._xmax):
            self._y += self._dy
            self._dx = -self._dx
        else:
            self._x += self._dx
        
        self._endTime = time()     # quando premiamo freccia su prende di nuovo il tempo di adesso
        if (self._endTime - self._startTime >= random.choice(self._myList2)):   # se il tempo preso quando abbiamo cliccato freccia su meno il tempo preso quando l'oggetto è stato creato è maggiore di 1 secondo
            arena.spawn(AlienRocket((self._x + 12, self._y + 15)))
            self._startTime = self._endTime + random.choice(self._myList3)

    def collide(self, other: Actor, arena: Arena):
#         return   # per non far collidere le palline
        if isinstance(other, Rocket):
            arena.update_pt()
            arena.kill(self)
            g2d.load_audio("alienDeath.mp3")
            g2d.play_audio("alienDeath.mp3", False)

    def pos(self):
        return self._x, self._y

    def size(self):
        return self._w, self._h

    def sprite(self):
        if (self._visible == 1):
            return 135, 174
        elif (self._visible == 2):
            return 218, 174
        else:
            return 198, 52   # in base alla posizione icona nel png


class Ghost(Actor):
    def __init__(self, pos):
        self._x, self._y = pos
        self._w, self._h = 20, 20
        self._visible = True

    def move(self, arena: Arena):
        aw, ah = arena.size()
        dx = choice([-4, 0, 4])
        dy = choice([-4, 0, 4])
        self._x = (self._x + dx) % aw
        self._y = (self._y + dy) % ah

        if random.randrange(100) == 0:
            self._visible = not self._visible

    def collide(self, other: Actor, arena: Arena):
        pass

    def pos(self):
        return self._x, self._y

    def size(self):  # da cambiare
        return self._w, self._h

    def sprite(self):
        if self._visible:
            return 20, 0
        return 20, 20

    def visible(self):
        return self._visible

class Turtle(Actor):
    def __init__(self, pos):     # init viene chiamato solo una volta alla creazine dell'oggetto
        self._x, self._y = pos
        self._dx, self._dy = 0, 0
        self._w, self._h = 93-57, 108-67
        self._speed = 10
        self._lives = 3
        self._blinking = 0
        self._startTime = time()   #  appena l'oggetto viene creato prende l'orario di adesso
        self._endTime = 0          #

    def move(self, arena: Arena):
        keys = arena.current_keys()
        self._dx = self._dy = 0
        if "ArrowUp" in keys:
            self._endTime = time()     # quando premiamo freccia su prende di nuovo il tempo di adesso
            if (self._endTime - self._startTime >= 0.5):   # se il tempo preso quando abbiamo cliccato freccia su meno il tempo preso quando l'oggetto è stato creato è maggiore di 1 secondo
                arena.spawn(Rocket((self._x + 12, self._y - 30)))
                self._startTime = self._endTime   # il tempo di inizio del prossimo proiettile sarà il tempo di fine di quello precedente
        if "ArrowLeft" in keys:
            self._dx = -self._speed
        elif "ArrowRight" in keys:
            self._dx = self._speed
        self._x += self._dx
        #Spacebar
        
        aw, ah = arena.size()
        self._x = min(max(self._x, 0), aw - self._w)  # clamp
        self._y = min(max(self._y, 0), ah - self._h)  # clamp
        if self._blinking > 0:
            self._blinking -= 1

    def collide(self, other: Actor, arena: Arena):
        if self._blinking == 0:
            self._blinking = 60
            if isinstance(other, Ball) or isinstance(other, AlienRocket) or isinstance(other, AlienRocketFollower):
                self._lives -= 1
                g2d.load_audio("lifeLose.mp3")
                g2d.play_audio("lifeLose.mp3", False)
            if isinstance(other, MonsterWave):
                self._lives = 0
                g2d.load_audio("lifeLose.mp3")
                g2d.play_audio("lifeLose.mp3", False)
        if self._lives <= 0:
            arena.kill(self)

    def pos(self):
        return self._x, self._y

    def size(self):
        return self._w, self._h

    def sprite(self):
        if self._blinking > 0 and self._blinking % 4 <= 2:
            return None
        return 57, 67

class Wall(Actor):
    def __init__(self, pos):
        self._x, self._y = pos
        self._w, self._h = 136-25, 49-26   # grandezza pixel dell'area da ritagliare
        self._blinking = 0
        self._timeBreak = 40

    def move(self, arena: Arena):
        pass
    
    def collide(self, other: Actor, arena: Arena):
        if isinstance(other, Rocket) or isinstance(other, AlienRocket):
            self._timeBreak -= 1
            if (self._timeBreak%10 == 0):
                g2d.load_audio("rockBreaking.mp3")
                g2d.play_audio("rockBreaking.mp3", False)
        if (self._timeBreak == 0):
            arena.kill(self)
        elif isinstance(other, MonsterWave):
            arena.kill(self)
    
    def pos(self):
        return self._x, self._y

    def size(self):
        return self._w, self._h

    def sprite(self):
        if (self._timeBreak > 30 and self._timeBreak <= 40):
            return 25, 26   # punto in alto a sinistra, posizione da cui partire per il ritaglio
        if (self._timeBreak > 20 and self._timeBreak <= 30):
            return 15, 221
        if (self._timeBreak > 10 and self._timeBreak <= 20):
            return 15, 252
        else:
            return 15, 282
        
class Rocket(Actor):
    def __init__(self, pos):
        self._x, self._y = pos
        self._speed = 8
        self._w, self._h = 240-208, 161-136
        self._blinking = 0

    def move(self, arena: Arena):
        self._y -= self._speed
    
    def collide(self, other: Actor, arena: Arena):
        #pass
        if isinstance(other, Ball) or isinstance(other, AlienRocket) or isinstance(other, Wall) or isinstance(other, Boss) or isinstance(other, AlienRocketFollower):
            arena.kill(self)
    
    def pos(self):
        return self._x, self._y

    def size(self):
        return self._w, self._h

    def sprite(self):
        if self._blinking > 0 and self._blinking % 4 <= 2:
            return None
        return 208, 136

class AlienRocket(Actor):
    def __init__(self, pos):
        self._x, self._y = pos
        self._speed = 5
        self._w, self._h = 108-94, 181-138   # grandezza pixel dell'area da ritagliare
        self._blinking = 0

    def move(self, arena: Arena):
        self._y += self._speed
        if (self._y >= 820):
            arena.kill(self)
    
    def collide(self, other: Actor, arena: Arena):
        if isinstance(other, Turtle) or isinstance(other, Rocket) or isinstance(other, Wall):
            arena.kill(self)
    
    def pos(self):
        return self._x, self._y

    def size(self):
        return self._w, self._h

    def sprite(self):
        return 97, 142   # punto in alto a sinistra, posizione da cui partire per il ritaglio

class Boss(Actor):
    def __init__(self, pos, ready: bool):
        self._x, self._y = pos
        self._w, self._h = 300, 537-350
        self._speed = 15
        self._dx = self._speed
        self._dy = 8
        self._bossL = 50
        self._startTime = time()   #  appena l'oggetto viene creato prende l'orario di adesso
        self._endTime = 0          #
        self._myList = [0.2, 0.4, 0.6, 0.8]

    def move(self, arena: Arena):
        if (arena._bossAppear == True):
            self._y += self._dy
            if (self._endTime-self._startTime > random.choice(self._myList)):
                arena.spawn(AlienRocket((self._x + 100, self._y + 100)))
                self._startTime = self._endTime   # il tempo di inizio del prossimo proiettile sarà il tempo di fine di quello precedente
            self._endTime = time()  #### altrimenti alla fine del def move
            if (self._y + self._dy > 200):
                self._dy = 0
            
            self._numTrovato = random.randrange(0, 30)
            if (self._numTrovato == 0):
                arena.spawn(AlienRocketFollower((self._x + 100, self._y + 100)))
            
            self._numTrovato2 = random.randrange(0, 100)
            if (self._numTrovato2 == 0):
                arena.spawn(MonsterWave((self._x + 100, self._y + 100)))
        
        ## movimento orizzontale:
        if (self._x + self._dx < 0 or self._x + self._dx + self._w > 1200):
            #arena.haToccato = True    # quando sono tutti passati giù si resetta a false
            self._dx = -self._dx
        else:
            self._x += self._dx
        
    def collide(self, other: Actor, arena: Arena):
        #pass
        if (isinstance(other, Rocket)):
            self._bossL -= 1
            g2d.load_audio("alienDeath.mp3")
            g2d.play_audio("alienDeath.mp3", False)
        if (self._bossL == 0):
            arena.kill(self)
            arena._bossDeath = True
        
    def pos(self):
        return self._x, self._y

    def size(self):
        return self._w, self._h

    def sprite(self):
        return 0, 365   # in base alla posizione icona nel png

class AlienRocketFollower(Actor):
    def __init__(self, pos):
        self._x, self._y = pos
        self._dx = 10
        self._speed = 5
        self._w, self._h = 108-94, 181-138   # grandezza pixel dell'area da ritagliare
        self._blinking = 0

    def move(self, arena: Arena):
        self._y += self._speed
        
        self._xplayer, self._yplayer = arena._yourPosition
        
        if (self._y <= 760):
            if (self._x < self._xplayer):
                self._x += self._dx
            if (self._x > self._xplayer):
                self._x -= self._dx
        
        if (self._y >= 820):
            arena.kill(self)
    
    def collide(self, other: Actor, arena: Arena):
        if isinstance(other, Turtle) or isinstance(other, Rocket) or isinstance(other, Wall):
            arena.kill(self)
    
    def pos(self):
        return self._x, self._y

    def size(self):
        return self._w, self._h

    def sprite(self):
        return 97, 142   # punto in alto a sinistra, posizione da cui partire per il ritaglio

class MonsterWave(Actor):
    def __init__(self, pos):
        self._x, self._y = pos
        self._speed = 5
        self._w, self._h = 280-12, 366-303   # grandezza pixel dell'area da ritagliare
        self._blinking = 0

    def move(self, arena: Arena):
        self._y += self._speed
        if (self._y >= 800):
            arena.kill(self)
    
    def collide(self, other: Actor, arena: Arena):
        if isinstance(other, Turtle) or isinstance(other, Wall):
            arena.kill(self)
    
    def pos(self):
        return self._x, self._y

    def size(self):
        return self._w, self._h

    def sprite(self):
        return 12, 303   # punto in alto a sinistra, posizione da cui partire per il ritaglio


def main():
    arena = Arena((480, 360))
    arena.spawn(Ball((40, 80)))
    arena.spawn(Ball((80, 40)))
    arena.spawn(Ghost((120, 80)))

    for i in range(25):
        print_arena(arena)
        arena.move_all()

##main()  # call main to start the program


