import pygame,sys
from random import randint
pygame.init()

screentitle=pygame.display.set_caption('第一个')
screen=pygame.display.set_mode([800,600])
screen.fill([0,230,200])
for i in range(20) :
       circler=randint(0,255)
       circleg=randint(0,255)
       circleb=randint(0,255)
       circlex=randint(0,600)
       circley=randint(0,600)
       circle2r=randint(3,500)
       pygame.draw.circle(screen,[circler,circleg,circleb],[circlex,circley],circle2r,3)
pygame.draw.circle(screen,[255,0,255],[100,200],50,0)
pygame.draw.rect(screen,[0,0,0],[650,560,150,40],0)       
pygame.display.flip()
while True :
    for event in pygame.event.get() :
        if event.type == pygame.QUIT :
            pygame.quit()
            sys.exit()
    
