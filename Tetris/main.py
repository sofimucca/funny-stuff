import pygame
from pygame.locals import *
import random
from colors import *

SIZE = 25

X = 0
Y = 1

N_HIGHT  = 24
N_WIDTH = 20

N_SIDEBAR = 8
SIDEBAR_WIDTH = N_SIDEBAR * SIZE

DISPLAYWIDTH = N_WIDTH * SIZE
DISPLAYHIGHT = N_HIGHT * SIZE

TOP_BORDER   = 0
LEFT_BORDER  = 0
BOTTOM_BORDER= DISPLAYHIGHT - 0
RIGHT_BORDER = DISPLAYWIDTH - SIDEBAR_WIDTH

GAME_WIDTH = RIGHT_BORDER- LEFT_BORDER
GAME_HIGHT  = BOTTOM_BORDER- TOP_BORDER
N_ROWS  = int(GAME_HIGHT/SIZE)
N_COLUMNS = int(GAME_WIDTH/SIZE)

FPS = 60
FRAME_PER_BLOCK = 48
FAST_FRAME_PER_BLOCK = 10

class Block:
    def __init__(self, screen, size, color,x=0,y=0):
        self.screen = screen
        self.color = color
        self.size = size
        self.x = x
        self.y = y
        self.center = [x+0.5,y+0.5]
        self.rect = (x*size,y*size,size,size)

    def draw(self):
        pygame.draw.rect(self.screen,self.color,self.rect,0)
        pygame.draw.rect(self.screen,GRID_COLOR,self.rect,1)

    def update_center(self):
        self.center = [self.x+0.5,self.y+0.5]
        self.rect = (self.x*self.size,self.y*self.size,self.size,self.size)

    def update_coordinates(self):
        self.x = self.center[X]-0.5
        self.y = self.center[Y]-0.5
        self.rect = (self.x*self.size,self.y*self.size,self.size,self.size)

    def move(self,x,y):
        self.center[X] = x
        self.center[Y] = y
        self.update_coordinates()
    def move_left(self):
        self.x -= 1
        self.update_center()
    def move_rigth(self):
        self.x += 1
        self.update_center()
    def move_down(self):
        self.y += 1
        self.update_center()


