###############################################################################
#  Algorithm
#  prompts the user to enter a choice
#      if command is 'tf x y': Move card from Tableau column x to Foundation column y.
#      if command is 'tt x y n': Move n cards from Tableau column x to Tableau column y.
#      if command is 'wf x': Move the top card from waste to Foundation column x.
#      if command is 'wt x': Move the top card from waste to Tableau column x.
#      if command is 'sw': Move the top card from stock to waste.
#      if command is  'r': restart the game
#      if command is 'h': display the menu of choices
#      if command is 'q': quit the game
#      setup_game() function creates and initializes the tableau, and
#          foundation, and then returns foundation, tableau, stock, waste.
#      display_game function display the game in sample order.
#      valid_fnd_move and valid_tab_move functions chack whether the two card
#          are valid for move.
#      tableau_to_foundation, tableau_to_tableau, waste_to_foundation,
#          waste_to_tableau and stock_to_waste, those functions move the required
#          cards to different places.
#      is_winner founction shows the game is won.
###############################################################################


import cards        # this is required

YAY_BANNER = """
__   __             __        ___                       _ _ _
\ \ / /_ _ _   _    \ \      / (_)_ __  _ __   ___ _ __| | | |
 \ V / _` | | | |    \ \ /\ / /| | '_ \| '_ \ / _ \ '__| | | |
  | | (_| | |_| |_    \ V  V / | | | | | | | |  __/ |  |_|_|_|
  |_|\__,_|\__, ( )    \_/\_/  |_|_| |_|_| |_|\___|_|  (_|_|_)
           |___/|/

"""

RULES = """
    *------------------------------------------------------*
    *-------------* Thumb and Pouch Solitaire *------------*
    *------------------------------------------------------*
    Foundation: Columns are numbered 1, 2, ..., 4; built
                up by rank and by suit from Ace to King.
                You can't move any card from foundation,
                you can just put in.

    Tableau:    Columns are numbered 1, 2, 3, ..., 7; built
                down by rank only, but cards can't be laid on
                one another if they are from the same suit.
                You can move one or more faced-up cards from
                one tableau to another. An empty spot can be
                filled with any card(s) from any tableau or
                the top card from the waste.

     To win, all cards must be in the Foundation.
"""

MENU = """
Game commands:
    TF x y     Move card from Tableau column x to Foundation y.
    TT x y n   Move pile of length n >= 1 from Tableau column x
                to Tableau column y.
    WF x       Move the top card from the waste to Foundation x
    WT x       Move the top card from the waste to Tableau column x
    SW         Draw one card from Stock to Waste
    R          Restart the game with a re-shuffle.
    H          Display this menu of choices
    Q          Quit the game
"""


def valid_fnd_move(src_card, dest_card):
    """
    judge whether a card is valid for move to foundation
    src_card: the card trying to move
    dest_card: the top card of the column trying to place on
    return True for valid move and False for invalid move
    """
    if src_card.suit() == dest_card.suit(): #make sure the suits are same
        if src_card.rank() - dest_card.rank() == 1: #make sure the difference between two cards is 1
            return True
        else:
            #print error information if not differ by 1
            raise RuntimeError('Error: invalid move due to mismatched cards(the rank must be differ by 1)')
            return False

    else:
        #print error information
        raise RuntimeError('Error: invalid move due to mismatched cards(different suit)')
        return False



def valid_tab_move(src_card, dest_card):
    """
    judge whether a card is valid for move to tableau
    src_card: the card trying to move
    dest_card: the top card of the column trying to place on
    return True for valid move and False for invalid move
    """
    if src_card.suit() != dest_card.suit(): #check the suits are different
        if dest_card.rank() - src_card.rank() == 1: #make sure the difference is 1
            return True
        else:
            #print error information if not differ by 1
            raise RuntimeError('Error: invalid move due to mismatched cards(the rank must be differ by 1)')
            return False
    else:
        #print the error information
        raise RuntimeError('Error: invalid move due to mismatched cards(same suit)')
        return False



def tableau_to_foundation(tab, fnd):
    """
    move a card from tableau to foundation
    tab: the specific column of tableau with the moving card (list)
    fnd: the specific column of foundation trying to place on the card(list)
    """
    if tab != []: #check the tableau has card for move
        card = tab[-1] #assign card with the top card of the tableau
        if len(fnd)!=0 and valid_fnd_move(tab[-1], fnd[-1])==True:
            #check the foundation is not empty and valid for move
            fnd.append(card) #add the card to foundation
            tab.pop() #remove the card from the tableau
            #if the last card in column is 'xx', flip the card
            if len(tab)!=0 and tab[-1].is_face_up() == False:
                tab[-1].flip_card()

        elif len(fnd)==0 and card.rank()==1:
            #check if the foundation is empty and the card is ace
            fnd.append(card) #add the card to the foundation
            tab.pop() #remove the card from the tableau
             #if the last card in column is 'xx', flip the card
            if tab[-1].is_face_up() == False:
                tab[-1].flip_card()
        else: #print error message
            raise RuntimeError('Error: invalid move due to mismatched cards')
    else:
        raise RuntimeError('Error: insufficient number of cards to move')



