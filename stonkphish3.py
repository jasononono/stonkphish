# INITIALIZE
cardValues = {'3': 0, '4': 1, '5': 2, '6': 3, '7': 4, '8': 5, '9': 6,
                     '10': 7, 'J': 8, 'Q': 9, 'K': 10, 'A': 11, '2': 12, 'JOKER': 13}

deck = {i: 4 for i in cardValues.values()}
deck[13] = 2
deductedFromHand = False
previousPlayAmount = 0
previousPlayValue = 0


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
    if amount == 0 or len(array) == 0:
        return
    if len(array) == amount:
        array.extend(burnedCard())
    else:
        array = array[-amount:]

    for i in array:
        deck[i] -= amount


def chore(card, amount): # CHance Of REfutation
    if amount <= 0:
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
    global deductedFromHand, previousPlayAmount, previousPlayValue

    yourHand = sorted([cardValues[i] for i in yourHand])
    pile = sorted([cardValues[i] for i in currentPile])

    if not deductedFromHand:
        deductDeck(yourHand)
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
    
    if currentAmount == -1 or currentAmount == 0:
        highestChore = -1
        for i in hand.keys():
            playAmount = hand[i]
            cardChore = chore(i, playAmount)
            if cardChore > highestChore:
                highestChore = cardChore
                playValue = i
        playAmount = hand[playValue]
        
    else:
        target = cardValues[currentPile[-1]]

        if target in hand.keys() and currentAmount <= hand[target] and chore(target, hand[target] - currentAmount) < 15:
            playAmount = currentAmount
            playValue = target
        else:
            for i in hand.keys():
                if i == 13:
                    playAmount = 1
                    playValue = 13
                    break
                if i > target and (currentAmount == hand[i] or (currentAmount < hand[i] and i > 9)):    
                    playAmount = currentAmount
                    playValue = i
                    break
        
    previousPlayAmount = playAmount
    previousPlayValue = playValue
    return playAmount, translatePlayValue(playValue)
