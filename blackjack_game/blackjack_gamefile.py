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
active = False

#draw game conditions and buttons
def draw_game(act):
    button_list = []
    #initially on startup (not active) only option is to deal new hand
    if not act:
        deal = pygame.draw.rect(screen, 'white', [150, 20, 300, 100], 0, 5)
        pygame.draw.rect(screen, 'green', [150, 20, 300, 100], 3, 5)
        deal_text = font.render('DEAL HAND', True, 'black')
        screen.blit(deal_text, (165, 50))
        button_list.append(deal)



#main game loop
run = True
while run:
    # run game at our framerate and fill screen with bg color
    timer.tick(fps)
    screen.fill('black')
    buttons = draw_game(active)

    #event handling, if quit pressed, then exit game
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.flip()
pygame.quit()