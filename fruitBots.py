import pygame
from bot import Bot
from slidersFile import Slider
import random
import numpy as np
import itertools
import pathFinding
import GUI
from GUI import SlideBar, Button

# widow size
WINDOW_SIZE = [1240, 640]

# grid size

GRID_SIZE_SMALL = 5
GRID_SIZE_MEDIUM = 8
GRID_SIZE_LARGE = 12

grid_size = GRID_SIZE_MEDIUM

grid_total_width = grid_total_height = 420
cell_margin = 2

cell_width = cell_height = (grid_total_width- (cell_margin*grid_size))//grid_size

icon_size = 30

# create grid
grid = np.array([[0 for x in range(grid_size)] for y in range(grid_size)])

# variavel de controlo do ciclo principal
end = False

# bot
player1 = Bot(-1, grid_size, icon_size, pygame.image.load('img/walle.png'))

player2 = Bot(-2, grid_size, icon_size, pygame.image.load('img/eve.png'))
steps = 0

pygame.init()
screen = pygame.display.set_mode(WINDOW_SIZE)

# nova imagem a mostrar
new_frame = None

clock = pygame.time.Clock()
pygame.display.set_caption("Fruit Bots")

WHITE = (255, 255, 255)
DARK_GREY = (30, 34, 38)
GREY = (52, 56, 60)
LIGHT_GREY = (171, 178, 186)

TURQUOISE = (1, 174, 180)
LIGHT_TURQUOISE = (167, 221, 223)
DARK_TURQUOISE = (14, 92, 104)

ORANGE = (209, 112, 31)
LIGHT_ORANGE = (249, 209, 147)
DARK_ORANGE = (151, 51, 0)

RED = (223, 79, 68)
LIGHT_RED = (247, 168, 151)
DARK_RED = (171, 25, 36)

screen.fill(GREY)

winner_img  = pygame.image.load('img/cup.png')
winner_img = pygame.transform.scale(winner_img, (icon_size, icon_size))

logo = pygame.image.load("img/logo_watermelon.png")
# logo = pygame.transform.scale(logo, (banner_base_size, banner_base_size))
banana_img  = pygame.image.load('img/banana3.png')
banana_img = pygame.transform.scale(banana_img, (icon_size, icon_size))

apple_img = pygame.image.load('img/apple.png')
apple_img = pygame.transform.scale(apple_img, (icon_size, icon_size))

watermelon_img = pygame.image.load('img/watermelon.png')
watermelon_img = pygame.transform.scale(watermelon_img, (icon_size, icon_size))

banner_base_size = 65
grid_offset_x = 10
grid_offset_y = 75

