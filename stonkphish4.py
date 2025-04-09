'''
------------------------------------------------------
STONKPHISH V4
------------------------------------------------------

A Stonkphish version that fixed a lot of issues from previous versions.

------------------------------------------------------
'''

# INITIALIZE
cardValues = {'3': 0, '4': 1, '5': 2, '6': 3, '7': 4, '8': 5, '9': 6,
                     '10': 7, 'J': 8, 'Q': 9, 'K': 10, 'A': 11, '2': 12, 'JOKER': 13}

deck = {i: 4 for i in cardValues.values()}
deck[13] = 2
deductedFromHand = False
previousPlayAmount = 0
previousPlayValue = 0
prevHandAmount = 0
prevNumOppHand = 0

BREAKPOINT1 = 30
BREAKPOINT2 = 9


def burnedCard():
    card = []
    if deck[13] != 0:
        if deck[previousPlayValue] < previousPlayAmount:
             card = [13]
    else:
        card = [previousPlayValue] * previousPlayAmount
    return card


def deductDeck(array, amount = 0):
    global deck
    if len(array) == 0 or amount == -1: # stonkphish starts round, empty pile
        return
    if amount == 0: # deducting own hand
        amount = 1
    elif len(array) == 1: # opponent burned pile
        for i in burnedCard():
            deck[i] -= 1
    else: # round is ongoing
        array = [array[-1]]

    for i in array:
        deck[i] -= amount

    #print(deck)


def chore(card, amount, numOppHand): # CHance Of REfutation
    if amount <= 0 or amount > numOppHand:
        return 0
    total = 0
    for i in range(card, len(cardValues)):
        if i == 13:
            total += deck[i]
            continue
        if deck[i] >= amount:
            total += deck[i] - amount + 1
    return total


def translatePlayValue(value): 
    return list(cardValues.keys())[list(cardValues.values()).index(value)]


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

    #print(yourHand)

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
                cardChore = chore(i, playAmount, numOppHand)
                if cardChore < lowestChore:
                    lowestChore = cardChore
                    playValue = i

        playAmount = hand[playValue]

        
    else:
        target = cardValues[currentPile[-1]]

        if target in hand.keys() and currentAmount <= hand[target] and (
            chore(target, hand[target] - currentAmount, numOppHand) < BREAKPOINT1): #####
            playAmount = currentAmount
            playValue = target
        else:
            for i in hand.keys():
                if i == 13:
                    playAmount = 1
                    playValue = 13
                    break
                if i > target and (currentAmount == hand[i] or
                                   (currentAmount < hand[i] and i > BREAKPOINT2)): #####    
                    playAmount = currentAmount
                    playValue = i
                    break
        
    previousPlayAmount = playAmount
    previousPlayValue = playValue
    return playAmount, translatePlayValue(playValue)
