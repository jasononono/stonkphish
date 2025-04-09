'''
------------------------------------------------------
STONKPHISH V2i
------------------------------------------------------

An experimental version of Stonkphish V2. (spoiler: it didnt work)

------------------------------------------------------
'''


cardValues = {'3': 0, '4': 1, '5': 2, '6': 3, '7': 4, '8': 5, '9': 6,
                     '10': 7, 'J': 8, 'Q': 9, 'K': 10, 'A': 11, '2': 12, 'JOKER': 13}

deck = {i: 4 for i in cardValues.values()}
deck[13] = 2
deductedFromHand = False
previousPlayAmount = 0

BREAKPOINT = 0.9
refBreak = 0.5

def deductDeck(array, amount=0, prevAmount=0):
    global deck
    if amount != 0:
        if len(array) == 0:
            return
        elif len(array) != amount:
            array = array[-amount:]
        else:
            #figure out how the opponent started the new round (burn) (stockphish3: burned w/ joker or same card)
            if prevAmount == 0:
                pass
            #if the round is burned by the opponent, include the burning card in the deduction. (future work)

    for i in array:
        deck[i] -= 1


def chore(card, amount): # CHance Of REfutation
    total = 0
    for i in range(card, len(cardValues)):
        if i == 13:
            total += deck[i]
            continue
        if deck[i] >= amount:
            total += deck[i] - (amount * refBreak) + 1
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

    splitHand = {i + 1: [] for i in range(4)} # key value combination: [amount: value]
    for i in hand.keys():
        if i != 13:
            splitHand[hand[i]].append(i)

    playAmount = 0
    playValue = list(hand.keys())[0]
    
    if currentAmount == -1:
        
        highestChoreAvg = 0
        for a in range(1, 5):
            if len(splitHand[a]) == 0:
                continue
            choreAvg = 0
            for i in splitHand[a]:
                choreAvg += chore(i, a)
            choreAvg = abs(choreAvg / len(splitHand[a]) / 54 - BREAKPOINT)
            if choreAvg > highestChoreAvg:
                highestChoreAvg = choreAvg
                playAmount = a
        if playAmount == 0:
            playAmount = 1
            playValue = 13

        playValue = translatePlayValue(splitHand[playAmount][0])
        
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
            elif (hand[i] == currentAmount and target < i) or i == 13:
                playAmount = currentAmount
                playValue = translatePlayValue(i)
                break
    
    previousPlayAmount = playAmount
    return playAmount, playValue


print(getMove(['3', '3', '4', '4', '5', '5', '6', 'K', 'A', 'A', 'JOKER'], [], -1, 5))