def tableau_to_tableau(tab1, tab2, n):
    """
    move card(s) from tableau to tableau
    tab1: the specific column of tableau with the moving card(s) (list)
    tab2: the specific column of tableau trying to place on the card(s) (list)
    n: the number of cards want to move in that column (integer)
    """
    if tab1 != [] and tab1[-n].is_face_up() == True:
        #check the beginning tableau is not empty and has enough cards faced up for move
        card = tab1[-n:]
        if len(tab2)==0 or valid_tab_move(tab1[-n],tab2[-1])==True:
            #checke if the aim tableau is empty or valid for move
            tab2.extend(card) #add the card to the aim tableau

            for c in range(n): #remove the card from the previous tableau
                tab1.pop()
             #if the last card in column is 'xx', flip the card
            if len(tab1)!=0 and tab1[-1].is_face_up() == False:
                tab1[-1].flip_card()

        else: #print error message
            raise RuntimeError('Error: invalid move due to mismatched cards')
    else:
        raise RuntimeError('Error: insufficient number of cards to move')



def waste_to_foundation(waste, fnd, stock):
    """
    move a card from waste to foundation
    waste: the list of waste cards (list)
    fnd: the specific column of foundation trying to place on the card(list)
    stock: the list of cards for stock cards (list)
    """
    if waste != []:
        card = waste[-1]
        if len(fnd)!=0 and valid_fnd_move(waste[-1], fnd[-1])==True:
            #check the foundation is not empty and valid for move
            fnd.append(card) #add the card to foundation
            waste.pop() #remove the card from waste

        elif len(fnd)==0 and card.rank()==1:
            #check the foundation is empty and the card is ace
            fnd.append(card) #add the card to foundation
            waste.pop() #remove the card from waste

        else: #print error message
            raise RuntimeError('Error: invalid move due to mismatched cards')
    else:
        raise RuntimeError('Error: insufficient number of cards to move')



def waste_to_tableau(waste, tab, stock):
    """
    move a card from waste to tableau
    waste: the list of waste cards (list)
    tab: the specific column of tableau trying to place on the card (list)
    stock: the list of cards for stock cards (list)
    """
    if waste != []: #waste has card to move
        card = waste[-1] #assign the card
        if (len(tab)==0) or (valid_tab_move(waste[-1], tab[-1])==True):
            #check the tableau is empty or valid for move
            tab.append(card)
            waste.pop()
        else:
            raise RuntimeError('Error: invalid move due to mismatched cards')
    else:
        raise RuntimeError('Error: insufficient number of cards to move')



def stock_to_waste(stock, waste):
    """
    move a card from stock to waste
    stock: the list of cards for stock with the moving card (list)
    waste: the list of waste cards (list)
    """
    if stock != []: #check if the stock has card to move
        waste.append(stock.deal()) #add the card to waste
    else:
        raise RuntimeError('Error: insufficient number of cards to move')



def is_winner(tableau, stock, waste):
    """
    check whether the situation is won
    tableau: the list of 7 cards lists for tableau (list)
    stock: the list of cards for stock (list)
    waste: the list of cards for waste (list)
    return True for valid won and False for not won yet
    """
    if tableau == [[],[],[],[],[],[],[]] and waste == [] and stock == []:
        return True
        #if all cards were added to foundation (no cards everywhere except the foundation),
        #the player won, return True
    else:
        return False



def setup_game():
    """
        The game setup function, it has 4 foundation piles, 7 tableau piles,
        1 stock and 1 waste pile. All of them are currently empty. This
        function populates the tableau and the stock pile from a standard
        card deck.

        7 Tableau: There will be one card in the first pile, two cards in the
        second, three in the third, and so on. The top card in each pile is
        dealt face up, all others are face down. Total 28 cards.

        Stock: All the cards left on the deck (52 - 28 = 24 cards) will go
        into the stock pile.

        Waste: Initially, the top card from the stock will be moved into the
        waste for play. Therefore, the waste will have 1 card and the stock
        will be left with 23 cards at the initial set-up.

        This function will return a tuple: (foundation, tableau, stock, waste)
    """
    # you must use this deck for the entire game.
    # the stock works best as a 'deck' so initialize it as a 'deck'
    stock = cards.Deck()
    stock.shuffle()
    foundation = [[], [], [], []]           # list of 4 lists
    tableau = [[], [], [], [], [], [], []]  # list of 7 lists
    waste = []                              # one list

    for i in range(7): #has 7 tableau lists
        for j in range(i):
            card = stock.deal()
            card.flip_card()
            tableau[i].append(card) #append cards (face down)
        tableau[i].append(stock.deal()) #the top card is face up

    waste.append(stock.deal()) #add cards to waste (face up)

    return foundation, tableau, stock, waste



