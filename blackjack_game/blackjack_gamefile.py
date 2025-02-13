# blackjack game in python with pygame
import copy
import random
import pygame

#game variables
cards = ['2','3','4','5','6','7','8','9','10','J','Q','K','A',]
one_deck = 4 * cards
decks = 4
game_deck = copy.deepcopy(decks * one_deck)
print(game_deck)