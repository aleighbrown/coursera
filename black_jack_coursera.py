# Mini-project #6 - Blackjack
#built for Rice University's coursera course
#works in their provided gui environment
#link to actually play the game: http://www.codeskulptor.org/#user40_vMN5KTUxnd_18.py

import simplegui
import random

# load card sprite - 936x384 - source: jfitz.com
CARD_SIZE = (72, 96)
CARD_CENTER = (36, 48)
card_images = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/cards_jfitz.png")

CARD_BACK_SIZE = (72, 96)
CARD_BACK_CENTER = (36, 48)
card_back = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/card_jfitz_back.png")    

# initialize some useful global variables
in_play = False
outcome = ""
score = 0

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}


# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
        
# define hand class
class Hand:
    def __init__(self):
        self.cards = []

    def __str__(self):
        ans = "Hand contains "
        for i in range(len(self.cards)):
            ans += str(self.cards[i]) + " " 
        return ans

    def add_card(self, card):
        self.cards.append(card)

    def get_value(self):
        r = [VALUES[card.get_rank()] for card in self.cards]
        r = sum(r)
        if r == 0:
            return r
        if 'A' in [card.get_rank() for card in self.cards] and r + 10<= 21:
            r = r+10
            return r
        else:
            return r
        
   
    def draw(self, canvas, pos):
        for i in range(len(self.cards)):
            pos[0] = (78*i)
            self.cards[i].draw(canvas, pos)
               
# define deck class 
class Deck:
    def __init__(self):
        self.deck = list([])
        for rank in RANKS:
            for suit in SUITS:
                self.deck.append(Card(suit, rank))
        

    def shuffle(self):
        # shuffle the deck 
        random.shuffle(self.deck)


    def deal_card(self):
        return self.deck.pop(random.randrange(len(self.deck)))
        
    
    def __str__(self):
        ans = "Deck contains "
        for card in self.deck:
            ans += str(card) + " " 
        return ans

#define event handlers for buttons
def deal():
    global outcome, in_play, game_deck, dealer_hand, player_hand
    game_deck = Deck()
    dealer_hand = Hand()
    player_hand = Hand()
    
    game_deck.shuffle
    dealer_hand.add_card(game_deck.deal_card())
    dealer_hand.add_card(game_deck.deal_card())
    player_hand.add_card(game_deck.deal_card())
    player_hand.add_card(game_deck.deal_card())
    print "Dealer ", dealer_hand.get_value(), "Player ", player_hand.get_value()
    outcome = 'Hit or Stand?'
    
  
    in_play = True

def hit():
    global in_play, player_hand, score, outcome
 
    # if the hand is in play, hit the player
    if in_play:
        player_hand.add_card(game_deck.deal_card())
        print player_hand.get_value()
    # if busted, assign a message to outcome, update in_play and score
        if player_hand.get_value() > 21:
            outcome = 'You busted! New Game? Hit Deal'
            in_play = False
            score -= 1
            print outcome, score
   
       
def stand():
    global dealer_hand, in_play, player_hand, score, outcome
    if player_hand.get_value() > 21:
        print "You have busted"
    # if hand is in play, repeatedly hit dealer until his hand has value 17 or more
    if in_play:
        while dealer_hand.get_value() <= 17:
            dealer_hand.add_card(game_deck.deal_card())
            print dealer_hand.get_value()
        if dealer_hand.get_value() <= 21:             
    # assign a message to outcome, update in_p.get_value() lay and score
            if dealer_hand.get_value() >= player_hand.get_value():
                outcome = 'Dealer wins! New Game? Hit Deal'
                score -= 1
                print outcome, score
            else:
                outcome = 'Player wins! New Game? Hit Deal'
                score += 1
                print outcome, score
        else:
            outcome = 'Dealer busts. Player wins! New Game? Hit Deal'
            score += 1
            print outcome, score
        
        in_play = True

# draw handler    
def draw(canvas):
    # test to make sure that card.draw works, replace with your code below

    player_hand.draw(canvas, [15, 500])
    dealer_hand.draw(canvas, [15, 100])
    canvas.draw_text(outcome, [270, 50], 20, 'White') 
    canvas.draw_text("Score: " + str(score) , [500, 250], 20, 'White')


# initialization frame

frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)


# get things rolling
deal()
frame.start()