class Tetrimino:
    def __init__(self,screen,field=[[]],size=1,shape='L',x=0,y=0):
        self.screen = screen
        self.field = field
        self.shape = shape
        self.x = x
        self.y = y
        self.blocks = []

        if shape == 'I':
            self.blocks.append(Block(screen,size,CYAN,x-1,y-1))
            self.blocks.append(Block(screen,size,CYAN,x-2,y-1))
            self.blocks.append(Block(screen,size,CYAN,x,y-1))
            self.blocks.append(Block(screen,size,CYAN,x+1,y-1))
        if shape == 'O':
            self.blocks.append(Block(screen,size,YELLOW,x-1,y-1))
            self.blocks.append(Block(screen,size,YELLOW,x,y-1))
            self.blocks.append(Block(screen,size,YELLOW,x-1,y))
            self.blocks.append(Block(screen,size,YELLOW,x,y))
        if shape == 'T':
            self.blocks.append(Block(screen,size,PURPLE,x-1,y))
            self.blocks.append(Block(screen,size,PURPLE,x,y))
            self.blocks.append(Block(screen,size,PURPLE,x+1,y))
            self.blocks.append(Block(screen,size,PURPLE,x,y-1))
        if shape == 'S':
            self.blocks.append(Block(screen,size,GREEN,x,y))
            self.blocks.append(Block(screen,size,GREEN,x-1,y))
            self.blocks.append(Block(screen,size,GREEN,x,y-1))
            self.blocks.append(Block(screen,size,GREEN,x+1,y-1))
        if shape == 'Z':
            self.blocks.append(Block(screen,size,RED,x,y))
            self.blocks.append(Block(screen,size,RED,x,y-1))
            self.blocks.append(Block(screen,size,RED,x-1,y-1))
            self.blocks.append(Block(screen,size,RED,x+1,y))
        if shape == 'J':
            self.blocks.append(Block(screen,size,BLUE,x,y))
            self.blocks.append(Block(screen,size,BLUE,x-1,y))
            self.blocks.append(Block(screen,size,BLUE,x-1,y-1))
            self.blocks.append(Block(screen,size,BLUE,x+1,y))
        if shape == 'L':
            self.blocks.append(Block(screen,size,ORANGE,x,y))
            self.blocks.append(Block(screen,size,ORANGE,x-1,y))
            self.blocks.append(Block(screen,size,ORANGE,x+1,y))
            self.blocks.append(Block(screen,size,ORANGE,x+1,y+1))

        if shape == 'I' or shape == 'O':
            self.rotation_center = [x,y]
        else:
            self.rotation_center = self.blocks[0].center

    def sorted_blocks(self):
        y_list = []
        for i, block in enumerate(self.blocks):
            y_list.append((block.y,i))
        y_list.sort()
        sorted_list = []
        for y, i in y_list:
            sorted_list.append(self.blocks[i])
        return sorted_list

    def draw(self):
        for block in self.blocks:
            block.draw()

    def is_at_the_left_border(self):
        for block in self.blocks:
            if block.x == 0:
                return True
        return False

    def is_at_the_right_border(self):
        for block in self.blocks:
            if block.x == (len(self.field[0])-1):
                return True
        return False

    def is_at_the_top_border(self):
        for block in self.blocks:
            if block.y == 0:
                return True
        return False

    def is_at_the_bottom_border(self):
        for block in self.blocks:
            if block.y == (len(self.field)-1):
                return True
        return False

    def is_at_the_border(self):
        return self.is_at_the_bottom_border() or self.is_at_the_top_border() or self.is_at_the_right_border() or self.is_at_the_left_border()

    def is_off_the_field(self):
        for block in self.blocks:
            if block.x>(len(self.field[0])-1) or block.x<0:
                return True
        return False

    def update_rotation_center(self,delta_x=0,delta_y=0):
        self.rotation_center[X] += delta_x
        self.rotation_center[Y] += delta_y
        
    def cellgrid_is_occupied(self,x,y):
        row = int(y)
        column = int(x)
        if self.field[row][column]:
            return True
        return False
        

    def move_down(self):
        self.y += 1
        self.update_rotation_center(delta_y=1)
        for block in self.blocks:
            block.move_down()

    def move_left(self):
        if not self.is_at_the_left_border():
            for block in self.blocks:
                if self.cellgrid_is_occupied(block.x-1,block.y):
                    return False
            self.x -= 1
            self.update_rotation_center(delta_x=-1)
            for block in self.blocks:
                block.move_left()

    def move_rigth(self):
        if not self.is_at_the_right_border():
            for block in self.blocks:
                if self.cellgrid_is_occupied(block.x+1,block.y):
                    return False
            self.x += 1
            self.update_rotation_center(delta_x=1)
            for block in self.blocks:
                block.move_rigth()

    def arrived(self):
        if self.is_at_the_bottom_border():
            return True
        for block in self.blocks:
            if self.cellgrid_is_occupied(x=block.x,y=block.y+1):
                return True
        return False

    def is_top_out(self):
        for block in self.blocks:
            if block.y < 0:
                return True
        return False

    def check_rotation(self,block):
        if block.x>(len(self.field[0])-1) or block.x<0 or block.y >(len(self.field)-1) :
            return False
        row = int(block.y)
        column = int(block.x)
        if self.field[row][column]:
            return False
        return True

    def rotate_block(self,block):
        block_center_to_rotation_center = [X,Y]
        # coordinates respect the center
        block_center_to_rotation_center[X]= block.center[X] - self.rotation_center[X]
        block_center_to_rotation_center[Y]= block.center[Y] - self.rotation_center[Y]
        #rotation formulas in absolute coordinates
        x = -block_center_to_rotation_center[Y] + self.rotation_center[X]
        y =  block_center_to_rotation_center[X] + self.rotation_center[Y]

        rotated_block = Block(block.screen,block.size,block.color,block.x,block.y)
        rotated_block.move(x,y)
        return rotated_block

    def rotate(self):
        rotated_blocks = []
        for block in self.blocks:
            rotated_block = self.rotate_block(block)
            if not self.check_rotation(rotated_block):
                return False
            else:
                rotated_blocks.append(rotated_block)
        self.blocks = rotated_blocks

