

import pygame
from pygame.locals import *
import time
import random

UP = 'up'
DOWN = 'down'
LEFT= 'left'
RIGHT = 'right'

SIZE = 40
FONT_SIZE = int(0.7*SIZE)
APPLE_SIZE = SIZE*0.5

N_WIDTHSIZEES = 21
N_HIGHSIZEES = 17

DISPLAYWIDTH = SIZE * N_WIDTHSIZEES
DISPLAYHIGH = SIZE * N_HIGHSIZEES

N = 1
N_NAVBAR = 2
NAVBARHIGH = N_NAVBAR*SIZE
NAVBAR = (0,0,DISPLAYWIDTH,NAVBARHIGH)
TOP_BOUND = N*SIZE + NAVBARHIGH
LEFT_BOUND = N*SIZE
BOTTOM_BOUND = DISPLAYHIGH - N*SIZE
RIGHT_BOUND = DISPLAYWIDTH - N*SIZE

DISPLAY_RECT = (LEFT_BOUND, TOP_BOUND, DISPLAYWIDTH-2*SIZE, DISPLAYHIGH-2*SIZE-NAVBARHIGH)

SNAKE_RADIUS = 20
EYE_RADIUS = 10
PUPIL_RADIUS = EYE_RADIUS/2


# set up the colors
BG_COLOR     = (  0, 150,   0)
NB_COLOR     = (  0, 110,   0)
BLACK        = (  0,   0,   0)
WHITE        = (255, 255, 255)
RED          = (255,   0,   0)
GREEN        = (  0, 255,   0)
DARKGREEN    = (  0, 225,   0)
BLUE         = (  0,   0, 255)
BROWN        = (139,  69,  19)


class Apple:
    def __init__(self, parent_screen):
        self.parent_screen = parent_screen
        self.x = LEFT_BOUND + 2*SIZE
        self.y = TOP_BOUND + 2*SIZE

    def draw(self):
        x_center = self.x + SIZE/2
        y_center = self.y + SIZE/2
        pygame.draw.circle(self.parent_screen,RED,(x_center,y_center),APPLE_SIZE)
        pygame.draw.rect(self.parent_screen,BROWN,(x_center-2.5,y_center-APPLE_SIZE-8,3,8))
        pygame.draw.ellipse(self.parent_screen,BG_COLOR,(x_center+2.5,y_center-APPLE_SIZE-8,16,8))
        pygame.display.update(DISPLAY_RECT)
        

    def move(self):
        self.x = random.randint(N+1,N_WIDTHSIZEES-1-N)*SIZE 
        self.y = random.randint(N+1+N_NAVBAR,N_HIGHSIZEES-1-N)*SIZE 
                  
class Eyes:
    def __init__(self,snake):
        self.parent_screen = snake.parent_screen
        self.snake = snake
        
    def draw(self):
    
        if self.snake.direction == LEFT:
            left_eye = (self.snake.x[0]+SIZE/2,self.snake.y[0]+SIZE-4)
            left_pupil=(self.snake.x[0]+SIZE/2-PUPIL_RADIUS,self.snake.y[0]+SIZE-4)
            right_eye = (self.snake.x[0]+SIZE/2,self.snake.y[0]+4)
            right_pupil=(self.snake.x[0]+SIZE/2-PUPIL_RADIUS,self.snake.y[0]+4)
        if self.snake.direction == RIGHT:
            left_eye = (self.snake.x[0]+SIZE/2,self.snake.y[0]+4)
            left_pupil=(self.snake.x[0]+SIZE/2+PUPIL_RADIUS,self.snake.y[0]+4)
            right_eye = (self.snake.x[0]+SIZE/2,self.snake.y[0]+SIZE-4)
            right_pupil=(self.snake.x[0]+SIZE/2+PUPIL_RADIUS,self.snake.y[0]+SIZE-4)
        if self.snake.direction == UP:
            left_eye = (self.snake.x[0]+4,self.snake.y[0]+SIZE/2)
            left_pupil=(self.snake.x[0]+4,self.snake.y[0]+SIZE/2-PUPIL_RADIUS)
            right_eye = (self.snake.x[0]+SIZE-4,self.snake.y[0]+SIZE/2)
            right_pupil=(self.snake.x[0]+SIZE-4,self.snake.y[0]+SIZE/2-PUPIL_RADIUS)
        if self.snake.direction == DOWN:
            left_eye = (self.snake.x[0]+4,self.snake.y[0]+SIZE/2)
            left_pupil=(self.snake.x[0]+4,self.snake.y[0]+SIZE/2+PUPIL_RADIUS)
            right_eye = (self.snake.x[0]+SIZE-4,self.snake.y[0]+SIZE/2)
            right_pupil=(self.snake.x[0]+SIZE-4,self.snake.y[0]+SIZE/2+PUPIL_RADIUS)
             
        pygame.draw.circle(self.parent_screen,WHITE,left_eye,EYE_RADIUS)
        pygame.draw.circle(self.parent_screen,BLACK,left_pupil,PUPIL_RADIUS)
        
        pygame.draw.circle(self.parent_screen,WHITE,right_eye,EYE_RADIUS)
        pygame.draw.circle(self.parent_screen,BLACK,right_pupil,PUPIL_RADIUS)
        
    
