#!/usr/bin/env python3
'''
@author  Michele Tomaiuolo - http://www.ce.unipr.it/people/tomamic
@license This software is free - http://www.gnu.org/licenses/gpl.html
'''

import g2d
from random import randrange, choice
from p3_oop_bounce import Arena, Ball, Ghost, Turtle, Wall, Boss

arenaSize = 1200, 910
arena = Arena(arenaSize)


rowsY = (0, 70, 140, 210, 280, 350, 420)
columnsX = (0, 70, 140, 210, 280, 350, 420, 490, 560, 630)
for i in columnsX:
    for j in rowsY:
        arena.spawn(Ball((i, j)))


arena.spawn(Wall((120, 765)))
arena.spawn(Wall((320, 765)))
arena.spawn(Wall((520, 765)))
arena.spawn(Wall((720, 765)))
arena.spawn(Wall((920, 765)))

arena.spawn(Turtle((0, 815)))

arena.spawn(Boss((0, -200), False))

#############################################################################################################################################

def tick():
    arena.tick(g2d.current_keys())  # Game logic
    
    lives = 0
    pts = arena.get_pt()
    nAlien = False
    #bossAlive = False
    #g2d.clear_canvas()
    
    g2d.set_color((0, 0, 0))
    g2d.fill_rect((0, 0), arenaSize)
    g2d.set_color((0, 255, 0))
    g2d.draw_line((0, 865), (1200, 865))
    
    for a in arena.actors():    #arena.actors()
        if (isinstance(a, Turtle)):
            lives = a._lives
            arena._yourPosition = a.pos()
            #print(str(arena._yourPosition))
        if (isinstance(a, Ball)):
            nAlien = True
        if a.sprite() != None:
            g2d.draw_image_clip("personaggi.png", a.pos(), a.sprite(), a.size())
        else:
            pass
    
    g2d.set_color((255, 255, 255))
    g2d.draw_text("Lifes: " + str(lives), (10, 875), 30)
    g2d.set_color((255, 255, 255))
    g2d.draw_text("Score: " + str(pts), (100, 875), 30)
    
    #nAlien = False
    if(nAlien == False):
        arena._bossAppear = True
        if (arena._bossDeath == True):
            g2d.set_color((0, 0, 0))
            g2d.fill_rect((0, 0), arenaSize)
            g2d.set_color((255, 255, 255))
            g2d.draw_text_centered("GAME OVER: WIN", (600, 450), 70)
            
            for a in arena.actors():   # toglie tutti gli actor in modo che il gioco non continui in schermata
                if not isinstance(a, Turtle):
                    arena.kill(a)
    if(lives == 0):
        #red = randrange(0, 256)
        #green = randrange(0, 256)
        #blue = randrange(0, 256)
        g2d.set_color((0, 0, 0))
        g2d.fill_rect((0, 0), arenaSize)
        g2d.set_color((255, 255, 255))
        g2d.draw_text_centered("GAME OVER: LOSE", (600, 450), 70)
        
        for a in arena.actors():
            arena.kill(a)
        

def main():
    g2d.init_canvas(arena.size())
    g2d.load_audio("gameMusic.mp3")
    g2d.play_audio("gameMusic.mp3", True)
    g2d.main_loop(tick)

main()
