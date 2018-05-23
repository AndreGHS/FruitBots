import pygame
from bot import Bot
from slidersFile import Slider
import random
import numpy as np
import itertools
import pathFinding

# grid size
WINDOW_SIZE = [720, 640]

width = 40
height = 40
margin = 2

# create grid
grid_size = 10
grid = [[0 for x in range(grid_size)] for y in range(grid_size)]
graph = pathFinding.Graph()
graph.constructGraphFromGrid(grid_size)

# variável de controlo do ciclo principal
end = False

# bot
bot = Bot()
player1 = Bot()
player1.setBoard_size(grid_size - 1)

MAX_TIME = 50
time_count = 0
start_time = 0
game_start = False

pygame.init()
screen = pygame.display.set_mode(WINDOW_SIZE)

# nova imagem a mostrar
new_frame = None

clock = pygame.time.Clock()
pygame.display.set_caption("Fruit Bots")

white = (255, 255, 255)
dark_grey = (30, 34, 38)
grey = (52, 56, 60)
light_grey = (171, 178, 186)

screen.fill(grey)

logo = pygame.image.load("img/logo_watermelon.png")
# logo = pygame.transform.scale(logo, (banner_base_size, banner_base_size))
banana_img = pygame.image.load('img/banana3.png')
banana_img = pygame.transform.scale(banana_img, (30, 30))
img_fruit_size = banana_img.get_size()[0]

apple_img = pygame.image.load('img/apple.png')
apple_img = pygame.transform.scale(apple_img, (30, 30))

watermelon_img = pygame.image.load('img/watermelon.png')
watermelon_img = pygame.transform.scale(watermelon_img, (30, 30))

banner_base_size = 65
grid_offset_x = 10
grid_offset_y = 75

font_title_size = 20
font_title = pygame.font.Font("font/Roboto-Regular.ttf", font_title_size)

# for random actions
last_action_time = pygame.time.get_ticks()

# Sliders settings
banana_slider = Slider("Bananas", 2, 5, 1, 25)
apple_slider = Slider("Apples", 2, 5, 1, 175)
watermelon_slider = Slider("Watermelons", 2, 5, 1, 325)
slides = list()
slides.append(banana_slider)
slides.append(apple_slider)
slides.append(watermelon_slider)

BANANA = 1
APPLE = 2
WATERMELON = 3

num_fruits = total_fruits = banana_slider.val + apple_slider.val + watermelon_slider.val
total_bananas = num_bananas = banana_slider.val
total_apples = num_apples = apple_slider.val
total_watermelons = num_watermelons = watermelon_slider.val

pairs = list(itertools.product(np.arange(grid_size), repeat=2))
del pairs[0]

positions = list()


def process_pygame_events():
    global game_start
    global end
    global start_time
    global time_left
    global last_action_time

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            end = True
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            for s in slides:
                if s.button_rect.collidepoint(pos):
                    s.hit = True
        elif event.type == pygame.MOUSEBUTTONUP:
            for s in slides:
                s.hit = False

        pressed = pygame.key.get_pressed()

        if pressed[pygame.K_SPACE]:
            print("PRESS SPACE")

            game_start = not game_start
            if not game_start:
                new_game()
            else:
                start_time = pygame.time.get_ticks()
                time_count = 0
                last_action_time = pygame.time.get_ticks()





        if game_start:
            if pressed[pygame.K_DOWN]:
                print("PRESS ARROW")
                grid[bot.row][bot.column] = 0
                bot.move_down()

            elif pressed[pygame.K_UP]:
                print("PRESS ARROW")
                grid[bot.row][bot.column] = 0
                bot.move_up()

            elif pressed[pygame.K_RIGHT]:
                print("PRESS ARROW")
                grid[bot.row][bot.column] = 0
                bot.move_right()

            elif pressed[pygame.K_LEFT]:
                print("PRESS ARROW")
                grid[bot.row][bot.column] = 0
                bot.move_left()


