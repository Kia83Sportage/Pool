import pygame
from pygame import mixer
import pymunk
import pymunk.pygame_util
import math
import sys

pygame.init()

SCREEN_WIDTH = 1545
SCREEN_HEIGHT = 880

# Screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("8 Ball")

# Pymunk Space
space = pymunk.Space()
static_body = space.static_body
draw_options = pymunk.pygame_util.DrawOptions(screen)

# Clock
clock = pygame.time.Clock()
FPS = 120

# Players
white = (255, 255, 255)
black = (0, 0, 0)
player1_name = "Amir"
player2_name = "Kia"
font = pygame.font.Font(None, 40)
player1_text = font.render(player1_name, True, white)
player2_text = font.render(player2_name, True, white)

# Menu
resume_text = font.render("Resume", True, white)
exit_text = font.render("Exit", True, white)
resume_rect = resume_text.get_rect(center=(1545 // 2, 1.2*678 // 3))
exit_rect = exit_text.get_rect(center=(1545 // 2, 1.4*678 // 3 + 100))
menu = True

# Game Variables
game_running = True
dia = 36
pocket_dia = 66
force = 0
max_force = 10000
force_direction = 1
cue_ball_potted = False
taking_shot = True
powering = False
pottedBalls = []
ballsType1 = []
ballsType2 = []
witch_player = 1

# Load Images
backgroundImg = pygame.image.load("D:\Programming\Python\Projects\Pool\pic\\background6.png").convert_alpha()
tableImg = pygame.image.load("D:\Programming\Python\Projects\Pool\pic\\table.png").convert_alpha()
pocketImg = pygame.image.load("D:\Programming\Python\Projects\Pool\pic\\pocket.png").convert_alpha()
cueImg = pygame.image.load("D:\Programming\Python\Projects\Pool\pic\\cue.png").convert_alpha()
previewImg = pygame.image.load("D:\Programming\Python\Projects\Pool\pic\\preview.png").convert_alpha()
scorebarImg = pygame.image.load("D:\Programming\Python\Projects\Pool\pic\\scorebar.png").convert_alpha()
turnImg = pygame.image.load("D:\Programming\Python\Projects\Pool\pic\\turn.png").convert_alpha()
ballImgs = []
ballImages = []
for i in range(1, 17):
    ball_image = pygame.image.load(f"D:\Programming\Python\Projects\Pool\pic\\ball{i}.png").convert_alpha()
    ballImgs.append(ball_image)
    ballImages.append(ball_image)

# Creating Balls
def create_ball(radius, pos):
    body = pymunk.Body()
    body.position = pos
    shape = pymunk.Circle(body, radius)
    shape.mass = 5
    shape.elasticity = 0.8
    # Use Pivot
    pivot = pymunk.PivotJoint(static_body, body, (0, 0), (0, 0))
    pivot.max_bias = 0
    pivot.max_force = 500

    space.add(body, shape, pivot)
    return shape

# Setup Balls
balls = []
rows = 5
cols = 5
for col in range(cols):
    for row in range(rows):
        pos = (350 + (col * (dia+1)), 420 + (row * (dia+1)) + (col * dia/2))
        new_ball = create_ball(dia/2, pos)
        balls.append(new_ball)
    rows -= 1
pos = (1020, SCREEN_HEIGHT / 2 + 50)
cue_ball = create_ball(dia/2, pos)
balls.append(cue_ball)

# Creating Pockets
pockets = [(158, 200), (698, 197), (1239, 200), (156, 770), (697, 775), (1240, 770)]

# Creating Cushions
cushions = [
    [(160, 185), (185, 203), (670, 203), (679, 185)],
    [(720, 185), (730, 203), (1215, 203), (1235, 185)],
    [(160, 790), (185, 773), (670, 773), (679, 790)],
    [(720, 790), (730, 773), (1215, 773), (1235, 790)],
    [(135, 210), (151, 235), (151, 740), (135, 765)],
    [(1265, 210), (1248, 235), (1248, 740), (1265, 765)],
]
def create_cushion(poly_dims):
    body = pymunk.Body(body_type = pymunk.Body.STATIC)
    body.position = ((0, 0))
    shape = pymunk.Poly(body, poly_dims)
    shape.elasticity = 0.8
    space.add(body, shape)
for c in cushions:
    create_cushion(c)

# Creating Cue
class Cue():
    def  __init__(self, pos):
        self.original_image = cueImg
        self.angle = 0
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect()
        self.rect.center = pos
    def update(self, angle):
        self.angle = angle
    def draw(self, surface):
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        surface.blit(self.image, (self.rect.centerx - self.image.get_width() / 2, self.rect.centery - self.image.get_height() / 2))
cue = Cue(balls[-1].body.position)

# Create Power Bar
powerBar = pygame.Surface((10, 20))
powerBar.fill((0, 0, 200))

# Winner
def text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

# Game Loop
running = True
while running:
    # Clock
    clock.tick(FPS)
    space.step(1/FPS)

    # Background
    screen.blit(backgroundImg, (0, 0))

    # Score Bar
    screen.blit(scorebarImg, (190, 5))

    # Players
    screen.blit(player1_text, (450, 51))
    screen.blit(player2_text, (900, 51))
    
    # Players Turn
    if witch_player == 1:
        screen.blit(turnImg, (85, 50))
    elif witch_player == 2:
        screen.blit(turnImg, (665, 50))

    # Table
    screen.blit(tableImg, (100, 150))
    screen.blit(pocketImg, (1300, 220))

    # Checking Potted
    for i, ball in enumerate(balls):
        for pocket in pockets:
            ball_x_dist = abs(ball.body.position[0] - pocket[0])
            ball_y_dist = abs(ball.body.position[1] - pocket[1])
            ball_dist = math.sqrt((ball_x_dist ** 2) + (ball_y_dist ** 2))
            if ball_dist <= pocket_dia / 2:
                # Checking Cue Ball
                if i == len(balls) - 1:
                    cue_ball_potted = True
                    ball.body.position = (1020, SCREEN_HEIGHT / 2 + 50)
                    ball.body.velocity = (0.0, 0.0)
                    if witch_player == 1:
                        witch_player = 2
                    else: witch_player = 1
                else:
                    ball.body.position = (210, 888)
                    space.remove(ball.body)
                    balls.remove(ball)
                    pottedBalls.append(ballImgs[i])
                    ballImgs.pop(i)
                    if pottedBalls[-1] in ballImages[0:7]:
                        ballsType1.append(pottedBalls[-1])
                    elif pottedBalls[-1] in ballImages[8:15]:
                        ballsType2.append(pottedBalls[-1])
                
            #elif ball_dist > pocket_dia / 2:
                #if witch_player == 1:
                        #witch_player = 2
                #else: witch_player = 1

    # Balls
    for i, ball in enumerate(balls):
        screen.blit(ballImgs[i], (ball.body.position[0] - ball.radius, ball.body.position[1] - ball.radius))
    
    # Checking Balls Stop
    taking_shot = True
    for ball in balls:
        if int(ball.body.velocity[0]) != 0 or int(ball.body.velocity[1]) != 0:
            taking_shot = False

    # Cue
    if taking_shot == True and game_running == True:
        if cue_ball_potted == True:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            screen.blit(previewImg, (mouse_x-20, mouse_y-20))
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 3:  
                        balls[-1].body.position = (mouse_x, mouse_y)
                        cue_ball_potted = False
        mouse_pos = pygame.mouse.get_pos()
        cue.rect.center = balls[-1].body.position
        x = balls[-1].body.position[0] - mouse_pos[0]
        y = -(balls[-1].body.position[1] - mouse_pos[1])
        cue_angle = math.degrees(math.atan2(y, x))
        cue.update(cue_angle)
        cue.draw(screen)

    # Powering
    if powering == True:
        force += 100 * force_direction
        if force >= max_force or force <= 0:
            force_direction *= -1
        # Power Bar
        for b in range(math.ceil(force/2000)):
            screen.blit(powerBar, (balls[-1].body.position[0] - 30 + (b * 15), balls[-1].body.position[1] + 30))
    elif powering == False and taking_shot == True:
        x_impulse = math.cos(math.radians(cue_angle))
        y_impulse = math.sin(math.radians(cue_angle))
        balls[-1].body.apply_impulse_at_local_point((force * -x_impulse, force * y_impulse), (0, 0))
        force = 0
        force_direction = 1

    # Draw Potted Balls
    for i, ball in enumerate(pottedBalls):
        if ball in ballImages[0:7]:
            for j in range(len(ballsType1)):
                screen.blit(ballsType1[j], (207 + (j * 45), 98))
        elif ball in ballImages[8:15]:
            for k in range(len(ballsType2)):
                screen.blit(ballsType2[k], (887 + (k * 45), 98))
        elif ball == ballImages[7] and len(balls) > 1:
            text("You Lost The Game!", font, (255, 0, 0), SCREEN_WIDTH / 2 - 180, SCREEN_HEIGHT / 2 - 100)
            game_running = False
    
    # Fouls Handeling
    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE]:
        if witch_player == 1:
            witch_player = 2
        else: witch_player = 1
        mouse_x, mouse_y = pygame.mouse.get_pos()
        screen.blit(previewImg, (mouse_x-20, mouse_y-20))
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 3:  
                balls[-1].body.position = (mouse_x, mouse_y)

    # Checking Winner
    if len(balls) == 1:
        text("You Won The Game!", font, (255, 255, 255), SCREEN_WIDTH / 2 - 180, SCREEN_HEIGHT / 2 - 100)
        game_running = False

    # Handler
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                clock = pygame.time.Clock()
                clock.tick(60)
                menu = True
                while menu:
                    screen.fill(black)
                    screen.blit(resume_text, resume_rect)
                    screen.blit(exit_text, exit_rect)
                    pygame.display.flip()
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit()
                        elif event.type == pygame.MOUSEBUTTONDOWN:
                            mouse_x, mouse_y = pygame.mouse.get_pos()
                            if resume_rect.collidepoint(mouse_x, mouse_y):
                                menu = False
                            elif exit_rect.collidepoint(mouse_x, mouse_y):
                                pygame.quit()
                                sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and taking_shot == True:
                powering = True
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1 and taking_shot == True:
                shot_sound = mixer.Sound('D:\Programming\Python\Projects\pool\sounds\shot.mp3')
                shot_sound.play()
                powering = False
        if event.type == pygame.QUIT:
            running = False

    #space.debug_draw(draw_options)
    pygame.display.update()

pygame.quit()
