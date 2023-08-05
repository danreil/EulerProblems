# Euler problem 22: Finding number of wins for player 1 in file euler22.txt
# NOTE: This is actually euler 54.
from pathlib import Path
from enum import IntEnum

import numpy as np

filename = 'euler22.txt'
file_directory = Path.cwd().joinpath('data')
file = file_directory.joinpath(filename)

num_cards = 5
hands = np.loadtxt(file, dtype=str, delimiter=' ')
player1, player2 = hands[:,0:num_cards], hands[:,num_cards:]

# Make a structure for comparing poker hand strength to determine winner
poker_hands = ['High Card', 'One Pair', 'Two Pair', 'Three of a Kind',
               'Straight', 'Flush', 'Full House', 'Four of a Kind',
               'Straight Flush']
hand_order = IntEnum('HandsOrderEnum', poker_hands) 


def convert_hand(hand_str):
    """
    Convert the hand from the array of strings representation to a record array of card rank and suit
    :param
    hand_str:array of strings for that players hand
    :return:
    """
    ranks = []
    suits = []
    for card in hand_str:
        match card[0]:
            case 'T':
                ranks.append(10)
            case 'J':
                ranks.append(11)
            case 'Q':
                ranks.append(12)
            case 'K':
                ranks.append(13)
            case 'A':
                ranks.append(14)
            case _:
                ranks.append(int(card[0]))

        suits.append(card[1])

    hand_record = np.core.records.fromarrays([ranks, suits], names='ranks, suits')

    hand_record_sort = np.sort(hand_record, order = 'ranks')
    return hand_record_sort

def detect_best_hand(hand_array):
    """
    Detect the type of hand that the input 5 cards has from the deal (ie, pair, flush, etc.)
    :param hand_array: output of convert_hand. A numpy record array
    :return: TBD
    """
    pass

def detect_pairs(hand_array):
    # Detect any of the types of pairs in the hand (1 pair, 2 pair, 3 of kind, 4 of a kind)
    ranks = hand_array.ranks
    count_ranks = {}
    for rank in ranks:
        if rank in count_ranks:
            count_ranks[rank] += 1
        else:
            count_ranks[rank] = 1
    
    if max(count_ranks.values()) == 4:
        result_hand = hand_order['Four of a Kind']
    elif (max(count_ranks.values()) == 3) and (2 in count_ranks.values()):
        result_hand = hand_order['Full House']
    elif (max(count_ranks.values()) == 3) and (len(count_ranks.values()) == 3):
        result_hand = hand_order['Three of a Kind']
    elif (max(count_ranks.values()) == 2) and (len(count_ranks.values()) == 3):
        result_hand = hand_order['Two Pair']
    elif (max(count_ranks.values()) == 2) and (len(count_ranks.values()) == 4):
        result_hand = hand_order['One Pair']
    else:
        result_hand = hand_order['High Card']
    
    return result_hand.name        
        


def detect_straight(hand_array):
    # As an example, might change. But try detecting a straight, and return highest number in straight
    ranks = hand_array.ranks
    result = True
    for i in range(num_cards-1):
        if ranks[i] != ranks[i+1] - 1:
            result = False
    # Note, haven't implemented the option of ace being low. Not sure if it should or not
    return result, ranks[num_cards-1]

#def detect_flush    


# hand_test = player2[14]
# print(hand_test)
# convert_hand_test = convert_hand(hand_test)
# print(convert_hand_test.ranks)
# print(convert_hand_test.suits)
# is_straight, high_card = detect_straight(convert_hand_test)
# print(convert_hand_test)

hand_test_manual = np.array(['4H','4J','7H','5H','5H'])
convert_hand_test_manual = convert_hand(hand_test_manual)
# is_straight, high_card = detect_straight(convert_hand_test_manual)
result_hand = detect_pairs(convert_hand_test_manual)
print(result_hand)