bot_menu_margin = 50
bot_menu_x = grid_offset_x + grid_total_width + bot_menu_margin
bot_menu_h = (grid_total_height//2)-banner_base_size-grid_offset_x- (grid_offset_x/2)
bot_menu_width = 300


font_title_size = 20
font_title = pygame.font.Font("font/Roboto-Regular.ttf", font_title_size)

font_menu_size = 14
font_menu = pygame.font.Font("font/Roboto-Regular.ttf", font_menu_size)

# for random actions
last_action_time = pygame.time.get_ticks()

BANANA = 1
APPLE = 2
WATERMELON = 3
WALL = -3

total_bananas = num_bananas = 2
total_apples = num_apples = 2
total_watermelons = num_watermelons = 2

total_fruits = num_fruits = num_bananas + num_apples + num_watermelons

pairs = list(itertools.product(np.arange(grid_size), repeat=2))
del pairs[0]
del pairs[len(pairs)-1]

positions = list()

is_reset = False
game_start = False
is_pause = False

###########################################################################

def process_pygame_events():
    global game_start
    global end
    global start_time
    global time_left
    global last_action_time
    global is_reset
    global is_pause

    mouse = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            end = True
        elif event.type == pygame.MOUSEBUTTONDOWN:

            if mouse in bt_start and is_reset:
                bt_start.click()
            elif mouse in bt_reset and not is_reset and not game_start:
                    bt_reset.click()
            elif mouse in bt_shuffle and is_reset and not game_start:
                    bt_shuffle.click()
            elif not game_start:
                if mouse in bt_react_bot1 and player1.get_architecture() != "React":
                    bt_react_bot1.click()
                elif mouse in bt_bdi_bot1 and player1.get_architecture() != "BDI":
                    bt_bdi_bot1.click()
                elif mouse in bt_react_bot2 and player2.get_architecture() != "React":
                    bt_react_bot2.click()
                elif mouse in bt_bdi_bot2 and player2.get_architecture() != "BDI":
                    bt_bdi_bot2.click()

                if is_reset:
                    if mouse in sb_apple:
                        sb_apple.focus()
                    elif mouse in sb_banana:
                        sb_banana.focus()
                    elif mouse in sb_watermelon:
                        sb_watermelon.focus()
                    elif mouse in bt_board_small and grid_size != GRID_SIZE_SMALL:
                        bt_board_small.click()
                    elif mouse in bt_board_medium and grid_size != GRID_SIZE_MEDIUM:
                        bt_board_medium.click()
                    elif mouse in bt_board_large and grid_size != GRID_SIZE_LARGE:
                        bt_board_large.click()
                    

        elif event.type == pygame.MOUSEBUTTONUP:
                sb_banana.unfocus()
                sb_apple.unfocus()
                sb_watermelon.unfocus()

                bt_start.release()
                bt_reset.release()
                bt_shuffle.release()
                bt_board_small.release()
                bt_board_medium.release()
                bt_board_large.release()

                bt_react_bot1.release()
                bt_react_bot2.release()
                bt_bdi_bot1.release()
                bt_bdi_bot2.release()
        else:

            if mouse in bt_shuffle and is_reset and not game_start:
                bt_shuffle.color = LIGHT_ORANGE
            else:
                bt_shuffle.color = ORANGE
        
            if mouse in bt_start and is_reset:
                bt_start.color = LIGHT_RED
            else:
                if game_start and not is_pause:
                    bt_start.color = DARK_RED
                elif not game_start or is_pause:
                    bt_start.color = RED

            if mouse in bt_reset and not is_reset and not game_start:
                bt_reset.color = LIGHT_RED
            else:
                bt_reset.color = RED
            
            if mouse in bt_board_small and is_reset and not game_start and grid_size != GRID_SIZE_SMALL:
                bt_board_small.color = LIGHT_TURQUOISE
            elif grid_size == GRID_SIZE_SMALL:
                bt_board_small.color = DARK_TURQUOISE
            else:
                bt_board_small.color = TURQUOISE

            if mouse in bt_board_medium and is_reset and not game_start  and grid_size != GRID_SIZE_MEDIUM:
                bt_board_medium.color = LIGHT_TURQUOISE
            elif grid_size == GRID_SIZE_MEDIUM:
                bt_board_medium.color = DARK_TURQUOISE
            else:
                bt_board_medium.color = TURQUOISE

            if mouse in bt_board_large and is_reset and not game_start  and grid_size != GRID_SIZE_LARGE:
                bt_board_large.color = LIGHT_TURQUOISE
            elif grid_size == GRID_SIZE_LARGE:
                bt_board_large.color = DARK_TURQUOISE
            else:
                bt_board_large.color = TURQUOISE

            if mouse in bt_react_bot1 and not game_start and player1.get_architecture() != "React":
                bt_react_bot1.color = LIGHT_TURQUOISE
            elif player1.get_architecture() == "React":
                bt_react_bot1.color = DARK_TURQUOISE
            else:
                bt_react_bot1.color = TURQUOISE

            if mouse in bt_bdi_bot1 and not game_start and player1.get_architecture() != "BDI":
                bt_bdi_bot1.color = LIGHT_TURQUOISE
            elif player1.get_architecture() == "BDI":
                bt_bdi_bot1.color = DARK_TURQUOISE
            else:
                bt_bdi_bot1.color = TURQUOISE

            if mouse in bt_react_bot2 and not game_start and player2.get_architecture() != "React":
                bt_react_bot2.color = LIGHT_TURQUOISE
            elif player2.get_architecture() == "React":
                bt_react_bot2.color = DARK_TURQUOISE
            else:
                bt_react_bot2.color = TURQUOISE    

            if mouse in bt_bdi_bot2 and not game_start and player2.get_architecture() != "BDI":
                bt_bdi_bot2.color = LIGHT_TURQUOISE
            elif player2.get_architecture() == "BDI":
                bt_bdi_bot2.color = DARK_TURQUOISE
            else:
                bt_bdi_bot2.color = TURQUOISE

        pressed = pygame.key.get_pressed()

        if pressed[pygame.K_SPACE]:
            print("PRESS SPACE")
            if not game_start:
                game_start = True

def draw_banner():
    global new_frame
    global steps

    new_frame.fill(DARK_GREY, (0, 0, banner_base_size, banner_base_size))
    new_frame.fill(GREY, (banner_base_size, 0, WINDOW_SIZE[0] - banner_base_size, banner_base_size))

    new_frame.blit(logo, (0, 0, 50, 50))

    title = font_title.render("FruitBots", 1, LIGHT_GREY)
    new_frame.blit(title, (font_title_size + banner_base_size, banner_base_size // 2 - (font_title_size // 2)))

    text = font_title.render("Steps: " + str(steps), 1, LIGHT_GREY)
    new_frame.blit(text, (
        WINDOW_SIZE[0] - text.get_width() - font_title_size, banner_base_size // 2 - (font_title_size // 2)))

def remove_old_fruits(fruit_type, old_total_fruits):

    global grid
    global total_fruits
    global pairs

    n_fruits_remove = old_total_fruits - total_fruits

    old_positions = pairs[:old_total_fruits]


    match_fruits = np.asarray(np.where(grid == fruit_type)).T
    match_fruits = [tuple(l) for l in match_fruits]

    
    random.shuffle(match_fruits)
    fruit_delete = match_fruits[:n_fruits_remove]

    for f in fruit_delete:
        grid[f[0]][f[1]] = 0
        pairs.remove(f)
        pairs.append(f)

def add_new_fruits(fruit_type, old_total_fruits):

    global pairs
    global grid
    global total_fruits
    global positions

    positions = pairs[old_total_fruits:total_fruits]

    for i in range(len(positions)):
        pos = positions[i]
        grid[pos[0]][pos[1]] = fruit_type

def place_fruits(randomize):

    global grid
    global total_fruits
    global total_bananas
    global total_apples
    global total_watermelons
    global pairs
    global positions

    # place fruits

    # shuffle possible positions
    if(randomize): random.shuffle(pairs)
    positions = pairs[:total_fruits]

    bananas_placed = 0
    apples_placed = 0
    watermelons_placed = 0
    for i in range(total_fruits):
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

def draw_grid():
    global new_frame
    global grid
    global grid_size
    global cell_width
    global cell_height

    #print("grid", grid)

    grid_copy = grid.copy()

    for row in range(0, len(grid_copy)):
        for column in range(0, len(grid_copy)):
            
            full_width = cell_margin + cell_width
            full_height = cell_margin + cell_height

            pygame.draw.rect(new_frame, LIGHT_GREY,
                             [full_width * column + grid_offset_x + cell_margin, full_height * row + grid_offset_y + cell_margin,
                              cell_width, cell_height], 1)

            fruit_to_draw = None
            # draw fruits
            if grid_copy[row][column] == BANANA:
                fruit_to_draw = banana_img
            elif grid_copy[row][column] == APPLE:
                fruit_to_draw = apple_img
            elif grid_copy[row][column] == WATERMELON:
                fruit_to_draw = watermelon_img

            if fruit_to_draw:
                new_frame.blit(fruit_to_draw, (
                    (full_width * column + cell_margin + grid_offset_x + (full_width - icon_size) / 2),
                    (full_height * row + cell_margin + grid_offset_y + (full_height - icon_size) / 2)))


def draw_botmenu(bot, number):

    global new_frame


    y = grid_offset_y + cell_margin
    y = y + (bot_menu_h+banner_base_size+grid_offset_x*2 if number == 2 else 0)

    bot_img = bot.get_img()

    pygame.draw.rect(new_frame, LIGHT_GREY,(bot_menu_x, y,
                              bot_menu_width, banner_base_size), 1)

    pygame.draw.rect(new_frame, LIGHT_GREY,(bot_menu_x, banner_base_size+ y + grid_offset_x,
                              bot_menu_width, bot_menu_h), 1)

    new_frame.blit(bot_img, (
        bot_menu_x+grid_offset_x, y+((banner_base_size) // 2 - (icon_size // 2))))

    text = font_title.render("Bot "+str(number), 1, LIGHT_GREY)
    
    new_frame.blit(text, (
        bot_menu_x+(grid_offset_x*2) + icon_size, y+((banner_base_size) // 2 - (font_title_size // 2))))

    text_number_wins = font_menu.render(str(bot.number_wins), 1, DARK_GREY)

    w_text_win = font_menu.size(str(bot.number_wins))[0]
    win_x = bot_menu_x+bot_menu_width-(grid_offset_x*2)-icon_size-w_text_win

    win_y_img = y+((banner_base_size) // 2 - (icon_size // 2))
    win_y_text = y+((banner_base_size) // 2 - (font_menu_size // 2))

    new_frame.blit(winner_img, (win_x, win_y_img))
    new_frame.blit(text_number_wins, (win_x+icon_size+grid_offset_x, win_y_text))


def draw_buttons():
    global new_frame

    text_board_size = font_menu.render("Board Size", 1, DARK_GREY)
    new_frame.blit(text_board_size, (bt_x_ori+bt_board_size[0]*2+ grid_offset_x, bt_y- bt_board_size[1]))


    bt_board_small.render(new_frame)
    bt_board_medium.render(new_frame)
    bt_board_large.render(new_frame)
    bt_shuffle.render(new_frame)
    bt_start.render(new_frame)
    bt_reset.render(new_frame)

    bt_react_bot1.render(new_frame)
    bt_react_bot2.render(new_frame)
    bt_bdi_bot1.render(new_frame)
    bt_bdi_bot2.render(new_frame)

def draw_slidebars():
    global new_frame

    x = grid_offset_x + (sb_margin//2)
    y = sb_y - (icon_size) - sb_size[1]
    text_margin = 5

    new_frame.blit(banana_img, (x, y))
    text_banana = font_menu.render("Bananas", 1, DARK_GREY)
    new_frame.blit(text_banana, (x+icon_size+text_margin, y+(font_menu_size//2)))

    sb_banana.render(new_frame)

    x += sb_size[0] + sb_margin
    new_frame.blit(apple_img, (x, y))
    text_apple = font_menu.render("Apples", 1, DARK_GREY)
    new_frame.blit(text_apple, (x+icon_size+text_margin, y+(font_menu_size//2)))

    sb_apple.render(new_frame)
    
    x += sb_size[0] + sb_margin
    new_frame.blit(watermelon_img, (x, y))
    text_watermelon = font_menu.render("Watermelons", 1, DARK_GREY)
    new_frame.blit(text_watermelon, (x+icon_size+text_margin, y+(font_menu_size//2)))

    sb_watermelon.render(new_frame)

def get_neighbor_cells(row,col):
    global grid_size

    cells = [
                grid[row-1][col] if row-1 >= 0 else WALL, # up
                grid[row][col-1] if col-1 >= 0 else WALL, # left
                grid[row+1][col] if row+1 < grid_size else WALL, # down
                grid[row][col+1] if col+1 < grid_size else WALL # right
            ]
    return cells


def get_perception(bot):
    global grid
    global num_bananas
    global num_apples
    global num_watermelons

    arch = bot.get_architecture()

    # tem acesso as 4 celulas em redor
    if arch == "React":
        return get_neighbor_cells(bot.row, bot.col)

    elif arch == "BDI":
        return {"grid":grid, 
                "row":bot.row, 
                "col":bot.col, 
                "fruits_count": [(BANANA,bot.banana_count), (APPLE, bot.apple_count), (WATERMELON, bot.watermelon_count)], 
                "fruits_left": [(BANANA,num_bananas), (APPLE,num_apples), (WATERMELON,num_watermelons)]}

def change_environment(old_pos, action_cell_pos, bot):
    global grid
    global num_fruits
    global num_apples
    global num_bananas
    global num_watermelons

    old_row = old_pos[0]
    old_col = old_pos[1]
    grid[old_row][old_col] = 0

    # grabbed fruit. if 0 means we moved
    if action_cell_pos[0] < 4:

        fruit_pos = action_cell_pos[1]
        fruit_type = grid[fruit_pos[0]][fruit_pos[1]]
        grid[fruit_pos[0]][fruit_pos[1]] = 0
        num_fruits -= 1
        if fruit_type == APPLE: num_apples -= 1
        elif fruit_type == BANANA: num_bananas -= 1
        elif fruit_type == WATERMELON: num_watermelons -= 1

    grid[bot.row][bot.col] = bot.symbol

def game_loop():
    global new_frame
    global game_start
    global last_action_time
    global num_fruits
    global num_bananas
    global num_apples
    global num_watermelons
    global positions
    global steps
    global cell_width
    global cell_height
    global grid
    global is_reset
    global is_pause

    new_frame = pygame.Surface([WINDOW_SIZE[0],WINDOW_SIZE[1]])
    new_frame.fill(WHITE)

    draw_banner()

    draw_grid()
    draw_botmenu(player1, 1)
    draw_botmenu(player2, 2)

    if game_start and not is_pause:
        # new action - random - every second
        time_elapsed_since_last_action = pygame.time.get_ticks() - last_action_time
        if time_elapsed_since_last_action >= 500:
            steps += 1

            old_pos_1 = (player1.row, player1.col)
            old_pos_2 = (player2.row, player2.col)

            action_cell_pos_1 = player1.execute(get_perception(player1))
            change_environment(old_pos_1, action_cell_pos_1, player1)
            action_cell_pos_2 = player2.execute(get_perception(player2))
            change_environment(old_pos_2, action_cell_pos_2, player2)
            last_action_time = pygame.time.get_ticks()

        if num_fruits == 0:
            print("here")
            print(num_fruits)
            game_start = False
            is_pause = False
            is_reset = False
            #new_game()

    player1.draw(new_frame, cell_margin, cell_width, cell_height, grid_offset_x, grid_offset_y)

    player2.draw(new_frame, cell_margin, cell_width, cell_height, grid_offset_x, grid_offset_y)

    draw_slidebars()
    draw_buttons()

def new_game(place = True):
    global steps
    global last_action_time
    global grid
    global grid_size
    global num_fruits
    global total_fruits
    global total_watermelons
    global total_apples
    global total_bananas

    steps = 0
    last_action_time = pygame.time.get_ticks()

    grid = np.array([[0 for x in range(grid_size)] for y in range(grid_size)])
    player1.row = player1.col = 0
    player2.row = player2.col = grid_size-1
    grid[player1.row][player1.col] = -1
    grid[player2.row][player2.col] = -2

    if place: place_fruits(False)

    num_bananas = total_bananas
    num_apples = total_apples
    num_watermelons = total_watermelons

    player1.banana_count = player1.apple_count = player1.watermelon_count = player1.fruit_count = 0
    player2.banana_count = player2.apple_count = player2.watermelon_count = player2.fruit_count = 0

    total_fruits = num_fruits = num_bananas + num_apples + num_watermelons


def init_game():

    global steps
    global last_action_time
    global grid
    global grid_size
    global total_fruits
    global pairs
    global positions

    steps = 0
    last_action_time = pygame.time.get_ticks()

    grid = np.array([[0 for x in range(grid_size)] for y in range(grid_size)])
    player1.row = player1.col = 0
    player2.row = player2.col = grid_size-1
    grid[player1.row][player1.col] = -1
    grid[player2.row][player2.col] = -2

    # shuffle possible positions
    random.shuffle(pairs)
    positions = pairs[:total_fruits]


###########################################################################

#
# Buttons
#

def func_shuffle():
    global grid
    global grid_size

    grid = np.array([[0 for x in range(grid_size)] for y in range(grid_size)])
    player1.row = player1.col = 0
    player2.row = player2.col = grid_size-1
    grid[player1.row][player1.col] = player1.symbol
    grid[player2.row][player2.col] = player2.symbol

    place_fruits(True)

def set_board_size(new_size):
    global grid
    global grid_size
    global cell_width
    global cell_height
    global pairs

    grid_size = new_size
    cell_width = cell_height = (grid_total_width- (cell_margin*grid_size))//grid_size

    # create grid
    grid = np.array([[0 for x in range(grid_size)] for y in range(grid_size)])

    player1.row = player1.col = 0
    player2.row = player2.col = grid_size-1
    grid[player1.row][player1.col] = player1.symbol
    grid[player2.row][player2.col] = player2.symbol
    player1.setBoard_size(grid_size)
    player2.setBoard_size(grid_size)

    pairs = list(itertools.product(np.arange(grid_size), repeat=2))
    del pairs[0]
    del pairs[len(pairs)-1]

    random.shuffle(pairs)

    if is_reset : place_fruits(False)

def func_board_small():

    set_board_size(GRID_SIZE_SMALL)

def func_board_medium():

    set_board_size(GRID_SIZE_MEDIUM)

def func_board_large():
    set_board_size(GRID_SIZE_LARGE)

def func_start_simulation():
    global game_start
    global is_pause

    if not game_start: game_start = True
    else: is_pause = not is_pause

def func_reset_simulation():
    global is_reset
    is_reset = True
    new_game()

bt_margin = 15
bt_shuffle_size = (130,40)

bt_x_ori=bt_x = grid_offset_x + grid_total_width + bot_menu_margin + (bt_shuffle_size[0]//2)
bt_y = 560

bt_shuffle = Button(func_shuffle, (bt_x, bt_y), bt_shuffle_size, 'Shuffle Board', color = ORANGE)

bt_x += (bt_shuffle_size[0]//2) + bt_margin*3
bt_board_size = (40,40)
bt_board_small = Button(func_board_small, (bt_x, bt_y), bt_board_size, 'S', color = TURQUOISE)

bt_x += bt_board_size[0] + bt_margin
bt_board_medium = Button(func_board_medium, (bt_x, bt_y), bt_board_size, 'M', color = TURQUOISE)

bt_x += bt_board_size[0] + bt_margin
bt_board_large = Button(func_board_large, (bt_x, bt_y), bt_board_size, 'L', color = TURQUOISE)


bt_start_x = grid_offset_x + grid_total_width + bot_menu_margin + bot_menu_width + (bt_shuffle_size[0]//2) + bot_menu_margin
bt_start_y = grid_offset_y + cell_margin + (bt_shuffle_size[1]//2)
bt_start = Button(func_start_simulation, (bt_start_x, bt_start_y), bt_shuffle_size, 'Run', color = RED)


bt_reset_x = bt_start_x + bt_shuffle_size[0] +bt_margin
bt_reset_y = bt_start_y
bt_reset = Button(func_reset_simulation, (bt_reset_x, bt_reset_y), bt_shuffle_size, 'Reset', color = RED)


# bot menu

def func_set_arch(bot, arch):
    bot.set_architecture(arch)

def func_set_react_bot1():

    func_set_arch(player1, "React")

def func_set_react_bot2():
    func_set_arch(player2, "React")

def func_set_bdi_bot1():
    func_set_arch(player1, "BDI")

def func_set_bdi_bot2():
    func_set_arch(player2, "BDI")

bt_arch_h = bot_menu_h//4
bt_arch_size = (bot_menu_width, bt_arch_h)

bot_menu_y_bot1 = grid_offset_y + cell_margin + banner_base_size + grid_offset_x

bot_menu_y_bot2 = bot_menu_y_bot1 + bot_menu_h+banner_base_size+grid_offset_x*2

bt_arch_x = bot_menu_x+(bt_arch_size[0]//2)

bt_react_bot1 = Button(func_set_react_bot1, (bt_arch_x, bot_menu_y_bot1), bt_arch_size, 'Reactive', color = TURQUOISE)
bot_menu_y_bot1 += bt_arch_h
bt_bdi_bot1 = Button(func_set_bdi_bot1, (bt_arch_x, bot_menu_y_bot1), bt_arch_size, 'BDI', color = TURQUOISE)

bt_react_bot2 = Button(func_set_react_bot2, (bt_arch_x, bot_menu_y_bot2), bt_arch_size, 'Reactive', color = TURQUOISE)
bot_menu_y_bot2 += bt_arch_h
bt_bdi_bot2 = Button(func_set_bdi_bot2, (bt_arch_x, bot_menu_y_bot2), bt_arch_size, 'BDI', color = TURQUOISE)

#
# Sliders settings
#

sb_margin = 25
sb_size = (grid_total_width//3 -(sb_margin),30)

sb_x = sb_x_init = grid_offset_x + sb_size[0]//2 + (sb_margin//2)
sb_y = 580

# bananas
sb_banana = SlideBar(print, (sb_x, sb_y), sb_size, 0, 5, 1, interval=4)

sb_banana.set(total_bananas)
def func_sb_banana(value):
    global total_fruits
    global total_bananas
    old_total_fruits = total_fruits
    total_fruits = total_fruits - total_bananas + value
    if (total_fruits == 0): 
        total_fruits = old_total_fruits
        sb_banana.set(total_bananas)
        return
    total_bananas = value

    if total_fruits > old_total_fruits: add_new_fruits(BANANA, old_total_fruits)
    else: remove_old_fruits(BANANA, old_total_fruits)

sb_banana.func = func_sb_banana

# apples
sb_x += sb_size[0] + sb_margin
sb_apple = SlideBar(print, (sb_x, sb_y), sb_size, 0, 5, 1, interval=4)

sb_apple.set(total_apples)
def func_sb_apple(value):
    global total_fruits
    global total_apples

    old_total_fruits = total_fruits
    total_fruits = total_fruits - total_apples + value
    if (total_fruits == 0): 
        total_fruits = old_total_fruits
        sb_apple.set(total_apples)
        return
    total_apples = value

    if total_fruits > old_total_fruits: add_new_fruits(APPLE, old_total_fruits)
    else: remove_old_fruits(APPLE, old_total_fruits)

sb_apple.func = func_sb_apple

# watermelons
sb_x += sb_size[0] + sb_margin
sb_watermelon = SlideBar(print, (sb_x, sb_y), sb_size, 0, 5, 1, interval=4)

sb_watermelon.set(total_watermelons)
def func_sb_watermelon(value):
    global total_fruits
    global total_watermelons

    old_total_fruits = total_fruits
    total_fruits = total_fruits - total_watermelons + value
    if (total_fruits == 0): 
        total_fruits = old_total_fruits
        sb_watermelon.set(total_watermelons)
        return
    total_watermelons = value

    if total_fruits > old_total_fruits: add_new_fruits(WATERMELON, old_total_fruits)
    else: remove_old_fruits(WATERMELON, old_total_fruits)

sb_watermelon.func = func_sb_watermelon

init_game()
while not end:
    process_pygame_events()

    game_loop()

    # actualizar pygame com a nova imagem
    screen.blit(new_frame, (0, 0))
    pygame.display.update()

pygame.quit()
quit()
