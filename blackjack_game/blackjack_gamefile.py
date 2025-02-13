# blackjack game in python with pygame
import copy
import random
import pygame

pygame.init()
#game variables
cards = ['2','3','4','5','6','7','8','9','10','J','Q','K','A',]
one_deck = 4 * cards
decks = 4
game_deck = copy.deepcopy(decks * one_deck)
print(game_deck)

#setting up pygame window
WIDTH = 600
HEIGHT = 900
screen = pygame.display.set_mode([WIDTH,HEIGHT])
pygame.display.set_caption('Pygame Blackjack!')
fps = 60
timer = pygame.time.Clock()
pygame.font.init()
font = pygame.font.Font(None, 36)


#main game loop
run = True
while run:
    # run game at our framerate and fill screen with bg color
    timer.tick(fps)
    screen.fill('black')

    #event handling, if quit pressed, then exit game
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.flip()
pygame.quit()