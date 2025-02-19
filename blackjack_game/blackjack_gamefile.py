# blackjack game in python with pygame
import os
import random
import pygame

# Get the directory where the script is located
script_dir = os.path.dirname(os.path.abspath(__file__))
# Construct the path to the cards.webp file relative to the script's directory
cards_path = os.path.join(script_dir, '../images/cards.webp')

# For debugging purposes
print(cards_path)

pygame.init()
#game variables

class Card:
    """The Card class is used to represent any car in the game. They have a value and a Surface."""

    def __init__(self, image: pygame.Surface, value: int):
        """Create the card."""
        self.image = image
        self.value = value
        self.is_ace = value == 11

# card images are from 
# https://pixabay.com/vectors/card-deck-deck-cards-playing-cards-161536/

def open_deck(path: str) -> tuple[list[Card], pygame.Surface]:
    """Open the image of all cards and return the deck of cards."""
    full_image = pygame.image.load(path) # this is an image of all the card together.
    size = full_image.get_size()
    card_size = size[0]/13, size[1]/5
    deck = []
    for i in range(4): # for the 4 colors
        for j, value in enumerate([11, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10]):
            # Extract the image of the card from the image of all cards.
            rect = pygame.Rect(int(j*card_size[0]), int(i*card_size[1]), int(card_size[0]), int(card_size[1]))
            deck.append(Card(full_image.subsurface(rect), value))
    # Extract the back of the cards.
    rect = pygame.Rect(2*card_size[0], 4*card_size[1], card_size[0], card_size[1])
    back = full_image.subsurface(rect)
    random.shuffle(deck)
    return deck, back

#setting up pygame window
WIDTH = 600
HEIGHT = 900
screen = pygame.display.set_mode([WIDTH,HEIGHT])
pygame.display.set_caption('Pygame Blackjack!')
fps = 60
timer = pygame.time.Clock()
font = pygame.font.Font(None, 44)
smaller_font = pygame.font.Font(None, 36)
active = False

game_deck, back = open_deck(cards_path)

# points/user bet input
bet_input_box = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 - 30, 200, 60)
bet_input = 0
points = 100
bet = 0
position_bet_middle = True
show_bet_input = True
show_bet_amount = False


#win, loss, draw/push
records = [0, 0, 0]
player_score = 0
dealer_score = 0
initial_deal = False
my_hand = []
dealer_hand = []
outcome = 0
reveal_dealer = False
hand_active = False
outcome = 0
add_score = False
results = ['', 'PLAYER BUSTED o_O', 'PLAYER WINS! :)', 'DEALER WINS :(', 'TIE GAME...']

#deal cards by selecting randomly from deck, and make function for one card at a time
def deal_cards(current_hand, current_deck):
    card = random.randint(0, len(current_deck))
    current_hand.append(current_deck[card-1])
    current_deck.pop(card-1)
    return current_hand, current_deck

#draw scores for player and dealer on screen
def draw_scores(player, dealer):
    screen.blit(font.render(f'Score: {player}', True, 'white'), (350, 400))
    if reveal_dealer:
        screen.blit(font.render(f'Score: {dealer}', True, 'white'), (350, 100))

#draw cards visually onto screen 
def draw_cards(player_hand, dealer_hand, reveal):
    for i in range(len(player_hand)):
        screen.blit(player_hand[i].image, (70 + (70 * i), 460 + (5 * i)))

    # if player hasn't finished turn, dealer will hide one card
    for i in range(len(dealer_hand)):
        if i != 0 or reveal:
            screen.blit(dealer_hand[i].image, (70 + (70 * i), 165 + (5 * i)))
        else:
            screen.blit(back, (75 + (70 * i), 165 + (5 * i)))

