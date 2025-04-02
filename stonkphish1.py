cardValues = {'3': 0, '4': 1, '5': 2, '6': 3, '7': 4, '8': 5, '9': 6,
                     '10': 7, 'J': 8, 'Q': 9, 'K': 10, 'A': 11, '2': 12, 'JOKER': 13}

def translatePlayValue(value):
    return list(cardValues.keys())[list(cardValues.values()).index(value)]

def getMove(yourHand, currentPile, currentAmount, numOppHand):

    # sort hand
    yourHand = sorted([cardValues[i] for i in yourHand])
    hand = {}
    for i in yourHand:
        if i in hand.keys():
            hand[i] += 1
        else:
            hand[i] = 1

    playAmount = 0
    playValue = list(hand.keys())[0]
    if currentAmount == -1:
        for i in hand.keys():
            playAmount = hand[i]
            if list(hand.values()).count(playAmount) == 1 and 13 not in hand.keys() and playAmount != 4:
                continue
            playValue = translatePlayValue(i)
            return playAmount, playValue
        return list(hand.values())[0], translatePlayValue(playValue)
        
    else:
        target = cardValues[currentPile[-1]]
        if target in hand.keys() and currentAmount <= hand[target]:
            playAmount = currentAmount
            playValue = translatePlayValue(target)
            return playAmount, playValue
                
        for i in hand.keys():
            if i == 13:
                playAmount = 1
                playValue = 'JOKER'
                break
            elif (hand[i] == currentAmount and target < i) or i == 13:
                playAmount = currentAmount
                playValue = translatePlayValue(i)
                break

    return playAmount, playValue