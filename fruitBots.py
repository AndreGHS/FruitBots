import pygame
from bot import Bot
from slidersFile import Slider
from random import randint
import numpy as np

# grid size
WINDOW_SIZE = [720, 516]

width = 40
height = 40
margin = 2

# create grid
grid_size = 10
grid = [[0 for x in range(grid_size)] for y in range(grid_size)]

# variável de controlo do ciclo principal
end = False

# bot
bot = Bot()
bot.setBoard_size(grid_size - 1)

MAX_TIME = 10
time_left = MAX_TIME
start_time = 0
game_start = False

pygame.init()
screen = pygame.display.set_mode(WINDOW_SIZE)
# nova imagem a mostrar
new_frame = None

clock = pygame.time.Clock()
pygame.display.set_caption("Fruit Bots")

white = (255, 255, 255)
dark_grey = (30,34,38)
grey = (52, 56, 60)
light_grey = (171, 178, 186)

logo = pygame.image.load("img/logo_watermelon.png")
#logo = pygame.transform.scale(logo, (banner_base_size, banner_base_size))
banana_img = pygame.image.load('img/banana2.png')
banana_img = pygame.transform.scale(banana_img, (30, 30))  
img_banana_size = banana_img.get_size()[0]


banner_base_size = 65
grid_offset_x = 10
grid_offset_y = 75

font_title_size = 20
font_title = pygame.font.Font("font/Roboto-Regular.ttf", font_title_size)

# for random actions
last_action_time = pygame.time.get_ticks()

# Sliders settings
num_bananas = Slider("Bananas", 2, 5, 1, 25)
num_apples = Slider("Apples", 2, 5, 1, 175)
num_watermelons = Slider("Watermelons", 2, 5, 1, 325)
slides = list()
slides.append(num_bananas)
slides.append(num_apples)
slides.append(num_watermelons)

num_fruits = TOTAL_FRUITS = num_bananas.val

def process_pygame_events():
    
    global game_start
    global end
    global start_time
    global time_left
    global last_action_time
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            end = True
            
        pressed = pygame.key.get_pressed()
        
        if pressed[pygame.K_SPACE]:
            print("PRESS SPACE")
            
            game_start = not game_start
            if not game_start: new_game()
            else: 
                start_time = pygame.time.get_ticks()
                time_left = MAX_TIME
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
    global time_left
    global game_start
    
    new_frame.fill(dark_grey, (0, 0, banner_base_size, banner_base_size))
    new_frame.fill(grey, (banner_base_size, 0, WINDOW_SIZE[0]-banner_base_size, banner_base_size))
    
    new_frame.blit(logo, (0, 0, 50, 50))
    
    title = font_title.render("FruitBots", 1, light_grey)
    new_frame.blit(title, (font_title_size + banner_base_size, banner_base_size//2-(font_title_size//2)))
    
    if game_start: time_left = (MAX_TIME - (pygame.time.get_ticks() - start_time)//1000)
    
    text = font_title.render("Timer: " + str(time_left) + " s", 1, light_grey)
    new_frame.blit(text, (WINDOW_SIZE[0] - text.get_width() - font_title_size, banner_base_size//2-(font_title_size//2)))


def draw_grid():
    global new_frame
    global grid
    for row in range(0, grid_size):
        for column in range(0, grid_size):
            #TODO - REVER DESENHO DOS RECTS
            full_width = margin + width
            full_height = margin + height
            pygame.draw.rect(new_frame, white, [full_width * column + grid_offset_x+margin, full_height * row + grid_offset_y+margin,
                                             width, height], 0)
            pygame.draw.rect(new_frame, light_grey, [full_width * column + grid_offset_x+margin, full_height * row + grid_offset_y+margin,
                                             width, height], 1)
    
            # draw fruits
            if grid[row][column] == 1:
                new_frame.blit(banana_img, ((full_width * column + margin + grid_offset_x + (full_width-img_banana_size)/2), (full_height * row + margin + grid_offset_y+ (full_height-img_banana_size)/2)))

     
def game_loop():
    global new_frame
    global time_left
    global game_start
    global last_action_time
    global num_fruits
    
    new_frame = pygame.Surface(WINDOW_SIZE)
    new_frame.fill(white)
    
    draw_banner()
    
    draw_grid() 
    
    if game_start:
        # new action - random - every second
        time_elapsed_since_last_action = pygame.time.get_ticks() - last_action_time
        if time_elapsed_since_last_action >= 1000:
            grid[bot.row][bot.column] = 0
            bot.do_random_action()
            last_action_time = pygame.time.get_ticks()
        
        if grid[bot.row][bot.column] == 1:
            bot.catch_banana()         
            grid[bot.row][bot.column] = -1
            num_fruits -= 1
            
        if time_left <= 0 or num_fruits == 0:
            print("here")
            print(num_fruits)
            print(time_left)
            game_start = False
            new_game()
        
    bot.draw(new_frame, margin, width, height, grid_offset_x, grid_offset_y)
    
    """   
    for s in slides:
        if s.hit:
            s.move()
    for s in slides:
        print("drawing")
        s.draw()
    """
    
def new_game():
    
    global time_left
    global game_start
    global start_time
    global last_action_time
    global grid
    global num_fruits

    start_time = pygame.time.get_ticks()
    time_left = MAX_TIME
    last_action_time = pygame.time.get_ticks()
    
    grid = [[0 for x in range(grid_size)] for y in range(grid_size)]
    bot.row = bot.column = 0
    grid[bot.row][bot.column] = -1
    
    num_fruits = TOTAL_FRUITS
    bot.banana_count = bot.fruit_count = 0
    # place fruits
    for i in range(num_fruits):
        pos = np.random.choice(a=grid_size, size=2, replace=False)
        while pos[0] == 0 and pos[1] == 0:
            pos = np.random.choice(a=grid_size, size=2, replace=False)
        
        grid[pos[0]][pos[1]] = 1
        
    print(grid)    


new_game() 
while not (end):
    process_pygame_events()
    
    game_loop()
    
    # actualizar pygame com a nova imagem
    screen.blit(new_frame, (0, 0))    
    pygame.display.update()
    

pygame.quit()
quit()