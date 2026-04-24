import pygame
import random

# pygame setup
pygame.init()
screen = pygame.display.set_mode((600,600))
pygame.display.set_caption("snake")
clock = pygame.time.Clock()
running = True

snakedirx = 0
snakediry = -1
player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
player_poses = []

playerlength = 1
applex = False

def snakeonscreen():
    if player_pos.x == 600:
        player_pos.x = 0
    elif player_pos.x == -20:
        player_pos.x = 600
    elif player_pos.y == 600:
        player_pos.y = 0
    elif player_pos.y == -20:
        player_pos.y = 600

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("black")

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


    player_pos.y += 20 * snakediry
    player_pos.x += 20 * snakedirx

    if player_pos in player_poses:
        running = False

    #add snake length when the head collides with the apple
    if player_pos == applepos:
        applex = False
        playerlength += 1

    snakeonscreen()

    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(10)  # limits FPS

pygame.quit()