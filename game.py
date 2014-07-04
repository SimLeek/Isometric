import pygame, sys, pytmx
from pygame.locals import *
from math import floor
import numpy as np
import math

class IsoGame:
    def __init__(self, title='Isometric'):
        pygame.init()
        
        self.fpsClk=pygame.time.Clock()

        self.WSurf=pygame.display.set_mode((800,600),HWSURFACE|DOUBLEBUF|RESIZABLE)
        self.scrW=800
        self.scrH=600
        
        pygame.display.set_caption(title)
        self.font=pygame.font.SysFont(u'arial',24)
 
        self.bg=(0,0,0)

        self.x=2922
        self.y=1696
        self.x=15*32
        self.y=15*32
        self.vx=0
        self.vy=0

        self.speed=400

        self.myRect=pygame.Rect(15*32,15*32,32,32)
        pygame.mixer.init(44100,-16,300,1024)        

    def buffLvl(self,lvl='lvl1.tmx'):
        self.tmx=pytmx.load_pygame(lvl, pixelalpha=True)
        
        self.lvlSurf=pygame.Surface((64*100,64*100))
        self.lvlSurf.fill(self.bg)

        for k in range(10):
            for i in range(100):
                for j in range(100):
                    try:
                        img=self.tmx.getTileImage(i,j,k)
                        
                        self.lvlSurf.blit(img,(3200+32*(i-j),1616+16*(i+j)-img.get_height())) 
                    except AttributeError:
                        pass
                    except TypeError:
                        pass
                    except ValueError:
                        pass

    def playSound(self,filename):
        chan=pygame.mixer.find_channel()
        if chan:
            snd=pygame.mixer.Sound(filename)
            chan.play(snd)
        else:
            print "err: not enough sound channels"

    def startMusic(self, filename='Beatdrop -Toxic (The Unforgiven).mp3'):
        pygame.mixer.music.load(filename)
        pygame.mixer.music.play(-1)
        
    def checkCollission(self,nextx,nexty):
        o=self.tmx.objectgroups

        i=self.x*.5+self.y
        j=-self.x*.5+self.y
        i2=nextx*.5+nexty
        j2=-nextx*.5+nexty
        di=i2-i
        dj=j2-j

        txr=self.myRect.x+di
        tyr=self.myRect.y+dj
        tr=pygame.Rect(txr,tyr,32,32)

        #pygame.draw.rect(self.WSurf,(255,255,255),self.myRect)

        undo=False
        for j in range(2):
            for i in o[j]:
                recto=pygame.Rect(i.x,i.y,i.width,i.height) 
                #pygame.draw.rect(self.WSurf,(255,0,0),recto)
                if tr.colliderect(recto):
                    undo=True
        for i in o[2]:
            recto=pygame.Rect(i.x,i.y,i.width,i.height)
            if tr.colliderect(recto):
                try:
                    msg=i.name+':'+i.header
                except AttributeError:
                    msg=i.name

                msgSurf=self.font.render(msg,False,(255,255,255))
                msgRect=msgSurf.get_rect()
                msgRect.topleft=(10,20)
                self.WSurf.blit(msgSurf,msgRect)
                


                

        if not  undo:
            self.myRect=tr
 
        

        self.x=(self.myRect.x-self.myRect.y)
        self.y=(self.myRect.x+self.myRect.y)/2

    def loop(self):
        while True:
            self.WSurf.fill(self.bg)  

            for event in pygame.event.get(): 
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == KEYDOWN:
                    if event.key == K_LCTRL:
                        self.speed=200
                    if event.key== K_LSHIFT:
                        self.speed=1400
                    if event.key == K_LEFT:
                        self.vx-=1
                    if event.key == K_RIGHT:
                        self.vx+=1
                    if event.key == K_UP:
                        self.vy-=1
                    if event.key == K_DOWN:
                        self.vy+=1
                    elif event.key == K_ESCAPE:
                        pygame.event.post(pygame.event.Event(QUIT))
                elif event.type ==KEYUP:
                    if event.key == K_LCTRL:
                        self.speed=400
                    if event.key== K_LSHIFT:
                        self.speed=400
                    if event.key == K_LEFT:
                        self.vx+=1
                    if event.key == K_RIGHT:
                        self.vx-=1
                    if event.key == K_UP:
                        self.vy+=1
                    if event.key == K_DOWN:
                        self.vy-=1
                elif event.type==VIDEORESIZE:
                    self.WSurf=pygame.display.set_mode(event.dict['size'],HWSURFACE|DOUBLEBUF|RESIZABLE)
                    self.scrW,self.scrH=event.dict['size']

            self.WSurf.blit(self.lvlSurf, (-self.x-3232+self.scrW/2,-self.y-1600+self.scrH/2))

            mul=1
            if self.vx!=0 and self.vy!=0:
                mul=0.70710678118

            nextx=self.x+(self.fpsClk.get_time()/1000.)*(self.vx*mul)*self.speed
            nexty=self.y+(self.fpsClk.get_time()/1000.)*(self.vy*mul)*self.speed*.5
            r=pygame.Rect(self.scrW/2-32,self.scrH/2-16,64,32)
            pygame.draw.rect(self.WSurf,(0,0,255),r)

            self.checkCollission(nextx,nexty)

            pygame.display.flip()
            self.fpsClk.tick(60)

if __name__ == '__main__':
    game=IsoGame()
    game.buffLvl()
    game.loop()













