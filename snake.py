import pygame
import sys
from random import random

MOVEEVENT = pygame.USEREVENT

GAME_OVER_TIME = 1000
GAMEOVEREVENT = pygame.USEREVENT

WIDTH = 800
HEIGHT = 800
BLUE = (50,50,255)
WHITE = (255,255,255)
BACKGROUND = (0,0,0)
TILE_SIZE = [20, 20]

UP = 0
DOWN = 1
LEFT = 2
RIGHT = 3

GAME_OVER = False
score = 0

# initialize global variables, draw the initial empty grid
def init_game():
	global player
	global grid
	global pellet_pos
	global score
	global GAME_OVER
	global T

	# this will be a list of tuples where each element is a position in the grid
	# this is the rest of the snake
	player = []
	grid = [[0 for i in range(40)] for j in range(40)]
	pellet_pos = (0,0)

	score = 0
	GAME_OVER = False

	# the T value controls how fast the snake moves, the grid is updated every T milliseconds
	T = 75
	pygame.time.set_timer(MOVEEVENT, T)

	for i in range(0, len(grid)):
		for j in range(0, len(grid[i])):
			grid[i][j] = BACKGROUND
			pygame.draw.rect(screen, grid[i][j], (i * TILE_SIZE[0], j * TILE_SIZE[1], TILE_SIZE[0], TILE_SIZE[1]))

	pygame.display.update()

# redraws the grid, this is called each time the snake moves
def update_grid():
	for i in range(0, len(grid)):
		for j in range(0, len(grid[i])):
			pygame.draw.rect(screen, grid[i][j], (i * TILE_SIZE[0], j * TILE_SIZE[1], TILE_SIZE[0], TILE_SIZE[1]))

	pygame.display.update()

# pick a random starting point for the player
# spawn the initial pellet
def init_player_and_pellet():
	player_random_x = int(random() * len(grid))
	player_random_y = int(random() * len(grid[0]))
	player.append((player_random_x,player_random_y))

	grid[player_random_x][player_random_y] = BLUE

	new_pellet()

# spawn a pellet at a random location
# won't spawn a pellet directly on the snake
def new_pellet():
	pellet_random_x = int(random() * len(grid))
	pellet_random_y = int(random() * len(grid[0]))

	while grid[pellet_random_x][pellet_random_y] == BLUE:
		pellet_random_x = int(random() * len(grid))
		pellet_random_y = int(random() * len(grid[0]))

	pellet_pos = (pellet_random_x,pellet_random_y)
	grid[pellet_random_x][pellet_random_y] = WHITE

# check if the snake is about to hit the wall or its own body
def is_collision(new_tile):
	if new_tile[0] < 0 or new_tile[0] >= len(grid) or new_tile[1] < 0 or new_tile[1] >= len(grid[0]) \
		or grid[new_tile[0]][new_tile[1]] == BLUE:
		return True

	return False

# Updates the position of the snake and each body part for a single time step.
# This doesn't actually draw any components, it sets the colors and the list of
# positions stored in player. The components get redrawn when update_grid() is called
def update_player(direction):
	global GAME_OVER
	global score

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

	if is_collision(new_tile):
		GAME_OVER = True
		return

	end_of_tail = player[len(player) - 1]

	# update position of the rest of the body
	for i in range(len(player) - 1, 0, -1):
		player[i] = player[i - 1]
		body_part_pos = player[i]
		grid[body_part_pos[0]][body_part_pos[1]] = BLUE

	grid[end_of_tail[0]][end_of_tail[1]] = BACKGROUND

	if grid[new_tile[0]][new_tile[1]] == WHITE:
		score += 1
		player.append(end_of_tail)
		new_pellet()

	player[0] = new_tile
	grid[new_tile[0]][new_tile[1]] = BLUE

# main game loop
# listens for events and key presses
def game_loop():
	init_player_and_pellet()

	# set the initial direction
	# could be a random direction too
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

# game over screen, formats game over text and timer
# Escape key to exit, R to restart
# not my most readable code but it works...
def game_over_screen():
	global score

	screen.fill(BACKGROUND)
	done = False

	font_1 = pygame.font.SysFont('papyrus', 72)
	font_2 = pygame.font.SysFont('papyrus', 48)
	font_3 = pygame.font.SysFont('papyrus', 48)
	text = font_1.render('GAME OVER', True, (255, 0, 0))
	restart_text = font_2.render('Press \'R\' to restart', True, (255, 0, 0))
	time_left = 10
	time_text = font_1.render(str(time_left), True, (255, 0, 0))
	score_text = font_3.render('Score: %d' % score, True, (255, 255, 255))
	clock = pygame.time.Clock()

	pygame.time.set_timer(GAMEOVEREVENT, GAME_OVER_TIME)

	while not done:
		screen.blit(score_text, (WIDTH / 2 - score_text.get_width() / 2, HEIGHT / 2 - score_text.get_height() - text.get_height()))
		screen.blit(text, (WIDTH / 2 - text.get_width() / 2, HEIGHT / 2 - text.get_height()))
		screen.blit(restart_text, (WIDTH / 2 - restart_text.get_width() / 2, (HEIGHT / 2 - restart_text.get_height()) + restart_text.get_height()))
		screen.blit(time_text, (WIDTH / 2 - time_text.get_width() / 2, (HEIGHT / 2 - time_text.get_height()) + text.get_height() + restart_text.get_height()))
		pygame.display.flip()
		
		for event in pygame.event.get():
			if event.type == GAMEOVEREVENT:
				pygame.draw.rect(screen, BACKGROUND, (WIDTH / 2 - time_text.get_width() / 2, 
					(HEIGHT / 2 - time_text.get_height()) + text.get_height() + restart_text.get_height(), 100, 100))
				time_left -= 1
				if time_left == 0:
					# quit the game
					return True

				time_text = font_1.render(str(time_left), True, (255, 0, 0))

		keys = pygame.key.get_pressed()  #checking pressed keys

		# update direction of the head
		if keys[pygame.K_ESCAPE]:
			return True

		if keys[pygame.K_r]:
			return False

if __name__ == '__main__':
	quit = False

	while not quit:
		pygame.init()
		screen = pygame.display.set_mode((WIDTH, HEIGHT))
		init_game()
		game_loop()
		quit = game_over_screen()