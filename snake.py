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
eat_sound_path = os.path.join(base_path, "plastic-crunch-83779.wav")
gameover_img_path = os.path.join(base_path, "gameover.png")

# Load assets
grass_img = pygame.image.load(grass_img_path)
apple_img = pygame.image.load(apple_img_path)
pygame.mixer.music.load('C:\\Users\\sslavov\\Desktop\\SnakeGame\\SoundAndStyle\\best-adventure-ever-122726.mp3')
eat_sound = pygame.mixer.Sound(eat_sound_path)

# Resize images
dis_width = 800
dis_height = 600

# Fit background image to screen dimensions
grass_img = pygame.transform.scale(grass_img, (dis_width, dis_height))

# Resize apple image
apple_img_width = 30  # Set width for the apple image
apple_img_height = 30  # Set height for the apple image
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
transparent_black = (0, 0, 0, 128)

# Set snake parameters
snake_block = 10
snake_speed = 15
boosted_speed = snake_speed * 2

# Clock
clock = pygame.time.Clock()

# Font
font_style = pygame.font.SysFont("bahnschrift", 25)
score_font = pygame.font.SysFont("comicsansms", 35)

# AISnake class
class AISnake:
    def __init__(self, block_size, initial_length=1):
        self.snake_block = block_size
        self.snake_list = []
        self.length_of_snake = initial_length
        self.x = random.randint(0, dis_width // block_size) * block_size
        self.y = random.randint(0, dis_height // block_size) * block_size
        self.x_change = 0
        self.y_change = 0
        self.create_initial_snake()

    def create_initial_snake(self):
        for _ in range(self.length_of_snake):
            self.snake_list.append([self.x, self.y])

    def move(self, foodx, foody):
        # Simple strategy: move towards the food
        if self.x < foodx:
            self.x_change = self.snake_block
            self.y_change = 0
        elif self.x > foodx:
            self.x_change = -self.snake_block
            self.y_change = 0
        elif self.y < foody:
            self.x_change = 0
            self.y_change = self.snake_block
        elif self.y > foody:
            self.x_change = 0
            self.y_change = -self.snake_block

        self.x += self.x_change
        self.y += self.y_change

        # Update snake list
        snake_head = [self.x, self.y]
        self.snake_list.append(snake_head)
        if len(self.snake_list) > self.length_of_snake:
            del self.snake_list[0]

        # Check for self-collision
        for segment in self.snake_list[:-1]:
            if segment == snake_head:
                self.handle_self_collision()

    def handle_self_collision(self):
        # When the snake collides with itself, just end the game (simpler approach)
        self.snake_list = self.snake_list[-self.length_of_snake:]

    def draw(self, display):
        for segment in self.snake_list:
            pygame.draw.rect(display, green, [segment[0], segment[1], self.snake_block, self.snake_block])


# Game functions
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

def draw_stamina_bar(stamina, max_stamina):
    bar_width = 200
    bar_height = 20
    x = dis_width - bar_width - 10
    y = dis_height - bar_height - 10
    fill_width = (stamina / max_stamina) * bar_width

    s = pygame.Surface((bar_width, bar_height), pygame.SRCALPHA)
    s.fill(transparent_black)
    pygame.draw.rect(s, blue, (0, 0, fill_width, bar_height))
    dis.blit(s, (x, y))

def pause():
    paused = True
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    paused = False
                elif event.key == pygame.K_q:
                    pygame.quit()
                    quit()
        dis.fill(blue)
        message("Paused. Press C to Continue or Q to Quit.", red)
        pygame.display.update()
        clock.tick(5)

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

    stamina = 100
    max_stamina = 100
    boost_active = False
    boost_deplete_rate = 0.5
    boost_recover_rate = 0.2

    ai_snake = AISnake(snake_block)

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
                elif event.key == pygame.K_ESCAPE:
                    pause()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LCTRL] and stamina > 0:
            boost_active = True
            stamina -= boost_deplete_rate
        else:
            boost_active = False
            if stamina < max_stamina:
                stamina += boost_recover_rate

        if stamina < 0:
            stamina = 0
        if stamina > max_stamina:
            stamina = max_stamina

        if x1 >= dis_width or x1 < 0 or y1 >= dis_height or y1 < 0:
            game_close = True
        x1 += x1_change
        y1 += y1_change

        # Draw the grass background
        dis.blit(grass_img, [0, 0])

        # Draw the apple
        dis.blit(apple_img, [foodx, foody])

        snake_Head = [x1, y1]
        snake_List.append(snake_Head)
        
        if len(snake_List) > Length_of_snake:
            del snake_List[0]

        for x in snake_List[:-1]:
            if x == snake_Head:
                game_close = True

        our_snake(snake_block, snake_List)
        show_score(score)
        draw_stamina_bar(stamina, max_stamina)

        # Move and draw the AI snake
        ai_snake.move(foodx, foody)
        ai_snake.draw(dis)

        pygame.display.update()

        if x1 < foodx + apple_img_width and x1 + snake_block > foodx:
            if y1 < foody + apple_img_height and y1 + snake_block > foody:
                foodx = round(random.randrange(0, dis_width - apple_img_width) / 10.0) * 10.0
                foody = round(random.randrange(0, dis_height - apple_img_height) / 10.0) * 10.0
                Length_of_snake += 1
                score += 1
                eat_sound.play()  # Play sound effect when the snake eats the food

        # Check if the AI snake eats the food
        if ai_snake.x < foodx + apple_img_width and ai_snake.x + snake_block > foodx:
            if ai_snake.y < foody + apple_img_height and ai_snake.y + snake_block > foody:
                foodx = round(random.randrange(0, dis_width - apple_img_width) / 10.0) * 10.0
                foody = round(random.randrange(0, dis_height - apple_img_height) / 10.0) * 10.0
                ai_snake.length_of_snake += 1

        current_speed = boosted_speed if boost_active else snake_speed
        clock.tick(current_speed)

    pygame.quit()
    quit()

# Start the game
gameLoop()
