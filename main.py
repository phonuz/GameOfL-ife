import pygame
pygame.init()

import globals
import gameoflife

def drawCell(color, x, y, size):
    global screen
    pygame.draw.rect(screen, color, pygame.Rect(x, y, size, size) )
           
gameoflife = gameoflife.GameOfLife()

screen = pygame.display.set_mode((globals.SCREEN_WIDTH, globals.SCREEN_HEIGHT))

showCells = False
isEvolving = False
evolutionRate = 10
evolutionCounter = 0

clock = pygame.time.Clock()
FPS = 60

running = True
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                if showCells:
                    isEvolving = not(isEvolving)
            if event.key == pygame.K_g:
                showCells = True
                isEvolving = False
                gameoflife.seedCells()

    if isEvolving:
        if evolutionCounter < evolutionRate:
            evolutionCounter += 1
        else:
            gameoflife.updateCells()
            evolutionCounter = 0

    screen.fill(globals.FIELD_COLOR)

    if showCells:
        gameoflife.drawCells(drawCell)    

    pygame.display.flip()

    clock.tick(FPS)

pygame.quit()     