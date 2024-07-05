import pygame
import time
import random
import os

# Initialize Pygame
pygame.init()

# Define paths
base_path = "C:\\Users\\sslavov\\Desktop\\SnakeGame\\SoundAndStyle"
grass_img_path = os.path.join(base_path, "grass.jpg")
apple_img_path = os.path.join(base_path, "apple.png")
background_music_path = os.path.join(base_path, "best-adventure-ever-122726.mp3")
eat_sound_path = os.path.join(base_path, "plastic-crunch-83779.wav")

# Load assets
grass_img = pygame.image.load(grass_img_path)
apple_img = pygame.image.load(apple_img_path)
pygame.mixer.music.load(background_music_path)
eat_sound = pygame.mixer.Sound(eat_sound_path)

# Resize images
dis_width = 800
dis_height = 600

# Fit background image to screen dimensions
grass_img = pygame.transform.scale(grass_img, (dis_width, dis_height))

# Resize apple image
apple_img_width = 20  # Set width for the apple image
apple_img_height = 20  # Set height for the apple image
apple_img = pygame.transform.scale(apple_img, (apple_img_width, apple_img_height))

# Start background music
pygame.mixer.music.play(-1)  # Loop the background music indefinitely

# Set display dimensions
dis = pygame.display.set_mode((dis_width, dis_height))
pygame.display.set_caption('Snake Game')

# Set colors
white = (255, 255, 255)
yellow = (255, 255, 102)
black = (0, 0, 0)
red = (213, 50, 80)
green = (0, 255, 0)
blue = (50, 153, 213)

# Set snake parameters
snake_block = 10
snake_speed = 15

# Clock
clock = pygame.time.Clock()

# Font
font_style = pygame.font.SysFont("bahnschrift", 25)
score_font = pygame.font.SysFont("comicsansms", 35)

def our_snake(snake_block, snake_list):
    for i, x in enumerate(snake_list):
        if i == len(snake_list) - 1:
            pygame.draw.rect(dis, yellow, [x[0], x[1], snake_block, snake_block])  # Snake's head
        else:
            pygame.draw.rect(dis, black, [x[0], x[1], snake_block, snake_block])  # Snake's body

def message(msg, color):
    mesg = font_style.render(msg, True, color)
    dis.blit(mesg, [dis_width / 6, dis_height / 3])

def show_score(score):
    score_text = score_font.render("Score: " + str(score), True, white)
    dis.blit(score_text, [dis_width / 2 - score_text.get_width() / 2, 10])

def gameLoop():
    game_over = False
    game_close = False
    score = 0

    x1 = dis_width / 2
    y1 = dis_height / 2

    x1_change = 0
    y1_change = 0

    snake_List = []
    Length_of_snake = 1

    foodx = round(random.randrange(0, dis_width - apple_img_width) / 10.0) * 10.0
    foody = round(random.randrange(0, dis_height - apple_img_height) / 10.0) * 10.0

    while not game_over:

        while game_close == True:
            dis.fill(blue)
            message("You Lost! Press Q-Quit or C-Play Again", red)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        gameLoop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and x1_change == 0:
                    x1_change = -snake_block
                    y1_change = 0
                elif event.key == pygame.K_RIGHT and x1_change == 0:
                    x1_change = snake_block
                    y1_change = 0
                elif event.key == pygame.K_UP and y1_change == 0:
                    y1_change = -snake_block
                    x1_change = 0
                elif event.key == pygame.K_DOWN and y1_change == 0:
                    y1_change = snake_block
                    x1_change = 0

        if x1 >= dis_width or x1 < 0 or y1 >= dis_height or y1 < 0:
            game_close = True
        x1 += x1_change
        y1 += y1_change

        # Draw the grass background
        dis.blit(grass_img, [0, 0])

        # Draw the apple
        dis.blit(apple_img, [foodx, foody])

        snake_Head = []
        snake_Head.append(x1)
        snake_Head.append(y1)
        snake_List.append(snake_Head)
        if len(snake_List) > Length_of_snake:
            del snake_List[0]

        for x in snake_List[:-1]:
            if x == snake_Head:
                game_close = True

        our_snake(snake_block, snake_List)
        show_score(score)
        pygame.display.update()

        if x1 == foodx and y1 == foody:
            foodx = round(random.randrange(0, dis_width - apple_img_width) / 10.0) * 10.0
            foody = round(random.randrange(0, dis_height - apple_img_height) / 10.0) * 10.0
            Length_of_snake += 1
            score += 1
            eat_sound.play()  # Play sound effect when the snake eats the food

        clock.tick(snake_speed)

    pygame.quit()
    quit()

gameLoop()