class Sidebar:

    def __init__(self,parent_screen,width,color,rigth = True):
        self.parent_screen = parent_screen
        self.screen_width = parent_screen.get_width()
        self.color = color
        self.width = width
        if rigth:
            self.left = self.screen_width-width
        else:
            self.left = 0
        self.top = 0
        self.height = parent_screen.get_height()
        self.screen = parent_screen.subsurface((self.left,self.top,self.width,self.height))
        self.screen.fill(color)

    def clean(self):
        self.surf.fill(self.color)

    def show_next_tetrimino(self,tetrimino):
        shape = tetrimino.shape
        if shape == 'O' or shape == 'I':
            x = 4
        else:
            x = 3.5
        if shape == 'I':
            y = 13
        else:
            y = 12
        tetrimino_image = Tetrimino(self.screen,size=SIZE,shape=shape,x=x,y=y)
        tetrimino_image.draw()

    def show_game_name(self):
        font = pygame.font.SysFont('arial',2*SIZE,bold=True)
        game_name = font.render('TETRIS',True,FONT_COLOR)
        self.screen.blit(game_name,(5,20))

    def show_info(self,score=0,level=0):
        font = pygame.font.SysFont('arial',SIZE,bold=True)
        score = font.render(f'SCORE {score}',True,FONT_COLOR)
        self.screen.blit(score,(10,450))
        level = font.render(f'LEVEL {level}',True,FONT_COLOR)
        self.screen.blit(level,(10,500))

