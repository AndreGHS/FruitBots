import pygame
from bot import Bot
from slidersFile import Slider
from random import randint

# grid size
WINDOW_SIZE = [720, 516]

width = 30
height = 30
margin = 5

WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
bright_green = (0, 200, 0)
bright_red = (200, 0, 0)

player_img = pygame.image.load('img/bot.png')
banana_img = pygame.image.load('img/banana.png')

# create grid
gridSize = 10
grid = [[0 for x in range(gridSize)] for y in range(gridSize)]

# timer variables
passed_time = 0
timer_started = False

font = pygame.font.SysFont("comicsansms", 32)
fontScore = pygame.font.SysFont("arial", 20)
font_color = pygame.Color('springgreen')

# Sliders settings
num_bananas = Slider("Bananas", 2, 5, 1, 25)
num_apples = Slider("Apples", 2, 5, 1, 175)
num_watermelons = Slider("Watermelons", 2, 5, 1, 325)

slides = list()
slides.append(num_bananas)
slides.append(num_apples)
slides.append(num_watermelons)

pygame.init()
screen = pygame.display.set_mode(WINDOW_SIZE)
done = False
clock = pygame.time.Clock()
pygame.display.set_caption("Fruit Bots")


def gameLoop():
    global done
    global timer_started
    global passed_time
    global num_bananas
    gamestart = False
    # bot
    player = Bot()
    player.setBoard_size(gridSize - 1)

    # fruits specification
    fruits = list()
    bananas = list()
    apples = list()

    if not gamestart:
        for i in range (int(num_bananas.val//1)):
            r = randint(0,9)
            c = randint(0,9)
            if r == 0 and c == 0:
                r = randint(0, 9)
                c = randint(0, 9)
            bananas.append([r, c])
            fruits.append([r, c])


    #apple_pos = [2, 2]
    #apples.append(apple_pos)
    #fruits.append(apple_pos)

    # fills the fruits in the board
    for x in range(0, len(bananas)):
        grid[bananas[x][0]][bananas[x][1]] = 1
    for x in range(0, len(apples)):
        grid[apples[x][0]][apples[x][1]] = 2

    # draws bot image
    screen.blit(player_img, (((margin + width) * player.column + margin), ((margin + height) * player.row + margin)))

    while True:
        # grid[player[0]][player[1]] = -1;
        grid[player.row][player.column] = -1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quitGame()
            if not gamestart:
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
                gamestart = True
                timer_started = not timer_started
                if timer_started:
                    start_time = pygame.time.get_ticks()
            if gamestart:
                if pressed[pygame.K_q]:
                    timer_started = False
                    passed_time = 0
                    gameLoop()

                if pressed[pygame.K_DOWN]:
                    grid[player.row][player.column] = 0
                    player.move_down()

                elif pressed[pygame.K_UP]:
                    grid[player.row][player.column] = 0
                    player.move_up()

                elif pressed[pygame.K_RIGHT]:
                    grid[player.row][player.column] = 0
                    player.move_right()

                elif pressed[pygame.K_LEFT]:
                    grid[player.row][player.column] = 0
                    player.move_left()

                for banana in bananas:
                    if player.row == banana[0] and player.column == banana[1]:
                        player.catch_banana()
                        bananas.remove(banana)
                        fruits.remove(banana)

        screen.fill((0, 0, 0))

        # draws timer
        if timer_started:
            passed_time = pygame.time.get_ticks() - start_time
        text = font.render("Timer: " + str(passed_time // 1000), True, font_color)
        screen.blit(text, (WINDOW_SIZE[0] - text.get_width(), 0))

        scoretext = fontScore.render("Score: " + str(player.fruit_count), True, font_color)
        screen.blit(scoretext, (WINDOW_SIZE[0] / 2 + WINDOW_SIZE[0] / 4, WINDOW_SIZE[1]/2))

        # draw grid and images

        for row in range(0, 10):
            for column in range(0, 10):
                color = WHITE
                use_img = False

                pygame.draw.rect(screen, color, [(margin + width) * column + margin, (margin + height) * row + margin,
                                                 width, height])
                if grid[row][column] == -1:
                    img_toDraw = player_img
                    use_img = True

                if grid[row][column] == 1:
                    img_toDraw = banana_img
                    use_img = True
                    pygame.draw.rect(screen, RED, [(margin + width) * column + margin, (margin + height) * row + margin,
                                                   width, height])

                if use_img:
                    screen.blit(img_toDraw, (((margin + width) * column + margin), ((margin + height) * row + margin)))

        # check if there's no more fruits
        if len(fruits) == 0:
            timer_started = False
            passed_time = 0
            endGame()

        # check if time has ended
        if passed_time // 1000 >= 10:
            timer_started = False
            passed_time = 0
            gameOver()

        for s in slides:
            if s.hit:
                s.move()

        for s in slides:
            s.draw()

        clock.tick(60)
        pygame.display.flip()


def endGame():
    text = font.render("Game End", True, RED)
    text_rect = text.get_rect()
    text_x = WINDOW_SIZE[0] / 2 - text_rect.width / 2
    text_y = WINDOW_SIZE[1] / 2 - text_rect.height / 2
    screen.fill((0, 0, 0))
    screen.blit(text, [text_x, text_y])

    while True:
        for event in pygame.event.get():
            # print(event)
            if event.type == pygame.QUIT:
                quitGame()

        # gameDisplay.fill(white)

        button("PlayAgain", WINDOW_SIZE[0] / 2 - WINDOW_SIZE[0] / 4, WINDOW_SIZE[1] / 2 + WINDOW_SIZE[1] / 4, GREEN,
               bright_green, gameLoop)
        button("Quit", WINDOW_SIZE[0] / 2 + WINDOW_SIZE[0] / 4, WINDOW_SIZE[1] / 2 + WINDOW_SIZE[1] / 4, RED,
               bright_red, quitGame)

        pygame.display.update()
        clock.tick(15)


def gameOver():
    text = font.render("Game Over", True, RED)
    text_rect = text.get_rect()
    text_x = WINDOW_SIZE[0] / 2 - text_rect.width / 2
    text_y = WINDOW_SIZE[1] / 2 - text_rect.height / 2
    screen.fill((0, 0, 0))
    screen.blit(text, [text_x, text_y])

    while True:
        for event in pygame.event.get():
            # print(event)
            if event.type == pygame.QUIT:
                quitGame()

        # gameDisplay.fill(white)

        button("Retry", WINDOW_SIZE[0] / 2 - WINDOW_SIZE[0] / 4, WINDOW_SIZE[1] / 2 + WINDOW_SIZE[1] / 4, GREEN,
               bright_green, gameLoop)
        button("Quit", WINDOW_SIZE[0] / 2 + WINDOW_SIZE[0] / 4, WINDOW_SIZE[1] / 2 + WINDOW_SIZE[1] / 4, RED,
               bright_red, quitGame)

        pygame.display.update()
        clock.tick(15)


def quitGame():
    pygame.quit()
    quit()


# UI FUNCTIONS-------------------------

# text used on objects
def text_objects(text, font):
    textSurface = font.render(text, True, (0, 0, 0))
    return textSurface, textSurface.get_rect()


def button(message, x, y, ic, ac, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    smallText = pygame.font.SysFont("comicsansms", 32)
    textSurf, textRect = text_objects(message, smallText)
    w = textRect.width
    h = textRect.height
    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        pygame.draw.rect(screen, ac, (x, y, w, h))
        if click[0] == 1 and action is not None:
            action()
    else:
        pygame.draw.rect(screen, ic, (x, y, w, h))

    textRect.center = ((x + (w / 2)), (y + (h / 2)))
    screen.blit(textSurf, textRect)


gameLoop()