class Snake:
    def __init__(self, parent_screen):
        self.parent_screen = parent_screen
        
        self.direction = DOWN
        self.length = 2
        self.x = [LEFT_BOUND+SIZE, LEFT_BOUND+SIZE]
        self.y = [TOP_BOUND+2*SIZE, TOP_BOUND+SIZE]
        
        self.eyes = Eyes(self)

    def move_left(self):
        self.direction = LEFT

    def move_right(self):
        self.direction = RIGHT

    def move_up(self):
        self.direction = UP

    def move_down(self):
        self.direction = DOWN

    def walk(self):
        # update body
        for i in range(self.length-1,0,-1):
            self.x[i] = self.x[i-1]
            self.y[i] = self.y[i-1]

        # update head
        if self.direction == LEFT:
            self.x[0] -= SIZE
        if self.direction == RIGHT:
            self.x[0] += SIZE
        if self.direction == UP:
            self.y[0] -= SIZE
        if self.direction == DOWN:
            self.y[0] += SIZE

        self.draw()

    def draw(self):
        for i in range(self.length):
            if i == 0:
                self.draw_head()
            elif i == (self.length - 1):
                self.draw_tail(i)
            else:
                self.draw_body(i)
        
        pygame.display.update(DISPLAY_RECT)
    
    def draw_body(self,i):
        blue = (i*5,i*5,255)
        pygame.draw.rect(self.parent_screen,blue,((self.x[i], self.y[i]),(SIZE, SIZE)))
    
    def draw_head(self):
        if self.direction == LEFT:
            pygame.draw.rect(self.parent_screen,BLUE,((self.x[0], self.y[0]),(SIZE, SIZE)),border_top_left_radius = SNAKE_RADIUS, border_bottom_left_radius = SNAKE_RADIUS)
            
        if self.direction == RIGHT:
            pygame.draw.rect(self.parent_screen,BLUE,((self.x[0], self.y[0]),(SIZE, SIZE)),border_top_right_radius = SNAKE_RADIUS, border_bottom_right_radius = SNAKE_RADIUS)
            
        if self.direction == UP:
            pygame.draw.rect(self.parent_screen,BLUE,((self.x[0], self.y[0]),(SIZE, SIZE)),border_top_left_radius = SNAKE_RADIUS, border_top_right_radius = SNAKE_RADIUS)
            
        if self.direction == DOWN:
            pygame.draw.rect(self.parent_screen,BLUE,((self.x[0], self.y[0]),(SIZE, SIZE)),border_bottom_left_radius = SNAKE_RADIUS, border_bottom_right_radius = SNAKE_RADIUS)
            
        self.eyes.draw()
                 
    def draw_tail(self,i): 
        blue = (i*5,i*5,255)
        if (self.x[i-1]+SIZE, self.y[i-1]) == (self.x[i], self.y[i]): #self.direction == LEFT
            pygame.draw.rect(self.parent_screen,blue,((self.x[i], self.y[i]),(SIZE, SIZE)),border_top_right_radius = SNAKE_RADIUS, border_bottom_right_radius = SNAKE_RADIUS)
        if (self.x[i-1], self.y[i-1]) == (self.x[i]+SIZE, self.y[i]):#self.direction == RIGHT
            pygame.draw.rect(self.parent_screen,blue,((self.x[i], self.y[i]),(SIZE, SIZE)),border_top_left_radius = SNAKE_RADIUS, border_bottom_left_radius = SNAKE_RADIUS)
        if (self.x[i-1], self.y[i-1]+SIZE) == (self.x[i], self.y[i]):#self.direction == UP
            pygame.draw.rect(self.parent_screen,blue,((self.x[i], self.y[i]),(SIZE, SIZE)),border_bottom_left_radius = SNAKE_RADIUS, border_bottom_right_radius = SNAKE_RADIUS)
        if (self.x[i-1], self.y[i-1]) == (self.x[i], self.y[i]+SIZE):#self.direction == DOWN
            pygame.draw.rect(self.parent_screen,blue,((self.x[i], self.y[i]),(SIZE, SIZE)),border_top_left_radius = SNAKE_RADIUS, border_top_right_radius = SNAKE_RADIUS)

    def increase_length(self):
        self.length += 1
        self.x.append(-1)
        self.y.append(-1)

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Hungry Snake")

        pygame.mixer.init()
        self.play_background_music()

        self.surface = pygame.display.set_mode((DISPLAYWIDTH, DISPLAYHIGH))
        self.surface.fill(BG_COLOR)
        self.snake = Snake(self.surface)
        self.snake.draw()
        self.apple = Apple(self.surface)
        self.apple.draw()
        
        self.sleep_time = 0.25

    def play_background_music(self):
        pygame.mixer.music.load('resources/bg_music_1.ogg')
        pygame.mixer.music.play(-1, 0)

    def play_sound(self, sound_name):
        if sound_name == "crash":
            sound = pygame.mixer.Sound("resources/crash.ogg")
        elif sound_name == 'ding':
            sound = pygame.mixer.Sound("resources/ding.ogg")

        pygame.mixer.Sound.play(sound)

    def reset(self):
        self.snake = Snake(self.surface)
        self.apple = Apple(self.surface)
        self.sleep_time = 0.25

    def is_collision(self, x1, y1, x2, y2):
        if x1 >= x2 and x1 < x2 + SIZE:
            if y1 >= y2 and y1 < y2 + SIZE:
                return True
        return False
        
    def is_beyond_window_boundaries(self, x, y, top_bound, left_bound, bottom_bound, rigth_bound):
        if x < left_bound or x + SIZE > rigth_bound or y < top_bound or y + SIZE > bottom_bound:
            return True
        return False

    def render_background(self):
        self.surface.fill(BG_COLOR)
        pygame.draw.rect(self.surface,NB_COLOR,NAVBAR)
        darkgreen = True
        for y in range(TOP_BOUND,BOTTOM_BOUND,SIZE):
            for x in range(LEFT_BOUND,RIGHT_BOUND,SIZE):
                darkgreen = not darkgreen
                if darkgreen:
                    pygame.draw.rect(self.surface,DARKGREEN,((x,y),(SIZE, SIZE)))
                else:
                    pygame.draw.rect(self.surface,GREEN,((x,y),(SIZE, SIZE)))

    def increase_sleep_time(self):
        if self.snake.length <= 4:
            self.sleep_time -= 0.025
        elif self.snake.length > 4 and self.snake.length <=8:
            self.sleep_time -= 0.0125
        else:
            self.sleep_time -= 0.0075
            
    def apple_is_eaten(self):
        self.play_sound("ding")
        self.snake.increase_length()
        self.increase_sleep_time()
        new_apple = False
        while not new_apple:
            self.apple.move()
            new_apple = True
            for i in range(self.snake.length):
                if self.is_collision(self.snake.x[i], self.snake.y[i], self.apple.x, self.apple.y):
                    new_apple = False
                       
    def play(self):
        self.render_background()
        self.snake.walk()
        self.apple.draw()
        self.display_score()
        
        if self.is_collision(self.snake.x[0], self.snake.y[0], self.apple.x, self.apple.y):
            self.apple_is_eaten()

        # snake colliding with itself
        for i in range(3, self.snake.length):
            if self.is_collision(self.snake.x[0], self.snake.y[0], self.snake.x[i], self.snake.y[i]):
                self.play_sound('crash')
                raise "Collision Occurred"
        
        if self.is_beyond_window_boundaries(self.snake.x[0],self.snake.y[0], TOP_BOUND, LEFT_BOUND,BOTTOM_BOUND, RIGHT_BOUND):
            raise "Snake beyond window boundaries"
        
        pygame.display.flip()

    def display_score(self):
        font = pygame.font.SysFont('arial',FONT_SIZE,bold=True)
        score = font.render(f"Score: {self.snake.length}",True,WHITE)
        self.surface.blit(score,(DISPLAYWIDTH*0.8,SIZE*0.5))
        
    def show_game_over(self):
        self.render_background()
        pygame.draw.rect(self.surface,BLUE,((DISPLAYWIDTH*0.05,DISPLAYHIGH*0.25),(DISPLAYWIDTH*0.9,DISPLAYHIGH*0.5)),0,10)
        font = pygame.font.SysFont('arial', FONT_SIZE,bold=True)
        line1 = font.render(f"Game is over! Your score is {self.snake.length}", True, WHITE)
        self.surface.blit(line1, (DISPLAYWIDTH*0.08, DISPLAYHIGH*0.4))
        line2 = font.render("To play again press Enter. To exit press Escape!", True, WHITE)
        self.surface.blit(line2, (DISPLAYWIDTH*0.08, DISPLAYHIGH*0.5))
        pygame.mixer.music.pause()
        pygame.display.update(DISPLAY_RECT)

    def run(self):
        running = True
        pause = False

        while running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False

                    if event.key == K_RETURN:
                        pygame.mixer.music.unpause()
                        pause = False

                    if not pause:
                        if event.key == K_LEFT:
                            self.snake.move_left()

                        if event.key == K_RIGHT:
                            self.snake.move_right()

                        if event.key == K_UP:
                            self.snake.move_up()

                        if event.key == K_DOWN:
                            self.snake.move_down()

                elif event.type == QUIT:
                    running = False
            try:

                if not pause:
                    self.play()

            except Exception as e:
                self.show_game_over()
                pause = True
                self.reset()

            time.sleep(self.sleep_time)

if __name__ == '__main__':
    game = Game()
    game.run()