def display_game(foundation, tableau, stock, waste):
    """
    display the game in correct order
    foundation: the list of 4 cards lists for foundation (list)
    tableau: the list of 7 cards lists for tableau (list)
    stock: the list of cards for stock (list)
    waste: the list of cards for waste (list)
    print the whold game
    """
    print('='*17+' FOUNDATION '+'='*17)
    print('{:7s}{:7s}{:7s}{:7s}'.format('f1','f2','f3','f4'))
    for line in foundation:
        if line==[]:
            print('{:3s}'.format('[  ]'), end='   ') #dispaly empty list in foundation
        else:
            print('{:3s}'.format('['+str(line[-1])+']'), end='    ')
            #display the top card of each list in foundation
    print()
    print('='*18+'  TABLEAU  '+'='*17)
    maxnumber = len(max(tableau, key = len))
    print('{:7s}{:7s}{:7s}{:7s}{:7s}{:7s}{:7s}'.format(' t1',' t2',' t3',' t4',' t5',' t6',' t7'))
    for i in range(1,maxnumber+1): #has 7 lists in tableau
        for line in tableau:
            if len(line)>=i:
                print("%3s    " % (line[i-1]), end = "")
            else:  #add blank to the place with nothing
                print('    ',end = '   ')
        print()
    print('='*16+' STOCK/WASTE '+'='*17)
    print('Stock #('+str(len(stock))+') ==> '+str(waste))
    #display the number of cards in the stock and the waste list



print(RULES)
fnd, tab, stock, waste = setup_game() #assign the variables
display_game(fnd, tab, stock, waste)
print(MENU) #print the rules, game and menu
command = input("prompt :> ") #ask for imput command
while command.strip().lower() != 'q': #if imput is 'q', then stop the game
    try:
        command=command.strip().split() #change the input to list

        if command[0].lower()=='tf': #check different command
            if len(command)==3: #check the number of arguments
                x=int(command[1])-1 #change input column number to list index
                y=int(command[2])-1
                if x<=6 and y<=3: #check valid index for list
                    tableau_to_foundation(tab[x], fnd[y]) #call function to move the card
                else:
                    raise RuntimeError('Error: arguments must be numbers in range') #print error message
            else:
                raise RuntimeError('Error: wrong number of arguments')

        elif command[0].lower()=='tt': #this one is very similar with the previous 'tf' command
            if len(command)==4:
                x=int(command[1])-1
                y=int(command[2])-1
                n=int(command[3])
                if x<=6 and y<=6:
                    tableau_to_tableau(tab[x], tab[y], n)
                else:
                    raise RuntimeError('Error: arguments must be numbers in range')
            else:
                raise RuntimeError('Error: wrong number of arguments')

        elif command[0].lower()=='wf': #this one is very similar with the previous 'tf' command
            if len(command)==2:
                x=int(command[1])-1
                if x<=3:
                    waste_to_foundation(waste, fnd[x], stock)
                else:
                    raise RuntimeError('Error: arguments must be numbers in range')
            else:
                raise RuntimeError('Error: wrong number of arguments')

        elif command[0].lower()=='wt': #this one is very similar with the previous 'tf' command
            if  len(command)==2:
                x=int(command[1])-1
                if x<=6:
                    waste_to_tableau(waste, tab[x], stock)
                else:
                    raise RuntimeError('Error: arguments must be numbers in range')
            else:
                raise RuntimeError('Error: wrong number of arguments')

        elif command[0].lower()=='sw':
            if len(command)==1:
                stock_to_waste(stock, waste) #call function to move card from stock to waste
            else:
                raise RuntimeError('Error: wrong number of arguments')
        elif len(command)==1 and command[0].lower()=='r':
            fnd, tab, stock, waste = setup_game() #restart the game (re-assign the variable)
        elif len(command)==1 and command[0].lower()=='h':
            print(MENU) #print the menu
        else: #print error message
            raise RuntimeError('Error: Invalid Command')

    except RuntimeError as error_message:  # any RuntimeError you raise lands here
        print("{:s}\nTry again.".format(str(error_message)))
        command = input("prompt :> ") #ask re-command if the imput is incorrect
        continue
    display_game(fnd, tab, stock, waste) #display the results after command
    if is_winner(tab, stock, waste)==True: #check whether the game is win
        print(YAY_BANNER)
        break
    else:
        command = input("prompt :> ") #continue if not win
        continue
