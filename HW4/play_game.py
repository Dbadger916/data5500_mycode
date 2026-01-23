'''
This is an example of how to create a DeckOfCards object, shuffle it, and deal cards to play a game
'''

from DeckOfCards import *

#welcome user
print("Welcome to BlackJack!")
deck = DeckOfCards()

#defining score check for if you bust
def scoreCheck(score):
    if score > 21:
        print("You busted! You lose!")
        return True
    else:
        return False

#defining score compare to compare your score to the dealers and output all other possible endings besides you busting
def scoreCompare(score, dealerscore):
    if dealerscore > 21:
        print("Dealer busted, you win!")
        return
    elif score > dealerscore:
        print("Your score is higher. You win!")
        return
    elif score < dealerscore:
        print("Dealer's score is higher. You lose!")
        return
    else:
        print("Scores tied! No winner!")
        return


#game function, that can be run again and again to allow the user to keep playing
def main():
    j = 3
    print("Deck before being shuffled:")
    deck.print_deck()
    deck.shuffle_deck()
    print("Deck after being shuffled:")
    deck.print_deck()




    # deal two cards to the user
    card = deck.get_card()
    card2 = deck.get_card()

    #deal two cards to the dealer
    dealercard = deck.get_card()
    dealercard2 =  deck.get_card()


    score = 0
    dealerscore=0
    # calculate the user's hand score
    print("Card number 1 is: ", card)
    print("Card number 2 is: ", card2)
    score += card.val
    score += card2.val
    print("Your score is: ", score)


    # ask user if they would like a "hit" (another card), and allow them to hit multiple times. end if they bust.
    def hitting():
        nonlocal score
        nonlocal dealerscore
        nonlocal j
        hit = input("would you like a hit? y/n: ")
        if hit == 'y':
            card3 = deck.get_card()
            print("Card number", j, " is", card3)
            j+=1
            score += card3.val
            if card3.val == 11 and score > 21:
                score -= 10
            print("new score: ", score)
            if scoreCheck(score) == True:
                return
            else:
                hitting()

#define the dealers hand, for when you stop hitting and haven't busted/ 
        else:
            print("Dealer card number 1 is: ", dealercard)
            print("Dealer number 2 is: ", dealercard2)
            dealerscore += dealercard.val
            dealerscore += dealercard2.val
            i = 3
            while dealerscore <= 16:
                dealercard3 = deck.get_card()
                print("Dealer card number", i, " is", dealercard3)
                dealerscore += dealercard3.val
                i+=1
                if dealercard3.val == 11 and dealerscore > 21:
                    dealerscore -= 10
            print("Dealer score is: ", dealerscore)
            scoreCompare(score, dealerscore)

    #call hitting, ask if user would like to play again.
    hitting()
    again = input("Would you like to play again? y/n: ")
    if again == "y":
        main()
    else:
        print("Thank you for playing!")
    
        

main()

    


