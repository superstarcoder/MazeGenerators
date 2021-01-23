import pygame
import random

#screen = pygame.display.set_mode((0,0), pygame.RESIZABLE)
#infoObject = pygame.display.Info()
#width = infoObject.current_w
#height = infoObject.current_h
#size = (width, height) #1920, 1080
#screen = pygame.display.set_mode(size, pygame.FULLSCREEN)
width = 800
height = 800
screen = pygame.display.set_mode((800,800))



#width=500; height=500
#size = (width, height) #1920, 1080
#screen = pygame.display.set_mode(size, pygame.RESIZABLE)

clock = pygame.time.Clock()
pygame.init()

#colors
BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (209, 41, 41)
BLUE = (1, 38, 249)
YELLOW = (255, 242, 0)
GREEN = (5, 186, 29)
GREY = (20, 20, 20)

done=False; doneGen=False

s=20; xs=0; ys=0; x=xs; y=ys
cleared=[];leading=[[x,y]]

def renderText(myText, myFont, mySize, myColor, pos, center=False, dis=(0,0)):
	font = pygame.font.SysFont(myFont, mySize, True, False)
	text = font.render(myText, True, myColor)
	if center:
		width2 = 0.5 * text.get_rect().width
		height2 = 0.5 * text.get_rect().height
		screen.blit(text, (width/2-width2+dis[0], height/2-height2+dis[1]))
		return (width2, height2)
	else:
		screen.blit(text,pos)
	width2 = text.get_rect().width
	return width2

def checkU(x,y,s,blocks):
	if y-s < 0 or [x,y-s] in blocks or [x,y-s-s] in blocks or [x-s,y-s] in blocks or [x+s,y-s] in blocks:
		return 0
	return 1

def checkD(x,y,s,blocks,h):
	if y+s > h-s/3 or [x,y+s] in blocks or [x,y+s+s] in blocks or [x+s,y+s] in blocks or [x-s,y+s] in blocks:
		return 0
	return 1

def checkL(x,y,s,blocks):
	if x-s < 0 or [x-s,y] in blocks or [x-s-s,y] in blocks or [x-s,y-s] in blocks or [x-s,y+s] in blocks:
		return 0
	return 1

def checkR(x,y,s,blocks,w):
	if x+s > w-s/3 or [x+s,y] in blocks or [x+s+s,y] in blocks or [x+s,y-s] in blocks or [x+s,y+s] in blocks:
		return 0
	return 1

def getPossible(x,y,s,w,h,blocks):
	ls = []
	if checkU(x,y-s,s,blocks) and checkU(x,y,s,blocks):
		ls.append("u")
	if checkD(x,y+s,s,blocks,h) and checkD(x,y,s,blocks,h):
		ls.append("d")
	if checkL(x-s,y,s,blocks) and checkL(x,y,s,blocks):
		ls.append("l")
	if checkR(x+s,y,s,blocks,w) and checkR(x,y,s,blocks,w):
		ls.append("r")
	if ls:
		return random.choice(ls)
	return 0

while not done:
	#screen.fill(BLUE)
	while not doneGen:
		screen.fill(BLACK)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				doneGen = True
				done = True

		for lead in cleared:
			pygame.draw.rect(screen, WHITE, [lead[0], lead[1], s, s])
		for lead in leading[:-1]:
			pygame.draw.rect(screen, WHITE, [lead[0], lead[1], s, s])
		pygame.draw.rect(screen, YELLOW, [leading[-1][0], leading[-1][1], s, s])

		d = getPossible(x,y,s,width,height,(cleared+leading))
		if d:
			for i in range(2):
				if d == "u":
					y -= s
				elif d == "d":
					y += s
				elif d == "l":
					x -= s
				elif d == "r":
					x += s
				leading.append([x,y])
		else:
			for lead in leading[::-1]:
				if not getPossible(lead[0],lead[1],s,width,height,(leading+cleared)):
					leading.remove(lead)
					cleared.append(lead)
				else:
					x = lead[0]
					y = lead[1]
					break

		if not leading:
			screen.fill(BLACK)
			for lead in cleared:
				pygame.draw.rect(screen, WHITE, [lead[0], lead[1], s, s])
			pygame.draw.rect(screen, GREEN, [max(cleared)[0], max(cleared)[1], s, s])
			pygame.draw.rect(screen, RED, [xs, ys, s, s])
			doneGen = True
		pygame.display.update()


	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			done = True
	#pygame.display.update()

""" need to change leading, cleared to blocks """
