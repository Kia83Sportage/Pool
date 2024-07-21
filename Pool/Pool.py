import pygame
from pygame import mixer
import pymunk
import pymunk.pygame_util
import math
import sys

def Eight_Ball():
    # Screen
    SCREEN_WIDTH = 1545
    SCREEN_HEIGHT = 880
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("8 Ball")
    icon = pygame.image.load("D:\Programming\Python\Projects\Pool\pic\\icon.png")
    pygame.display.set_icon(icon)

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
    foul_checking = True
    foul_done = False
    aa = False
    pottedBalls = []
    ballsType1 = []
    ballsType2 = []
    player1_type = 0
    player2_type = 0
    lastpottedball_x = 1200
    lastpottedball_y = 231
    witch_player = 1
    counter1 = 0
    counter2 = 0

    # Load Images
    backgroundImg = pygame.image.load("D:\Programming\Python\Projects\Pool\pic\\background4.png").convert_alpha()
    tableImg = pygame.image.load("D:\Programming\Python\Projects\Pool\pic\\table1.png").convert_alpha()
    pocketImg = pygame.image.load("D:\Programming\Python\Projects\Pool\pic\\pocket.png").convert_alpha()
    cueImg = pygame.image.load("D:\Programming\Python\Projects\Pool\pic\\cue.png").convert_alpha()
    previewImg = pygame.image.load("D:\Programming\Python\Projects\Pool\pic\\preview.png").convert_alpha()
    scorebarImg = pygame.image.load("D:\Programming\Python\Projects\Pool\pic\\scorebar.png").convert_alpha()
    turnImg = pygame.image.load("D:\Programming\Python\Projects\Pool\pic\\turn.png").convert_alpha()
    timeImg = pygame.image.load("D:\Programming\Python\Projects\Pool\pic\\time.png").convert_alpha()
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
        # Handler
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    clock = pygame.time.Clock()
                    clock.tick(60)
                    menu = True
                    while menu:
                        screen.blit(backgroundImg, (0,0))
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
                    if player1_type == 0:
                        if counter1 % 2 == 0:
                            witch_player = 2
                        else: witch_player = 1
                        counter1 += 1
                    else: aa = True
            if event.type == pygame.QUIT:
                running = False
     
        # Clock
        clock.tick(FPS)
        space.step(1/FPS)

        # Background
        screen.blit(backgroundImg, (0, 0))

        # Score Bar
        screen.blit(scorebarImg, (190, 5))

        # Players
        screen.blit(player1_text, (430, 51))
        screen.blit(player2_text, (900, 51))
    
        # Players Turn
        if witch_player == 1:
            screen.blit(turnImg, (270, 53))
        elif witch_player == 2:
            screen.blit(turnImg, (1105, 53))

        # Players Time
        if witch_player == 1:
            screen.blit(timeImg, (518, 25))
        elif witch_player == 2:
            screen.blit(timeImg, (765, 25))

        # Draw Potted Balls
        screen.blit(pocketImg, (1300, 220))
        if len(pottedBalls) > 0:
            if lastpottedball_x <= 1334:
                lastpottedball_x += 1
                screen.blit(pottedBalls[-1], (lastpottedball_x, lastpottedball_y))
            if lastpottedball_x >= 1330 and lastpottedball_y <= 773 - (38 * (len(pottedBalls)-1)):
                lastpottedball_y += 1
                screen.blit(pottedBalls[-1], (lastpottedball_x, lastpottedball_y))
            if lastpottedball_x >= 1334 and lastpottedball_y >= 773 - (38 * (len(pottedBalls)-1)):
                screen.blit(pottedBalls[-1], (lastpottedball_x, lastpottedball_y))
        for i in range(len(pottedBalls)-1):
                screen.blit(pottedBalls[i], (1334, 773 - (38 * i)))
            
        # Table
        screen.blit(tableImg, (100, 150))

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
                        lastpottedball_x = 1200
                        lastpottedball_y = 231
                        ballImgs.pop(i)
                        if pottedBalls[-1] in ballImages[0:7]:
                            ballsType1.append(pottedBalls[-1])
                        elif pottedBalls[-1] in ballImages[8:15]:
                            ballsType2.append(pottedBalls[-1]) 

        # Set Players Type
        if len(pottedBalls) == 1 and player1_type == 0:
            if (pottedBalls[0] in ballImages[0:7] and witch_player == 1) or (pottedBalls[0] in ballImages[8:15] and witch_player == 2):
                player1_type = 1
                player2_type = 2
            elif (pottedBalls[0] in ballImages[0:7] and witch_player == 2) or (pottedBalls[0] in ballImages[8:15] and witch_player == 1):
                player1_type = 2
                player2_type = 1

        # Balls
        for i, ball in enumerate(balls):
            screen.blit(ballImgs[i], (ball.body.position[0] - ball.radius, ball.body.position[1] - ball.radius))
    
        # Checking Balls Stop
        taking_shot = True
        for ball in balls:
            if int(ball.body.velocity[0]) != 0 or int(ball.body.velocity[1]) != 0:
                taking_shot = False 
    
        # Checking Pitok
        if taking_shot == True and len(pottedBalls) == counter2 and aa == True:
            if witch_player == 1: witch_player = 2
            else: witch_player = 1
            aa = False
        elif taking_shot == True and len(pottedBalls) != counter2 and aa == True:
            for ball in pottedBalls:
                if ball in ballsType1 and player1_type == 1 and witch_player == 2:
                    witch_player = 1
                elif ball in ballsType1 and player2_type == 1 and witch_player == 1:
                    witch_player = 2
                elif ball in ballsType2 and player1_type == 2 and witch_player == 2:
                    witch_player = 1
                elif ball in ballsType2 and player1_type == 2 and witch_player == 1:
                    witch_player = 2
                counter2 = len(pottedBalls)
                aa = False
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
            foul_checking = True

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

        # Draw Scored Balls
        for i, ball in enumerate(pottedBalls):
            if ball in ballImages[0:7] and player1_type == 1 and player2_type == 2:
                for j in range(len(ballsType1)):
                    screen.blit(ballsType1[j], (207 + (j * 45), 98))
                for k in range(len(ballsType2)):
                    screen.blit(ballsType2[k], (887 + (k * 45), 98))
            elif ball in ballImages[0:7] and player1_type == 2 and player2_type == 1:
                for j in range(len(ballsType1)):
                    screen.blit(ballsType1[j], (887 + (j * 45), 98))
                for k in range(len(ballsType2)):
                    screen.blit(ballsType2[k], (207 + (k * 45), 98))
            elif ball == ballImages[7] and len(balls) > 1:
                text("You Lost The Game!", font, (255, 0, 0), SCREEN_WIDTH / 2 - 180, SCREEN_HEIGHT / 2 - 100)
                game_running = False
    
        # Fouls Handeling
        if foul_checking == True and len(pottedBalls) > 1:
            for i in range(len(balls)-1):
                if int(balls[i].body.velocity[0]) != 0 or int(balls[i].body.velocity[1]) != 0:
                    foul_checking = False
                    if (0 <= i <= 7 and witch_player == 1 and player1_type == 2) or (8 <= i <= 15 and witch_player == 1 and player1_type == 1):
                        witch_player = 2
                        foul_done = True
                    elif (0 <= i <= 7 and witch_player == 2 and player2_type == 2) or (8 <= i <= 15 and witch_player == 2 and player2_type == 1):
                        witch_player = 1
                        foul_done = True
        if foul_done == True:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            screen.blit(previewImg, (mouse_x-20, mouse_y-20))
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 3:  
                        balls[-1].body.position = (mouse_x, mouse_y)
                        foul_done = False
                    
        # Checking Winner
        if len(ballsType1) == 7:
            text("You Won The Game!", font, (255, 255, 255), SCREEN_WIDTH / 2 - 180, SCREEN_HEIGHT / 2 - 100)
            game_running = False

        #space.debug_draw(draw_options)
        pygame.display.update()

    pygame.quit()

