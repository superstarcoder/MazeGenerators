import pygame
import random

""" uncomment next para and comment next to next para for fullscreen """

#screen = pygame.display.set_mode((0,0), pygame.RESIZABLE)	
#infoObject = pygame.display.Info()
#width = infoObject.current_w
#height = infoObject.current_h
#size = (width, height) #1920, 1080

width = 800
height = 800
screen = pygame.display.set_mode((800, 800))


"""uncomment next para and comment previous for resizable screen. Adjust width & height to your convenience"""

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

""" adjust to your convenience """
s = 60 #maze cell size in pixels. Do not go below 30 in fullscreen (takes too much time to generate)
fps = 50 #frames per second
x=0; y=0 #starting point of the maze


w=s;h=s;w2=h; h2=w2/5; h2=1; w3=h; h3=w2/8; st=int(h3/2)

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

def getPossible(x, y, blocks, willRemove=[]):
	ls = ["u","d","l","r"]

	if not willRemove == []:
		for r in willRemove:
			if r in ls:
				ls.remove(r)
	if y-w2 < 0 or any(i[1] == y-w2 and i[0] == x for i in blocks):
		if "u" in ls:
			ls.remove("u")
	if y+w2 > height-w2 or any(i[1] == y+w2 and i[0] == x for i in blocks):
		if "d" in ls:
			ls.remove("d")

	if x-w2 < 0 or any(i[0] == x-w2 and i[1] == y for i in blocks):
		if "l" in ls:
			ls.remove("l")
	if x+w2 > width-w2 or any(i[0] == x+w2 and i[1] == y for i in blocks):
		if "r" in ls:
			ls.remove("r")
	return ls

def createMaze(x,y,s,showGen=False):
	w=s; h=s; w2=h; h2=w2/5; h2=1; w3=h; h3=w2/8; st=int(h3/2)
	w4=int(width/3.555); h4=int(height/5.4); x4=(width-w4)/2; y4=(height-h4)/2
	w5=int(width/3.84); h5=int(h4/4); x5=int(width/2.704); y5=int(height/2.097); t=int((width*height)/69120)

	willRemove = []
	blocks = [[x, y, w, h]]
	lines = []
	walls = []
	noWalls = []
	#screen.fill((244, 185, 66))
	doneGen = False
	done = False
	while not doneGen:
		screen.fill(BLACK)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				doneGen = True
				done = True
		if showGen:

			pygame.draw.rect(screen, YELLOW, [x,y,w,h])

			for wall in walls:
				pygame.draw.rect(screen, BLUE, wall)

			for noWall in noWalls:
				pygame.draw.rect(screen, BLACK, noWall)
		else:
			p = len(blocks)/(int(width/w2)*int(height/w2)-1)*100+1
			pygame.draw.rect(screen, WHITE, [x4, y4, w4, h4])
			pygame.draw.rect(screen, RED, [x5, y5, w5, h5])
			pygame.draw.rect(screen, GREEN, [x5, y5, p*(w5/100), h5])
			renderText(str(int(p))+"%", "aharoni", t, BLACK, False, True, (0, int(height/21.6)))

		ls = getPossible(x, y, blocks)

		if not ls == []:
			pygame.display.update()
			direction = random.choice(ls)
			if direction == "u":
				walls.append([x-h3/2,y,h3,w3])
				walls.append([(x-h3/2)+w2,y,h3,w3])
				noWalls.append([x,y-h3/2,w3,h3])
				y -= w2
				blocks.append([x, y, w, h])

			elif direction == "d":
				walls.append([x-h3/2,y,h3,w3])
				walls.append([(x-h3/2)+w2,y,h3,w3])
				noWalls.append([x,(y-h3/2)+w2,w3,h3])
				y += w2
				blocks.append([x, y, w, h])

			elif direction == "r":
				walls.append([x,y-h3/2,w3,h3])
				walls.append([x,(y-h3/2)+w2,w3,h3])
				noWalls.append([(x-h3/2)+w2,y,h3,w3])
				x += w2
				blocks.append([x, y, w, h])

			elif direction == "l":
				walls.append([x,y-h3/2,w3,h3])
				walls.append([x,(y-h3/2)+w2,w3,h3])
				noWalls.append([x-h3/2,y,h3,w3])
				x -= w2
				blocks.append([x, y, w, h])
		else:
			for a in range(1, len(blocks)+1):
				x = blocks[-a][0]
				y = blocks[-a][1]
				ls = getPossible(x, y, blocks)
				if not ls == []:
					break

		if len(blocks) >= int(width/w2)*int(height/w2)-1:
			for noWall in noWalls:
				while noWall in walls:
					walls.remove(noWall)
			pygame.display.update()
			return walls, done
	return walls, done
		

""" uncomment next line and comment next to next line for loading screen. (generates faster)"""
b = 0
""" uncomment next line and comment previous line for seeing the maze generate"""
#b = 1

walls, done = createMaze(x,y,s,b)

pygame.draw.rect(screen, BLUE, [0, 0, width-st, height-st], st)

while not done:
	screen.fill(BLACK)
	for wall in walls:
		pygame.draw.rect(screen, BLUE, wall)
	pygame.draw.rect(screen, BLUE, [0, 0, width-st, height-st], st)

	key = pygame.key.get_pressed()
	if key[pygame.K_SPACE]:
		walls, done = createMaze(x,y,s,b)

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			done = True

	pygame.display.update()
