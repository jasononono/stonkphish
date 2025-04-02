cardValues = {'3': 0, '4': 1, '5': 2, '6': 3, '7': 4, '8': 5, '9': 6, '10': 7, 'J': 8, 'Q': 9, 'K': 10, 'A': 11, '2': 12, 'JOKER': 13}
deck = {i: 4 for i in cardValues.values()}
deck[13] = 2
deductedFromHand = False
previousPlayAmount = 0
previousPlayValue = 0
prevHandAmount = 0
prevNumOppHand = 0
def deductDeck(array, amount = 0):
    global deck
    if amount == -1:
        return
    if amount == 0:
        amount = 1
    elif len(array) == 1:
        burnedCards = []
        if deck[13] != 0:
            if deck[previousPlayValue] < previousPlayAmount:
                 burnedCards = [13]
        else:
            burnedCards = [previousPlayValue] * previousPlayAmount
        for i in burnedCards:
            deck[i] -= 1
    else:
        array = [array[-1]]
    for i in array:
        deck[i] -= amount
def getMove(yourHand, currentPile, currentAmount, numOppHand):  
    global deductedFromHand, previousPlayAmount, previousPlayValue, prevHandAmount, prevNumOppHand, deck
    
    if prevHandAmount < len(yourHand) or prevNumOppHand < numOppHand:
        deductedFromHand = False
        deck = {i: 4 for i in cardValues.values()}
        deck[13] = 2
        previousPlayAmount = 0
        previousPlayValue = 0
    prevHandAmount = len(yourHand)
    prevNumOppHand = numOppHand
    yourHand = sorted([cardValues[i] for i in yourHand])
    pile = sorted([cardValues[i] for i in currentPile])
    if not deductedFromHand:
        deductDeck(yourHand, 0)
        deductedFromHand = True
    deductDeck(pile, currentAmount)
    hand = {}
    for i in yourHand:
        if i in hand.keys():
            hand[i] += 1
        else:
            hand[i] = 1
    playAmount = 0
    playValue = list(hand.keys())[0]
    if currentAmount == -1:
        if numOppHand == 1:
            lowestChore = 99
            for i in hand.keys():
                playAmount = hand[i]
                cardChore = 0
                if  numOppHand >= playAmount > 0:
                    for v in range(i, len(cardValues)):
                        if v == 13:
                            cardChore += deck[v]
                        elif deck[v] >= playAmount:
                            cardChore += deck[v] - playAmount + 1
                if cardChore < lowestChore:
                    lowestChore = cardChore
                    playValue = i
        playAmount = hand[playValue]
    else:
        target = cardValues[currentPile[-1]]
        if target in hand.keys() and currentAmount <= hand[target]:
            playAmount = currentAmount
            playValue = target
        else:
            for i in hand.keys():
                if i > target and (currentAmount == hand[i] or (currentAmount < hand[i] and i > 9) or i == 13):  
                    playAmount = currentAmount
                    if i == 13:
                        playAmount = 1
                    playValue = i
                    break            
    previousPlayAmount = playAmount
    previousPlayValue = playValue
    return playAmount, list(cardValues.keys())[list(cardValues.values()).index(playValue)]