def Snooker():
    # Screen
    SCREEN_WIDTH = 1545
    SCREEN_HEIGHT = 880
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Snooker")

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
    font1 = pygame.font.Font(None, 40)
    font2 = pygame.font.Font(None, 45)
    player1_score = 0
    player2_score = 0
    player1_text = font1.render(player1_name, True, white)
    player2_text = font1.render(player2_name, True, white)

    # Menu
    resume_text = font1.render("Resume", True, white)
    exit_text = font1.render("Exit", True, white)
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
    red_potted = False
    taking_shot = True
    powering = False
    pottedBalls = []
    allBalls = []
    player1_balls = []
    player2_balls = []
    counter = 0
    lastpottedball_x = 1200
    lastpottedball_y = 231
    witch_player = 1

    # Load Images
    backgroundImg = pygame.image.load("D:\Programming\Python\Projects\Pool\pic\\background8.png").convert_alpha()
    scorebarImg = pygame.image.load("D:\Programming\Python\Projects\Pool\pic\\scorebar.png").convert_alpha()
    tableImg = pygame.image.load("D:\Programming\Python\Projects\Pool\pic\\table2.png").convert_alpha()
    pocketImg = pygame.image.load("D:\Programming\Python\Projects\Pool\pic\\pocket.png").convert_alpha()
    cueImg = pygame.image.load("D:\Programming\Python\Projects\Pool\pic\\cue.png").convert_alpha()
    previewImg = pygame.image.load("D:\Programming\Python\Projects\Pool\pic\\preview.png").convert_alpha()
    turnImg = pygame.image.load("D:\Programming\Python\Projects\Pool\pic\\turn.png").convert_alpha()
    timeImg = pygame.image.load("D:\Programming\Python\Projects\Pool\pic\\time.png").convert_alpha()
    redImg = pygame.image.load("D:\Programming\Python\Projects\Pool\pic\\red.png").convert_alpha()
    pinkImg = pygame.image.load("D:\Programming\Python\Projects\Pool\pic\\pink.png").convert_alpha()
    blueImg = pygame.image.load("D:\Programming\Python\Projects\Pool\pic\\blue.png").convert_alpha()
    greenImg = pygame.image.load("D:\Programming\Python\Projects\Pool\pic\\green.png").convert_alpha()
    brownImg = pygame.image.load("D:\Programming\Python\Projects\Pool\pic\\brown.png").convert_alpha()
    yellowImg = pygame.image.load("D:\Programming\Python\Projects\Pool\pic\\yellow.png").convert_alpha()
    whiteImg = pygame.image.load("D:\Programming\Python\Projects\Pool\pic\\white.png").convert_alpha()
    blackImg = pygame.image.load("D:\Programming\Python\Projects\Pool\pic\\black.png").convert_alpha()
    ballImgs = []
    ballImages = []
    redBalls = []
    coloursBalls = [blackImg, pinkImg, blueImg, greenImg, brownImg, yellowImg]
    for i in range(15):
        redBalls.append(redImg)
    ballImgs = redBalls + coloursBalls
    ballImgs.append(whiteImg)
    ballImages.append(redImg)
    ballImages += coloursBalls
    ballImages.append(whiteImg)

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
    pos = (250, SCREEN_HEIGHT / 2 + 50)
    blackBall = create_ball(dia/2, pos)
    balls.append(blackBall)
    pos = (538, SCREEN_HEIGHT / 2 + 52)
    pinkBall = create_ball(dia/2, pos)
    balls.append(pinkBall)
    pos = (700, SCREEN_HEIGHT / 2 + 50)
    blueBall = create_ball(dia/2, pos)
    balls.append(blueBall)
    pos = (1020, SCREEN_HEIGHT / 2 + 140)
    greenBall = create_ball(dia/2, pos)
    balls.append(greenBall)
    pos = (1020, SCREEN_HEIGHT / 2 + 50)
    brownBall = create_ball(dia/2, pos)
    balls.append(brownBall)
    pos = (1020, SCREEN_HEIGHT / 2 - 40)
    yellowBall = create_ball(dia/2, pos)
    balls.append(yellowBall)
    pos = (1080, SCREEN_HEIGHT / 2 + 50)
    whiteBall = create_ball(dia/2, pos)
    balls.append(whiteBall)

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
    powerBar.fill((200, 0, 0))

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
        screen.blit(player1_text, (430, 51))
        screen.blit(player2_text, (900, 51))

        # Players Turn
        if witch_player == 1:
            screen.blit(turnImg, (270, 53))
        elif witch_player == 2:
            screen.blit(turnImg, (1105, 53))

        # Players Time
        if witch_player == 1:
            screen.blit(timeImg, (518, 25))
        elif witch_player == 2:
            screen.blit(timeImg, (765, 25))

        # Scores
        player1_scores = font2.render(str(player1_score), True, black)
        player2_scores= font2.render(str(player2_score), True, black)
        screen.blit(player1_scores, (227, 48))
        screen.blit(player2_scores, (1158, 48))
    
        # Players Turn
        if witch_player == 1:
            screen.blit(turnImg, (270, 53))
        elif witch_player == 2:
            screen.blit(turnImg, (1105, 53))

        # Draw Potted Balls
        screen.blit(pocketImg, (1300, 220))
        if len(pottedBalls) > 0:
            if lastpottedball_x <= 1334:
                lastpottedball_x += 1
                screen.blit(pottedBalls[-1], (lastpottedball_x, lastpottedball_y))
            if lastpottedball_x >= 1330 and lastpottedball_y <= 773 - (38 * (len(pottedBalls)-1)):
                lastpottedball_y += 1
                screen.blit(pottedBalls[-1], (lastpottedball_x, lastpottedball_y))
            if lastpottedball_x >= 1334 and lastpottedball_y >= 773 - (38 * (len(pottedBalls)-1)):
                screen.blit(pottedBalls[-1], (lastpottedball_x, lastpottedball_y))
        for i in range(len(pottedBalls)-1):
                screen.blit(pottedBalls[i], (1334, 773 - (38 * i)))

        # Tables
        screen.blit(tableImg, (100, 150))

        # Checking Potted
        for i, ball in enumerate(balls):
            for pocket in pockets:
                ball_x_dist = abs(ball.body.position[0] - pocket[0])
                ball_y_dist = abs(ball.body.position[1] - pocket[1])
                ball_dist = math.sqrt((ball_x_dist ** 2) + (ball_y_dist ** 2))
                if ball_dist <= pocket_dia / 2:
                    # Checking Cue Ball
                    match i + len(pottedBalls):
                        case 21:
                            cue_ball_potted = True
                            ball.body.position = (1070, SCREEN_HEIGHT / 2 + 50)
                            ball.body.velocity = (0.0, 0.0)
                        case 15:
                            if red_potted == True:
                                if witch_player == 1:
                                    player1_balls.append(ball)
                                    player1_score += 7
                                else: 
                                    player2_balls.append(ball)
                                    player2_score += 7
                            else:
                                if witch_player == 1:
                                    witch_player = 2
                                else:
                                    witch_player = 1
                                ball.body.position = (250, SCREEN_HEIGHT / 2 + 50)
                                ball.body.velocity = (0.0, 0.0)
                                red_potted = False
                                allBalls.append(ball)
                        case 16:
                            if red_potted == True:
                                if witch_player == 1:
                                    player1_balls.append(ball)
                                    player1_score += 6
                                else: 
                                    player2_balls.append(ball)
                                    player2_score += 6
                            else:
                                if witch_player == 1:
                                    witch_player = 2
                                else:
                                    witch_player = 1
                                ball.body.position = (538, SCREEN_HEIGHT / 2 + 52)
                                ball.body.velocity = (0.0, 0.0)
                                red_potted = False
                                allBalls.append(ball)
                        case 17:
                            if red_potted == True:
                                if witch_player == 1:
                                    player1_balls.append(ball)
                                    player1_score += 5
                                else: 
                                    player2_balls.append(ball)
                                    player2_score += 5
                            else:
                                if witch_player == 1:
                                    witch_player = 2
                                else:
                                    witch_player = 1
                                ball.body.position = (700, SCREEN_HEIGHT / 2 + 50)
                                ball.body.velocity = (0.0, 0.0)
                                red_potted = False
                                allBalls.append(ball)
                        case 18:
                            if red_potted == True:
                                if witch_player == 1:
                                    player1_balls.append(ball)
                                    player1_score += 3
                                else:
                                    player2_balls.append(ball)
                                    player2_score += 3
                            else:
                                if witch_player == 1:
                                    witch_player = 2
                                else:
                                    witch_player = 1
                                ball.body.position = (1020, SCREEN_HEIGHT / 2 + 140)
                                ball.body.velocity = (0.0, 0.0)
                                red_potted = False
                                allBalls.append(ball)
                        case 19:
                            if red_potted == True:
                                if witch_player == 1:
                                    player1_balls.append(ball)
                                    player1_score += 4
                                else:
                                    player2_balls.append(ball)
                                    player2_score += 4
                            else:
                                if witch_player == 1:
                                    witch_player = 2
                                else:
                                    witch_player = 1
                                ball.body.position = (1020, SCREEN_HEIGHT / 2 + 50)
                                ball.body.velocity = (0.0, 0.0)
                                red_potted = False
                                allBalls.append(ball)
                        case 20:
                            if red_potted == True:
                                if witch_player == 1:
                                    player1_balls.append(ball)
                                    player1_score += 2
                                else:
                                    player2_balls.append(ball)
                                    player2_score += 2
                            else:
                                if witch_player == 1:
                                    witch_player = 2
                                else:
                                    witch_player = 1
                            ball.body.position = (1020, SCREEN_HEIGHT / 2 - 40)
                            ball.body.velocity = (0.0, 0.0)
                            red_potted = False
                            allBalls.append(ball)
                        case _:
                            if witch_player == 1:
                                player1_balls.append(ball)
                                player1_score += 1
                            else:
                                player2_balls.append(ball)
                                player2_score += 1
                            ball.body.position = (210, 888)
                            space.remove(ball.body)
                            balls.remove(ball)
                            pottedBalls.append(ballImgs[i])
                            lastpottedball_x = 1200
                            lastpottedball_y = 231
                            ballImgs.pop(i)
                            red_potted = True
                            allBalls.append(ball)
    
        # Draw Scored Balls
        for ball in player1_balls:
            if ball == ballImages[0]:
                print("no")
                screen.blit(ball, (252, 98))
            elif ball == ballImages[1]:
                screen.blit(ball, (297, 98))
            elif ball == ballImages[2]:
                screen.blit(ball, (342, 98))
            elif ball == ballImages[3]:
                screen.blit(ball, (387, 98))
            elif ball == ballImages[4]:
                screen.blit(ball, (432, 98))
            elif ball == ballImages[5]:
                screen.blit(ball, (477, 98))
            elif ball == ballImages[6]:
                screen.blit(ball, (522, 98))
        for ball in player2_balls:
            if ball == ballImages[0]:
                print("yes")
                screen.blit(ball, (932, 98))
            elif ball == ballImages[1]:
                screen.blit(ball, (977, 98))
            elif ball == ballImages[2]:
                screen.blit(ball, (1022, 98))
            elif ball == ballImages[3]:
                screen.blit(ball, (1067, 98))
            elif ball == ballImages[4]:
                screen.blit(ball, (1112, 98))
            elif ball == ballImages[5]:
                screen.blit(ball, (1157, 98))
            elif ball == ballImages[6]:
                screen.blit(ball, (1202, 98))

        # Checking Pitok
        if counter != len(allBalls):
            if witch_player == 1:
                witch_player = 2
            else:
                witch_player = 1
            counter = len(allBalls)
        else:
            if witch_player == 1:
                witch_player = 1
            else:
                witch_player = 2

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

        # Handler
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    clock = pygame.time.Clock()
                    clock.tick(60)
                    menu = True
                    while menu:
                        screen.blit(backgroundImg, (0, 0))
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
                    shot_sound = mixer.Sound('D:\Programming\Python\Projects\Pool\sounds\shot.mp3')
                    shot_sound.play()
                    powering = False
                    counter += 1
            if event.type == pygame.QUIT:
                running = False

        #space.debug_draw(draw_options)
        pygame.display.update()

    pygame.quit()

