# INITIALIZE
cardValues = {'3': 0, '4': 1, '5': 2, '6': 3, '7': 4, '8': 5, '9': 6,
                     '10': 7, 'J': 8, 'Q': 9, 'K': 10, 'A': 11, '2': 12, 'JOKER': 13}

deck = {i: 4 for i in cardValues.values()}
deck[13] = 2
deductedFromHand = False
previousPlayAmount = 0


def deductDeck(array, amount = 0, prevAmount = 0):
    global deck
    if amount == 0 or len(array) == 0:
        return
    if len(array) != amount:
        array = array[-amount:]

    for i in array:
        deck[i] -= amount


def chore(card, amount): # CHance Of REfutation
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
    global deductedFromHand, previousPile, previousPlayAmount

    yourHand = sorted([cardValues[i] for i in yourHand])
    pile = sorted([cardValues[i] for i in currentPile])

    if not deductedFromHand:
        deductDeck(yourHand)
        deductedFromHand = True
    deductDeck(pile, currentAmount, previousPlayAmount)

    hand = {}
    for i in yourHand:
        if i in hand.keys():
            hand[i] += 1
        else:
            hand[i] = 1

    playAmount = 0
    playValue = list(hand.keys())[0]
    
    if currentAmount == -1:
        highestChore = -1
        for i in hand.keys():
            playAmount = hand[i]
            cardChore = chore(i, playAmount)
            if cardChore > highestChore:
                highestChore = cardChore
                playValue = i
        playAmount = hand[playValue]
        playValue = translatePlayValue(playValue)
        
    else:
        target = cardValues[currentPile[-1]]
        if target in hand.keys() and currentAmount <= hand[target]:
            playAmount = currentAmount
            playValue = translatePlayValue(target)
            
            previousPlayAmount = playAmount
            return playAmount, playValue
                
        for i in hand.keys():
            if i == 13:
                playAmount = 1
                playValue = 'JOKER'
                break
            elif (hand[i] == currentAmount and target < i):
                playAmount = currentAmount
                playValue = translatePlayValue(i)
                break
    
    previousPlayAmount = playAmount
    return playAmount, playValue