#pass in player or dealer hand and get best score possible
def calculate_score(hand: list[Card]):
    #calculate hand score fresh every time, check how many aces we have
    hand_score = 0
    aces_count = 0
    for card in hand:
        hand_score += card.value # add the value of the card
        aces_count += card.is_ace # add one if the card is an ace.

    # determine how many aces need to be 1 instead of 11 to get under 21 if possible
    if hand_score > 21 and aces_count > 0:
        for _ in range(aces_count):
            if hand_score > 21:
                hand_score -= 10
    return hand_score
    
#draw game conditions and buttons
def draw_game(act, record, result):
    button_list = []
    #initially on startup (not active) only option is to deal new hand
    if not act:
        deal = pygame.draw.rect(screen, 'white', [150, 20, 300, 100], 0, 5)
        pygame.draw.rect(screen, 'green', [150, 20, 300, 100], 3, 5)
        deal_text = font.render('DEAL HAND', True, 'black')
        screen.blit(deal_text, (165, 50))
        button_list.append(deal)

    #once game started, show hit and stand buttons and win/loss records
    elif result == 0:  #show buttons only when the game is running
        hit = pygame.draw.rect(screen, 'white', [0, 700, 300, 100], 0, 5)
        pygame.draw.rect(screen, 'green', [0, 700, 300, 100], 3, 5)
        hit_text = font.render('HIT ME', True, 'black')
        screen.blit(hit_text, (55, 735))
        button_list.append(hit)

        stand = pygame.draw.rect(screen, 'white', [300, 700, 300, 100], 0, 5)
        pygame.draw.rect(screen, 'green', [300, 700, 300, 100], 3, 5)
        stand_text = font.render('STAND', True, 'black')
        screen.blit(stand_text, (355, 735))
        button_list.append(stand)

    #show points (money)
    points_text = font.render(f'Points', True, 'white')
    points_number = font.render(str(points), True, 'white')
    screen.blit(points_text, (475, 10))
    screen.blit(points_number, (497, 50))

    #show win/loss records always
    score_text = font.render(f'Wins: {record[0]}   Losses: {record[1]}   Draws: {record[2]}', True, 'white')
    screen.blit(score_text, (15, 840))

    #if the game is over, show "NEW HAND" button
    if result != 0:
        screen.blit(font.render(results[result], True, 'white'), (15, 25))
        deal = pygame.draw.rect(screen, 'white', [150, 220, 300, 100], 0, 5)
        pygame.draw.rect(screen, 'green', [150, 220, 300, 100], 3, 5)
        pygame.draw.rect(screen, 'black', [153, 223, 294, 94], 3, 5)
        deal_text = font.render('NEW HAND', True, 'black')
        screen.blit(deal_text, (165, 250))
        button_list.append(deal)

    return button_list

#check endgame conditions function
def check_endgame(hand_active, deal_score, player_score, result, totals, add_score, points, bet, show_bet_amount, show_bet_input, bet_input):
    # check end game scenaris if player has stood, busted or blackjacked
    # result 1- player bust, 2-win, 3-loss, 4-push
    if not hand_active and deal_score >= 17:
        if player_score > 21:
            result = 1
            if not show_bet_input:
                bet = 0
                show_bet_amount = False
                show_bet_input = True
        elif deal_score < player_score <= 21 or deal_score > 21:
            result = 2
            if not show_bet_input:
                points = points + bet + bet
                bet = 0
                show_bet_amount = False
                show_bet_input = True
        elif player_score < deal_score <= 21:
            result = 3
            if not show_bet_input:
                bet = 0
                show_bet_amount = False
                show_bet_input = True
        else:
            result = 4
            if not show_bet_input:
                points = points + bet
                bet = 0
                show_bet_amount = False
                show_bet_input = True
        if add_score:
            if result == 1 or result == 3:
                totals[1] += 1
            elif result == 2:
                totals[0] += 1
            else:
                totals[2] += 1
            add_score = False
    return result, totals, add_score, points, bet, show_bet_amount, show_bet_input, bet_input

