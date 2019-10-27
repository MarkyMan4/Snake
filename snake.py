import pygame
import sys
from random import random

T = 75
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
# this will be a list of tuples where each element is a position in the grid
# this is the rest of the snake
player = [] # first element is head of snake
pellet_pos = (0,0)

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
	global player
	global pellet_pos
	global directions

	player_random_x = int(random() * len(grid))
	player_random_y = int(random() * len(grid[0]))
	player.append((player_random_x,player_random_y))

	grid[player_random_x][player_random_y] = BLUE

	new_pellet()

def new_pellet():
	global pellet_pos

	pellet_random_x = int(random() * len(grid))
	pellet_random_y = int(random() * len(grid[0]))
	pellet_pos = (pellet_random_x,pellet_random_y)
	grid[pellet_random_x][pellet_random_y] = WHITE

def is_out_of_bounds(new_tile):
	if new_tile[0] < 0 or new_tile[0] >= len(grid) or new_tile[1] < 0 or new_tile[1] >= len(grid[0]):
		return True

	return False

def update_player(direction):
	global player
	global directions

	new_tile = (0,0)
	head = player[0]

	# update position of head
	if direction == UP:
		new_tile = (head[0], head[1] - 1)
	elif direction == DOWN:
		new_tile = (head[0], head[1] + 1)
	elif direction == LEFT:
		new_tile = (head[0] - 1, head[1])
	elif direction == RIGHT:
		new_tile = (head[0] + 1, head[1])

	if is_out_of_bounds(new_tile):
		# TODO: add a game over screen
		# global GAME_OVER
		# GAME_OVER = True
		return
	
	end_of_tail = player[len(player) - 1]

	# update position of the rest of the body
	for i in range(len(player) - 1, 0, -1):
		player[i] = player[i - 1]
		body_part_pos = player[i]
		grid[body_part_pos[0]][body_part_pos[1]] = BLUE

	grid[end_of_tail[0]][end_of_tail[1]] = BACKGROUND

	if grid[new_tile[0]][new_tile[1]] == WHITE:
		player.append(end_of_tail)
		new_pellet()

	player[0] = new_tile
	grid[new_tile[0]][new_tile[1]] = BLUE


def game_loop():
	global directions

	init_player_and_pellet()

	direction = UP

	while not GAME_OVER:
		for event in pygame.event.get():
			if event.type == MOVEEVENT:
				update_player(direction)
				update_grid()

			if event.type == pygame.QUIT:
				sys.exit()

		keys = pygame.key.get_pressed()  #checking pressed keys

		# update direction of the head
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