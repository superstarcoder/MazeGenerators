import pygame
import random
import time

#screen = pygame.display.set_mode((0,0), pygame.RESIZABLE)	
#infoObject = pygame.display.Info()
#width = infoObject.current_w
#height = infoObject.current_h
#size = (width, height) #1920, 1080
#screen = pygame.display.set_mode(size, pygame.FULLSCREEN)

width = 800
height = 800
size = (width, height)
screen = pygame.display.set_mode(size)

clock = pygame.time.Clock()
pygame.init()

done = False; doneGen=False

s=20;xs=0; ys=0; x=xs; y=ys

BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (209, 41, 41)
BLUE = (1, 38, 249)
YELLOW = (255, 242, 0)
GREEN = (5, 186, 29)
GREY = (20, 20, 20)

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

def createMaze(x,y,s,showGen=False):
	cleared=[];leading=[[x,y]]
	w4=int(width/3.555); h4=int(height/5.4); x4=(width-w4)/2; y4=(height-h4)/2
	w5=int(width/3.84); h5=int(h4/4); x5=int(width/2.704); y5=int(height/2.097); t=int((width*height)/69120)

	while True:
		if showGen:
			screen.fill(BLACK)
			for lead in cleared:
				pygame.draw.rect(screen, WHITE, [lead[0], lead[1], s, s])
			for lead in leading:
				pygame.draw.rect(screen, WHITE, [lead[0], lead[1], s, s])
		else:
			screen.fill(BLACK)
			#p = ((len(cleared))/((width*height)/(65.7*s)))*100
			p = ((len(cleared))/(((width*height)/s)/65.775950668))*100
			pygame.draw.rect(screen, WHITE, [x4, y4, w4, h4])
			pygame.draw.rect(screen, RED, [x5, y5, w5, h5])
			if p >= 100:
				pygame.draw.rect(screen, GREEN, [x5, y5, 100*(w5/100), h5])
				renderText("100%", "aharoni", t, BLACK, False, True, (0, int(height/21.6)))
			else:
				pygame.draw.rect(screen, GREEN, [x5, y5, p*(w5/100), h5])
				renderText(str(int(p))+"%", "aharoni", t, BLACK, False, True, (0, int(height/21.6)))

		for lead in leading:
			if not getPossible(lead[0],lead[1],s,width,height,(cleared+leading)):
				leading.remove(lead)
				cleared.append(lead)

		if leading:
			xy = random.choice(leading)
			x = xy[0]
			y = xy[1]
			d = getPossible(x,y,s,width,height,(cleared+leading))
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
			if showGen:
				screen.fill(BLACK)
				for lead in cleared:
					pygame.draw.rect(screen, WHITE, [lead[0], lead[1], s, s])
				pygame.draw.rect(screen, GREEN, [max(cleared)[0], max(cleared)[1], s, s])
				pygame.draw.rect(screen, RED, [xs, ys, s, s])
			else:
				pygame.draw.rect(screen, WHITE, [x4, y4, w4, h4])
				pygame.draw.rect(screen, RED, [x5, y5, w5, h5])
				pygame.draw.rect(screen, GREEN, [x5, y5, 100*(w5/100), h5])
				renderText("100%", "aharoni", t, BLACK, False, True, (0, int(height/21.6)))
			pygame.display.update()
			time.sleep(0.5)
			return cleared, False

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				done = True
				return cleared, True
		pygame.display.update()

b = 1
blocks, done = createMaze(x,y,s,b)
while not done:
	screen.fill(BLACK)
	for lead in blocks:
		pygame.draw.rect(screen, WHITE, [lead[0], lead[1], s, s])
		pygame.draw.rect(screen, GREEN, [max(blocks)[0], max(blocks)[1], s, s])
		pygame.draw.rect(screen, RED, [xs, ys, s, s])

	key = pygame.key.get_pressed()
	if key[pygame.K_SPACE]:
		blocks, done = createMaze(x,y,s,b)

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			done = True

	pygame.display.update()
