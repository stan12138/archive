import sys,pygame
from pygame.locals import *

pygame.init()

screen = pygame.display.set_mode([800,600])
pygame.display.set_caption('Creat by 韩仪')

font=pygame.font.SysFont('simsunnsimsun',15)
flage = False
mousex = mousey = 0
movex = movey = 0
down = up = 0
downx = downy =0
upx = upy = 0
while True :
    for event in pygame.event.get() :
        if event.type == QUIT :
            pygame.quit()
            sys.exit()
        elif event.type == MOUSEMOTION :
            flage = True
            mousex,mousey = event.pos
            movex,movey = event.rel
        elif event.type == MOUSEBUTTONDOWN :
            flage = True
            down = event.button
            downx,downy = event.pos
        elif event.type == MOUSEBUTTONUP :
            flage = True
            up = event.button
            upx,upy = event.pos
    if not flage :
        text = font.render('请移动或者按下鼠标',True,[0,0,0])
        screen.fill([255,255,255])
        screen.blit(text,[310,300])
        pygame.display.update()

    if flage :
       
        screen.fill([255,255,255])
        text1 = font.render('mousex= '+str(mousex)+'     mousey='+str(mousey),True,[0,0,0])
        screen.blit(text1,[310,100])
        text2 = font.render('movex= '+str(movex)+'     movey='+str(movey),True,[0,0,0])
        screen.blit(text2,[310,200])
        text3 = font.render('down= '+str(down)+'     up='+str(up),True,[0,0,0])
        screen.blit(text3,[310,300])
        text4 = font.render('downx= '+str(downx)+'     downy='+str(downy),True,[0,0,0])
        screen.blit(text4,[310,400])
        text5 = font.render('upx= '+str(upx)+'     upy='+str(upy),True,[0,0,0])
        screen.blit(text5,[310,500])
        
        pygame.display.update()
        
    
        