def draw_banner():
    global new_frame
    global time_count
    global game_start

    new_frame.fill(dark_grey, (0, 0, banner_base_size, banner_base_size))
    new_frame.fill(grey, (banner_base_size, 0, WINDOW_SIZE[0] - banner_base_size, banner_base_size))

    new_frame.blit(logo, (0, 0, 50, 50))

    title = font_title.render("FruitBots", 1, light_grey)
    new_frame.blit(title, (font_title_size + banner_base_size, banner_base_size // 2 - (font_title_size // 2)))

    if game_start:
        # time_left = (MAX_TIME - (pygame.time.get_ticks() - start_time) // 1000)
        time_count = (pygame.time.get_ticks() - start_time) // 1000

    text = font_title.render("Timer: " + str(time_count) + " s", 1, light_grey)
    new_frame.blit(text, (
        WINDOW_SIZE[0] - text.get_width() - font_title_size, banner_base_size // 2 - (font_title_size // 2)))


def draw_grid():
    global new_frame
    global grid
    for row in range(0, grid_size):
        for column in range(0, grid_size):
            # TODO - REVER DESENHO DOS RECTS
            full_width = margin + width
            full_height = margin + height
            pygame.draw.rect(new_frame, white,
                             [full_width * column + grid_offset_x + margin, full_height * row + grid_offset_y + margin,
                              width, height], 0)
            pygame.draw.rect(new_frame, light_grey,
                             [full_width * column + grid_offset_x + margin, full_height * row + grid_offset_y + margin,
                              width, height], 1)

            fruit_to_draw = None
            # draw fruits
            if grid[row][column] == BANANA:
                fruit_to_draw = banana_img
            elif grid[row][column] == APPLE:
                fruit_to_draw = apple_img
            elif grid[row][column] == WATERMELON:
                fruit_to_draw = watermelon_img

            if fruit_to_draw:
                new_frame.blit(fruit_to_draw, (
                    (full_width * column + margin + grid_offset_x + (full_width - img_fruit_size) / 2),
                    (full_height * row + margin + grid_offset_y + (full_height - img_fruit_size) / 2)))


def game_loop():
    global new_frame
    global time_count
    global game_start
    global last_action_time
    global num_fruits
    global num_bananas
    global num_apples
    global num_watermelons
    global positions

    new_frame = pygame.Surface([720,516])
    new_frame.fill(white)

    draw_banner()

    draw_grid()

    if game_start:
        # new action - random - every second
        time_elapsed_since_last_action = pygame.time.get_ticks() - last_action_time
        if time_elapsed_since_last_action >= 1000:
            grid[player1.row][player1.column] = 0
            #bot.do_random_action()

            if not player1.hasPath() and num_fruits > 0: #TODO Make bot look for most desired fruit not the first of the list
                fruit = positions[0]
                positions.pop(0)
                startNode = str(player1.row)+str(player1.column)
                endNode = str(fruit[0])+str(fruit[1])
                movement = graph.getPathForMovement(graph.bfs_short_path(startNode, endNode))
                player1.setPath(movement)

            player1.nextPathMovement()

            last_action_time = pygame.time.get_ticks()

        if grid[player1.row][player1.column] == BANANA:
            player1.catch_banana()
            grid[player1.row][player1.column] = -1
            num_fruits -= 1
            num_bananas -= 1
        elif grid[player1.row][player1.column] == APPLE:
            player1.catch_apple()
            grid[player1.row][player1.column] = -1
            num_fruits -= 1
            num_apples -= 1
        elif grid[player1.row][player1.column] == WATERMELON:
            player1.catch_watermelon()
            grid[player1.row][player1.column] = -1
            num_fruits -= 1
            num_watermelons -= 1

        if num_fruits == 0:
            print("here")
            print(num_fruits)
            print(time_count)
            game_start = False
            new_game()

    player1.draw(new_frame, margin, width, height, grid_offset_x, grid_offset_y)

    for s in slides:
        if s.hit:
            s.move()
    for s in slides:

        s.draw()


def new_game():
    global time_count
    global game_start
    global start_time
    global last_action_time
    global grid
    global num_fruits
    global positions

    start_time = pygame.time.get_ticks()
    time_count = 0
    last_action_time = pygame.time.get_ticks()

    grid = [[0 for x in range(grid_size)] for y in range(grid_size)]
    player1.row = player1.column = 0
    grid[player1.row][player1.column] = -1

    total_bananas = num_bananas = banana_slider.val
    total_apples = num_apples = apple_slider.val
    total_watermelons = num_watermelons = watermelon_slider.val

    num_fruits = total_fruits = banana_slider.val + apple_slider.val + watermelon_slider.val
    player1.banana_count = player1.fruit_count = 0

    # place fruits

    # shuffle possible positions
    random.shuffle(pairs)
    positions = pairs[:num_fruits]

    bananas_placed = 0
    apples_placed = 0
    watermelons_placed = 0
    for i in range(num_fruits):
        pos = positions[i]
        if bananas_placed < total_bananas:
            to_place = BANANA
            bananas_placed += 1
        elif apples_placed < total_apples:
            to_place = APPLE
            apples_placed += 1
        elif watermelons_placed < total_watermelons:
            to_place = WATERMELON
            watermelons_placed += 1

        grid[pos[0]][pos[1]] = to_place

    print(grid)


new_game()
while not end:
    process_pygame_events()

    game_loop()

    # actualizar pygame com a nova imagem
    screen.blit(new_frame, (0, 0))
    pygame.display.update()

pygame.quit()
quit()
