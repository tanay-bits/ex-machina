import mytictactoe


# Print out the state of the board.  
# 0 indicates an empty cell
# 1 indicates an X 
# -1 indicates a 0

def print_board(board):

    for i in range(3):
        print " ",
        for j in range(3):
            if board[i*3+j] == 1:
                print 'X',
            elif board[i*3+j] == -1:
                print 'O',  
            elif board[i*3+j] == 0:
                print " ",         
            if j != 2:
                print " | ",
        print
        
        if i != 2:
            print "-----------------"
        else: 
            print 

# Print out some simple instructions as to how to refer to the cells in the board
            
def print_instructions():
    print "\nThe board is laid out as folows:\n"
    print "  1  |  2  |  3"
    print "-----------------"
    print "  4  |  5  |  6"
    print "-----------------"
    print "  7  |  8  |  9"
    print "\nWhen you play, input a board position.\n"


def select_starter():
    print "\n\nWeclome to Tic Tac Toe"
    print "Would you like to be the 'X' or the 'O'?"
 
    valid_user = False
    
    while not valid_user:
        valid_user = raw_input("Type X or O: ")
        if not valid_user in ["X","O"]:
            valid_user = False
    print "Great.  You are " + valid_user
    if valid_user == "X":
        print "You will go first!\n"
    else:
        print "The machine will go first!\n"
        
    print "Good luck!"
    return valid_user


def get_move(board, turn, user):
    if turn == user:
        return get_input(board,turn)
    else: 
        return machine_move(board,turn) 
 
            
def machine_move(board, my_symbol):
    valid_move = False
    while not valid_move:    
        response = mytictactoe.mymove(board,my_symbol)
        if response in [1,2,3,4,5,6,7,8,9]:
            move = response - 1
            if board[move] == 0:
                return move
            else:
                print "That position has already been taken.\n"
        else:
            print "That is not a valid move! Please try again.\n"         

    
def get_input(board,turn):
    valid = False
    while not valid:
        response = raw_input("Where would you like to make your move (You are " + turn + ")? Pick 1-9? ")
        if response in ["1","2","3","4","5","6","7","8","9"]:
            move = int(response) - 1
            if board[move] == 0:
                return move
            else:
                print "That position has already been taken.\n"
        else:
            print "That is not a valid move! Please try again.\n" 

        
def check_win(board):
    threes = ((1,2,3),(4,5,6),(7,8,9),(1,4,7),(2,5,8),(3,6,9),(1,5,9),(3,5,7))
    for each in threes:
        total = board[each[0]-1] + board[each[1]-1] + board[each[2]-1]
        if total == -3:
            return "O"
        elif total == 3:
            return "X"
    return "No Winner"

def main():
    
    # Start Game
    # Change turns
    # Checks for winner
    # Quits and redo board

    board = [0,0,0,0,0,0,0,0,0]
        
    user_symbol = select_starter()
    
    print_instructions()
      
    win = False
    move = 0
    while not win:

        # Print board
        
        move = move + 1    
        print "\nThe state of the game is as follows:"
        print_board(board)
        if move % 2 == 1:
            turn = 'X'
            target = 1
        else:
            turn = 'O'
            target = -1

        # Get input from player or machine and update board

        turn_value = get_move(board, turn, user_symbol)
        board[turn_value] = target

        # Continue move and check if end of game
        
        print "\nChecking for winner"
        winner = check_win(board)
        if winner != "No Winner":
            print "The winner is " + winner +"\n"
            print_board(board)
            quit()
        elif move >= 9:
            print "The game is a draw.\n"
            print_board(board)
            quit()
        print "No winner yet"

if __name__ == "__main__":
    main()
    
