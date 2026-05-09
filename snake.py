import pygame, random, time, json
from datetime import datetime

# pygame setup
pygame.init()
pygame.font.init()
screen = pygame.display.set_mode((600,600))
pygame.display.set_caption("snake")
clock = pygame.time.Clock()
pygame.mixer.init()
running = True
gmstart = False
scoreb = False

snakedirx = 0
snakediry = -1
player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
player_poses = []

playerlength = 1
applex = False

gmfont = pygame.font.SysFont('Arial',50)
sfont = pygame.font.SysFont('Arial',20)
title = gmfont.render("Simple Snake", False, "white")
scoretitle = gmfont.render("Score", False, "white")

appleeaten = pygame.mixer.Sound("sfx/appleeat.wav")
bpressfx = pygame.mixer.Sound("sfx/bpress.wav")
gmoversfx = pygame.mixer.Sound("sfx/gameover.wav")

scores = {}
scoreindex = 1

class button:
    def __init__(self,xpos,ypos,width,height,text):
        self.xpos = xpos
        self.ypos = ypos
        self.width = width
        self.height = height
        self.text = text
        self.brect = pygame.Rect(xpos,ypos,width,height)
        self.innerbrect = pygame.Rect(xpos + 3,ypos + 3,width - 5,height - 5)

    def draw(self):
        pygame.draw.rect(screen,"white",self.brect)
        pygame.draw.rect(screen,"black",self.innerbrect)
        text = gmfont.render(self.text, False, "white")
        screen.blit(text, (self.xpos,self.ypos + 5))

    def start(self):
        mospos = pygame.mouse.get_pos()
        if self.brect.collidepoint(mospos[0],mospos[1]):
            if pygame.mouse.get_pressed()[0]:
                global bpressfx
                global gmstart
                bpressfx.play()
                gmstart = True

    def scores(self):
        mospos = pygame.mouse.get_pos()
        if self.brect.collidepoint(mospos[0],mospos[1]):
            if pygame.mouse.get_pressed()[0]:
                global bpressfx
                global scoreb
                bpressfx.play()
                scoreb = True

    def back(self):
        mospos = pygame.mouse.get_pos()
        if self.brect.collidepoint(mospos[0],mospos[1]):
            if pygame.mouse.get_pressed()[0]:
                global bpressfx
                global scoreb
                bpressfx.play()
                scoreb = False

    def quit(self):
        mospos = pygame.mouse.get_pos()
        if self.brect.collidepoint(mospos[0],mospos[1]):
            if pygame.mouse.get_pressed()[0]:
                global bpressfx
                global running
                bpressfx.play()
                running = False

def pccontrols():
    global snakedirx
    global snakediry

    # movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        if snakediry != 1:
            snakediry = -1
            snakedirx = 0
    if keys[pygame.K_s]:
        if snakediry != -1:
            snakediry = 1
            snakedirx = 0
    if keys[pygame.K_a]:
        if snakedirx != 1:
            snakedirx = -1
            snakediry = 0
    if keys[pygame.K_d]:
        if snakedirx != -1:
            snakedirx = 1
            snakediry = 0

def snakeonscreen():
    if player_pos.x == 600:
        player_pos.x = 0
    elif player_pos.x == -20:
        player_pos.x = 600
    elif player_pos.y == 600:
        player_pos.y = 0
    elif player_pos.y == -20:
        player_pos.y = 600

def game():
    screen.fill("black")

    global running
    global applex
    global apple
    global applepos
    global player_pos
    global player_poses
    global playerlength
    global snakediry
    global snakedirx
    #make apple appear in random places if it doesnt exist. if the random place is in the snake,try again until not.
    if applex != True:
        applepos = pygame.Vector2(random.randrange(0,600, 20),random.randrange(0,600, 20))
        if applepos in player_poses or applepos == player_pos:
            while applepos in player_poses or applepos == player_pos:
                applepos = pygame.Vector2(random.randrange(0,600, 20),random.randrange(0,600, 20))
        apple = {"color":"red","position" : pygame.Rect(applepos.x,applepos.y,20,20)}
        applex = True

    oldpos = pygame.Vector2(player_pos.x,player_pos.y)
    #add new pos so it follows snake and remove old ones
    player_poses.append(oldpos)
    if len(player_poses) > playerlength:
        player_poses.remove(player_poses[0])

    #draw snake body
    for pos in player_poses:
        pygame.draw.rect(screen,"white",pygame.Rect(pos.x,pos.y,20,20))

    #draw snake head and apple
    pygame.draw.rect(screen,"white",pygame.Rect(player_pos.x,player_pos.y,20,20))
    pygame.draw.rect(screen,apple["color"],apple["position"])

    pccontrols()

    player_pos.y += 20 * snakediry
    player_pos.x += 20 * snakedirx

    #game over
    if player_pos in player_poses:
        global gmoversfx
        global gmstart
        global scoreb
        global scoreindex
        gmoversfx.play()
        time.sleep(2)
        date = datetime.now()

        score = {
            "length": playerlength,
            "day" : date.day,
            "month" : date.month,
            "year" : date.year
        }
        scores.update({"score" + str(scoreindex) : score})
        scoreindex += 1
        print(scores)
        player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
        player_poses = []
        playerlength = 1
        snakedirx = 0
        snakediry = -1
        applex = False
        gmstart = False
        scoreb = True


    #add snake length when the head collides with the apple
    if player_pos == applepos:
        global appleeaten
        appleeaten.play()
        applex = False
        playerlength += 1

    snakeonscreen()

def scoreboard():
    screen.fill("black")
    global scores

    pygame.draw.rect(screen,"white",pygame.Rect(105,50,400,500))
    pygame.draw.rect(screen,"black",pygame.Rect(110,55,390,490))
    screen.blit(scoretitle,(240,60))
    if scores:
        i = 0
        for x in scores.items():
            for obj in x:
                scoretxt = sfont.render(str(obj),False,"white")
                screen.blit(scoretxt,(100,120 + i))
                i += 50


    backbutton.draw()


exitbutton = button(200,400,200,70,"    Exit")
startbutton = button(200,200,200,70,"    Play")
scorebutton = button(200,300,200,70,"   Score")

backbutton = button(200,500,200,70, "    back")

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            if gmstart == False and scoreb == False:
                exitbutton.quit()
                scorebutton.scores()
                startbutton.start()
            elif scoreb == True and gmstart == False:
                backbutton.back()
        if event.type == pygame.QUIT:
            running = False

    if gmstart == False and scoreb == False:
        screen.fill("black")
        screen.blit(title,(150,120))
        startbutton.draw()
        scorebutton.draw()
        exitbutton.draw()
    elif gmstart == True and scoreb == False:
        game()
    elif scoreb == True and gmstart == False:
        scoreboard()

    pygame.display.flip() # show your work
    clock.tick(10)  # limits FPS

pygame.mixer.quit()
pygame.quit()