class Game:
    def __init__(self):
        pygame.init()
        
        pygame.mixer.init()
        pygame.mixer.music.load('resources/Tetris_theme.ogg')
        
        self.fpsClock = pygame.time.Clock()

        self.time_counter = FRAME_PER_BLOCK

        self.displaysurf = pygame.display.set_mode((DISPLAYWIDTH,DISPLAYHIGHT))
        pygame.display.set_caption('Tetris')
        self.gamesurf = self.displaysurf.subsurface((LEFT_BORDER,TOP_BORDER),(GAME_WIDTH, GAME_HIGHT))
        self.displaysurf.fill(BG_COLOR)
        self.gamesurf.fill(GAME_COLOR)
        for x in range (N_COLUMNS):
            for y in range (N_ROWS):
                pygame.draw.rect(self.gamesurf,GRID_COLOR,((x*SIZE,y*SIZE),(SIZE, SIZE)),1)

        self.sidebar = Sidebar(self.displaysurf,SIDEBAR_WIDTH,BG_COLOR)
        self.score = 0
        self.level = 0
        self.rows_removed = 0


        self.next_tetrimino = False
        self.tetrimino = False

        self.field = []
        for i in range(N_ROWS):
            row = []
            for j in range(N_COLUMNS):
                row.append(0)
            self.field.append(row)


        self.command_left = False
        self.command_rigth = False
        self.command_rotate = False
        self.command_fast_move_down = False

        pygame.display.flip()
        
    def update_level(self):
        if self.rows_removed >= 10:
            self.level += 1
            self.rows_removed -=10

    def update_score(self,n):
    #Original Nintendo scoring system
        if n == 1:
            self.score += 40 * (self.level+1)
        if n == 2:
            self.score += 100 * (self.level+1)
        if n == 3:
            self.score += 300 * (self.level+1)
        if n == 4:
            self.score += 1200 * (self.level+1)



    def render_background(self):
        self.displaysurf.fill(BG_COLOR)
        self.gamesurf.fill(GAME_COLOR)
        for x in range (N_COLUMNS):
            for y in range (N_ROWS):
                pygame.draw.rect(self.gamesurf,GRID_COLOR,((x*SIZE,y*SIZE),(SIZE, SIZE)),1)

    def random_tetrimino(self):
        tetrimino = False
        while not tetrimino:
            shapes = ['I', 'O', 'T', 'S', 'Z', 'J', 'L']
            shape = random.choice(shapes)
            x=random.randint(0,N_COLUMNS-1)
            y=0
            tetrimino = Tetrimino(self.gamesurf,self.field,SIZE,shape,x,y)
            if tetrimino.is_off_the_field():
                tetrimino = False
        return tetrimino

    def row_is_complete(self,row):
        for block in self.field[row]:
            if not block:
                return False
        return True

    def remove_row(self,i):
        for j in range(N_COLUMNS):
            self.field[i][j] = 0

    def update_rows(self,removed_row):
        for i in range(removed_row,1,-1):
            for j in range(N_COLUMNS):
                if not self.field[i][j] and self.field[i-1][j]:
                    self.field[i-1][j].move_down()
                    self.field[i][j] = self.field[i-1][j]
                    self.field[i-1][j] = 0

    def update_blocks_in_game(self):
        n = 0 #counter row removed with one tetrimino
        for block in self.tetrimino.sorted_blocks():
            row = int(block.y)
            column = int(block.x)
            self.field[row][column] = block
            if self.row_is_complete(row):
                n += 1
                self.rows_removed += 1
                self.remove_row(row)
                self.update_rows(row)
        self.update_level()
        self.update_score(n)

    def draw_blocks_in_game(self):
        for i in range(N_ROWS):
            for j in range(N_COLUMNS):
                if self.field[i][j]:
                    self.field[i][j].draw()

    def show_game_over(self):
        font = pygame.font.SysFont('arial',2*SIZE,bold=True)
        text = font.render('GAME',True,BLACK)
        self.gamesurf.blit(text,(50,100))
        text = font.render('OVER',True,BLACK)
        self.gamesurf.blit(text,(50,200))

    def initializing(self):
        pygame.mixer.music.play()
        self.score = 0
        self.level = 0
        self.rows_removed = 0
        self.next_tetrimino = False
        self.tetrimino = False
        self.field = []
        for i in range(N_ROWS):
            row = []
            for j in range(N_COLUMNS):
                row.append(0)
            self.field.append(row)

        self.render_background()

        self.command_left = False
        self.command_rigth = False
        self.command_rotate = False
        self.command_fast_move_down = False

    def calculus_cycle(self):
        self.time_counter -= 1
        cycle = (self.time_counter == 0)
        if cycle:
            if self.command_fast_move_down:
                self.time_counter = FAST_FRAME_PER_BLOCK
            else:
                self.time_counter = FRAME_PER_BLOCK - 5*self.level
        return cycle

    def play(self):

        move_down_cycle = self.calculus_cycle()

        if not self.next_tetrimino:
            self.tetrimino = self.random_tetrimino()
            self.next_tetrimino = self.random_tetrimino()

        if move_down_cycle:
            if self.tetrimino.arrived():
                if self.tetrimino.is_top_out():
                    raise Exception("Game Over")
                self.update_blocks_in_game()
                self.tetrimino = self.next_tetrimino
                self.next_tetrimino = self.random_tetrimino()
            else:
                self.tetrimino.move_down()

        if self.command_rotate:
            self.tetrimino.rotate()
            self.command_rotate = False
        elif self.command_left:
            self.tetrimino.move_left()
            self.command_left = False
        elif self.command_rigth:
            self.tetrimino.move_rigth()
            self.command_rigth = False

        self.render_background()
        self.tetrimino.draw()
        self.draw_blocks_in_game()

        self.sidebar.show_next_tetrimino(self.next_tetrimino)
        self.sidebar.show_game_name()
        self.sidebar.show_info(self.score,self.level)

    def run(self):
        
        running = True
        pause = True

        while running:

            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
                if event.type == KEYUP:
                    if event.key == K_DOWN:
                        self.command_fast_move_down = False
                if event.type == KEYDOWN:
                    if event.key == K_RETURN:
                        if pause:
                            pause = False
                            self.initializing()
                    if event.key == K_ESCAPE:
                        running = False
                    if event.key == K_SPACE:
                        self.command_rotate = True
                    if event.key == K_DOWN:
                        self.command_fast_move_down = True
                    if event.key == K_RIGHT:
                        self.command_rigth = True
                    if event.key == K_LEFT:
                        self.command_left = True

            if not pause:
                try:
                    self.play()
                except Exception as e:
                    self.show_game_over()
                    pygame.mixer.music.stop()
                    pause = True
                pygame.display.flip()

            self.fpsClock.tick(FPS)

if __name__ == '__main__':
    game = Game()
    game.run()








