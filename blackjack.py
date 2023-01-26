
import random

cards = [11, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10 ,10, 10]
user_cards = []
dealer_cards = []
# user_sum = 0
# dealer_sum = 0
sum = 0


def draw_random_card() :
    x =random.choice(cards)
    return x 
# draw_random_card(user_cards)
# draw_random_card(user_cards)
# draw_random_card(dealer_cards)
# dealer_cards.append("_")
# print (user_cards)
# print(dealer_cards)
# dealer_cards[1] = random.choice(cards)
#print(dealer_cards)
user_cards.append(draw_random_card())
user_cards.append(draw_random_card())
dealer_cards.append(draw_random_card())
dealer_cards.append(draw_random_card())

def calculate_score(list) :
    sum = 
    if sum == 21 :
        return 0
    elif sum > 21 :
        for i in list :
            if i == 11 :
                list[i] = 1
                return list
            else :
                return "Game over"
calculate_score(user_cards)
                


