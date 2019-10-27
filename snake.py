import pygame
import sys
from random import random

T = 250
MOVEEVENT = pygame.USEREVENT
pygame.time.set_timer(MOVEEVENT, T)

WIDTH = 800
HEIGHT = 800
BLUE = (50,50,255)
WHITE = (255,255,255)
BACKGROUND = (0,0,0)
PLAYER_POS = [400, 300]
TILE_SIZE = [20, 20]
GAME_OVER = False

UP = 0
DOWN = 1
LEFT = 2
RIGHT = 3

grid = [[0 for i in range(40)] for j in range(40)]
player_pos = (0,0) # this is the head of the snake
pellet_pos = (0,0)

# this will be a list of tuples where each element is a position in the grid
# this is the rest of the snake
tail = []
directions = [] # this is parallel to tail, keeps track of what direction each part is moving

def init_grid():
	for i in range(0, len(grid)):
		for j in range(0, len(grid[i])):
			grid[i][j] = BACKGROUND
			pygame.draw.rect(screen, grid[i][j], (i * TILE_SIZE[0], j * TILE_SIZE[1], TILE_SIZE[0], TILE_SIZE[1]))

	pygame.display.update()

def update_grid():
	for i in range(0, len(grid)):
		for j in range(0, len(grid[i])):
			pygame.draw.rect(screen, grid[i][j], (i * TILE_SIZE[0], j * TILE_SIZE[1], TILE_SIZE[0], TILE_SIZE[1]))

	pygame.display.update()

def init_player_and_pellet():
	global player_pos
	global pellet_pos
	global tail

	player_random_x = int(random() * len(grid))
	player_random_y = int(random() * len(grid[0]))
	player_pos = (player_random_x,player_random_y)
	tail.append((player_random_x,player_random_y))

	pellet_random_x = int(random() * len(grid))
	pellet_random_y = int(random() * len(grid[0]))
	pellet_pos = (pellet_random_x,pellet_random_y)

	grid[player_random_x][player_random_y] = BLUE
	grid[pellet_random_x][pellet_random_y] = WHITE

def is_out_of_bounds(new_tile):
	if new_tile[0] < 0 or new_tile[0] >= len(grid) or new_tile[1] < 0 or new_tile[1] >= len(grid[0]):
		return True

	return False

def update_player(direction):
	global player_pos
	global tail
	global directions

	new_tile = (0,0)

	if direction == UP:
		new_tile = (player_pos[0], player_pos[1] - 1)
	elif direction == DOWN:
		new_tile = (player_pos[0], player_pos[1] + 1)
	elif direction == LEFT:
		new_tile = (player_pos[0] - 1, player_pos[1])
	elif direction == RIGHT:
		new_tile = (player_pos[0] + 1, player_pos[1])

	if is_out_of_bounds(new_tile):
		# TODO: add a game over screen
		# global GAME_OVER
		# GAME_OVER = True
		return

	# TODO: make snake grow when pellet is eaten
	if grid[new_tile[0]][new_tile[1]] == WHITE:
		print('got pellet')
		tail.append(player_pos)
		directions.append(direction)

	grid[player_pos[0]][player_pos[1]] = BACKGROUND

	# print(new_tile)
	grid[new_tile[0]][new_tile[1]] = BLUE
	player_pos = new_tile


def game_loop():
	global directions

	init_player_and_pellet()

	direction = UP
	directions.append(UP)

	while not GAME_OVER:
		for event in pygame.event.get():
			if event.type == MOVEEVENT:
				update_player(direction)
				update_grid()

			if event.type == pygame.QUIT:
				sys.exit()

		keys = pygame.key.get_pressed()  #checking pressed keys
		if keys[pygame.K_w]:
			direction = UP
		elif keys[pygame.K_s]:
			direction = DOWN
		elif keys[pygame.K_a]:
			direction = LEFT
		elif keys[pygame.K_d]:
			direction = RIGHT

		if keys[pygame.K_ESCAPE]:
			sys.exit()

if __name__ == '__main__':
	pygame.init()
	screen = pygame.display.set_mode((WIDTH, HEIGHT))
	init_grid()
	game_loop()