#main game loop
run = True
while run:
    # run game at our framerate and fill screen with bg color
    timer.tick(fps)
    screen.fill('black')
    #initial deal to player and dealer
    if initial_deal:
        for i in range(2):
            my_hand, game_deck = deal_cards(my_hand, game_deck)
            dealer_hand, game_deck = deal_cards(dealer_hand, game_deck)
        initial_deal = False
    #once game is activated, and dealt, calculate scores and display cards
    if active:
        player_score = calculate_score(my_hand)
        draw_cards(my_hand, dealer_hand, reveal_dealer)
        if reveal_dealer:
            dealer_score = calculate_score(dealer_hand)
            if dealer_score < 17:
                dealer_hand, game_deck = deal_cards(dealer_hand, game_deck)
        draw_scores(player_score, dealer_score) 
    buttons = draw_game(active, records, outcome)

    #event handling, if quit pressed, then exit game
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        # Input bet
        elif event.type == pygame.KEYDOWN:
                
            if event.key == pygame.K_BACKSPACE:
                try:
                    bet_input = int(str(bet_input)[:-1])  # Remove last character
                except ValueError:
                    bet_input = 0

            elif event.unicode.isdigit():  # Accept only numbers
                bet_input = int(str(bet_input) + str(event.unicode))

            bet = int(bet_input)

        elif event.type == pygame.MOUSEBUTTONUP:

            if len(buttons) > 0 and buttons[0].collidepoint(event.pos) and outcome != 0:
                show_bet_input = False
                points = points - bet_input
                bet = bet_input
                bet_input = 0
                show_bet_amount = True
                active = True
                initial_deal = True
                reveal_dealer = False
                game_deck, back = open_deck(cards_path)
                my_hand = []
                dealer_hand = []
                outcome = 0
                hand_active = True
                add_score = True
                dealer_score = 0
                player_score = 0

            # If game is not active, check DEAL HAND button (usually first button)
            elif not active and len(buttons) > 0 and buttons[0].collidepoint(event.pos):
                position_bet_middle = False
                points = points - bet
                show_bet_input = False
                show_bet_amount = True
                active = True
                initial_deal = True
                game_deck, back = open_deck(cards_path)
                my_hand = []
                dealer_hand = []
                outcome = 0
                hand_active = True
                outcome = 0
                add_score = True

            # During game: HIT or STAND
            elif active and len(buttons) >= 2:
                # HIT button (usually first during game)
                if buttons[0].collidepoint(event.pos) and player_score < 21 and hand_active:
                    my_hand, game_deck = deal_cards(my_hand, game_deck)

                # STAND button (usually second during game)
                elif buttons[1].collidepoint(event.pos) and not reveal_dealer:
                    reveal_dealer = True
                    hand_active = False

    if show_bet_input:
        if not position_bet_middle:
            bet_input_box = pygame.Rect(WIDTH // 2 - 100, 1450 // 2 - 30, 200, 60)
        # Render the bet prompt
        bet_prompt = font.render('How much to bet?', True, 'white')
        screen.blit(bet_prompt, (bet_input_box.x, bet_input_box.y - 40))

        # Draw the input box
        pygame.draw.rect(screen, (255, 255, 255), bet_input_box, border_radius=10)

        # Render the user input inside the box
        text_surface = font.render(str(bet_input), True, (0, 0, 0))
        screen.blit(text_surface, (bet_input_box.x + 10, bet_input_box.y + 15))

    if show_bet_amount == True:
        #show betted amount
        bet_text = font.render(f'Bet', True, 'white')
        bet_amount = font.render(str(bet), True, 'white')
        screen.blit(bet_text, (385, 10))
        screen.blit(bet_amount, (385, 50))

    #if player busts, automatically end turn - treat like a stand
    if hand_active and player_score >= 21:
        hand_active = False
        reveal_dealer = True
    
    outcome, records, add_score, points, bet, show_bet_amount, show_bet_input, bet_input = check_endgame(hand_active, dealer_score, player_score, outcome, records, add_score, points, bet, show_bet_amount, show_bet_input, bet_input)
    
    pygame.display.flip()
pygame.quit()