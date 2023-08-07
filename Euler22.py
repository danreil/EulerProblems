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
    
    return result_hand         


def detect_straight(hand_array):
    """ Check whether hand_array has a straight. If so, return true."""
    ranks = hand_array.ranks
    result = True
    for i in range(num_cards-1):
        if ranks[i] != ranks[i+1] - 1:
            result = False
    # Note, haven't implemented the option of ace being low. Not sure if it should or not
    return result

def detect_flush(hand_array):
    """ Check whether hand_array has a Flush. If so, return true."""
    suits = hand_array.suits
    result = False
    if len(np.unique(suits)) == 1:
        result = True
    
    return result   

def find_hand_value(hand_array):
    """ Call all of the detect_XX functions to find the value of a player's hand"""
    value_pair = detect_pairs(hand_array) # this func directly returns the hand value
    value_nonpair = 0
    is_straight = detect_straight(hand_array)
    is_flush = detect_flush(hand_array)
    is_straight_flush = is_straight and is_flush
    if is_straight:
        value_nonpair = hand_order['Straight']
    if is_flush:
        value_nonpair = hand_order['Flush']
    if is_straight_flush:
        value_nonpair = hand_order['Straight Flush']
    
    # The greater of value_nonpair and value_pair is the hand_value
    value = max(value_pair, value_nonpair)

    return value
"""
def compare_tie(player1_hand, player2_hand, player1_value):
    """ In case of tie, follow this complicated logic to resolve it"""
    if player1_value == 1: # High Card
        if hand1_arr.ranks > hand2_arr.ranks:
            player_result = [1, 0]
        else:
            player_result = [0, 1]
        
    return player_result
"""

def detect_best_hand(player1_hand, player2_hand):
    """
    Find out the best hand type for each player, and find out which is best
    Input: Hand arrays (converted, as returned from convert hand) for player 1 and 2
    Return: A numpy array of [1,0] if player 1 wins, or [0,1] if player 2 wins 
    """
    player1_value = find_hand_value(player1_hand)
    player2_value = find_hand_value(player2_hand)
    
    if player1_value > player2_value:
        player_result = [1, 0]
    elif player2_value > player1_value:
        player_result = [0, 1]
    else:
        player_result = compare_tie(player1_hand, player2_hand, player1_value)
    
    return player_result

def card_strength_calc(hand_array):
    """ New Idea, assign values to card ranks, such that it correctly compares
    high cards all the way down (like, 14^5+14^3...)"""

hand1 = np.array(['10H','6C', '5H', '4S', '3D'])
hand2 = np.array(['JH','7C', '6S', '5S', '4D'])
hand1_arr, hand2_arr = convert_hand(hand1), convert_hand(hand2)

best_hand = detect_best_hand(hand1_arr, hand2_arr)