def Main():
    pygame.init()

    SCREEN_WIDTH = 1545
    SCREEN_HEIGHT = 880

    # Start Screen
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    # Background
    backgroundImg = pygame.image.load("D:\Programming\Python\Projects\Pool\pic\\background3.png").convert_alpha()
    screen.blit(backgroundImg, (0, 0))

    # Colors
    white = (255, 255, 255)
    black = (0, 0, 0)
    blue = (0, 0, 255)
    green = (0, 255, 0)

    # Font
    font = pygame.font.Font(None, 74)

    # Menu
    resume_text = font.render("Resume", True, white)
    exit_text = font.render("Exit", True, white)
    resume_rect = resume_text.get_rect(center=(1545 // 2, 1.2*678 // 3))
    exit_rect = exit_text.get_rect(center=(1545 // 2, 1.4*678 // 3 + 100))
    text_8ball = font.render('Eight Ball', True, blue)
    text_snooker = font.render('Snooker', True, green)
    eightball_rect = text_8ball.get_rect(center=(1545 // 2, 1.2*678 // 3))
    snooker_rect = text_snooker.get_rect(center=(1545 // 2, 1.4*678 // 3 + 100))
    screen.blit(text_8ball, eightball_rect)
    screen.blit(text_snooker, snooker_rect)
    menu = True

    # Main loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if eightball_rect.collidepoint(mouse_x, mouse_y):
                    Eight_Ball()
                elif snooker_rect.collidepoint(mouse_x, mouse_y):
                    Snooker()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                        clock = pygame.time.Clock()
                        clock.tick(60)
                        menu = True
                        while menu:
                            screen.blit(backgroundImg, (0, 0))
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
            if event.type == pygame.QUIT:
                running = False

        # Update the display
        pygame.display.flip()

Main()

