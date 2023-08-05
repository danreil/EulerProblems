# Euler problem 22: Finding number of wins for player 1 in file euler22.txt
# NOTE: This is actually euler 54.
from pathlib import Path


import numpy as np

filename = 'euler22.txt'
file_directory = Path.cwd().joinpath('data')
file = file_directory.joinpath(filename)

num_cards = 5
hands = np.loadtxt(file, dtype=str, delimiter=' ')
player1, player2 = hands[:,0:num_cards], hands[:,num_cards:]

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
    def detect_straight(hand_array):
        # As an example, might change. But try detecting a straight, and return highest number in straight
        ranks = hand_array.ranks
        for i in range(num_cards):




hand_test = player1[6]
convert_hand_test = convert_hand(hand_test)
print(convert_hand_test)
