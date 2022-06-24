def draw_board(board):
    """Draws the board with lines"""
    print(board[0] + "|" + board[1] + "|" + board[2])
    print("-----")
    print(board[3] + "|" + board[4] + "|" + board[5])
    print("-----")
    print(board[6] + "|" + board[7] + "|" + board[8])


def switch_player(current_player):
    """Switches the player from x to o"""
    if current_player == "x":
        return "o"
    else:
        return "x"


def placement(board, current_player):
    """Prompts for input and does input verification"""
    spot = input(current_player + ", Enter a number 0 through 8 for placement: ")
    valid = False
    while not valid:
        try:
            spot = int(spot)
            if 8 >= spot >= 0 and board[spot] == " ":
                valid = True
            else:
                print("Placement not valid")
                spot = input(current_player + ", Enter a number 0 through 8 for placement: ")
        except ValueError:
            print("That is not a number")
            spot = input(current_player + ", Enter a number 0 through 8 for placement: ")

    board[int(spot)] = current_player
    return board


def check_if_won(board):
    """All combinations of winning boards"""
    if board[0] == board[1] == board[2] != " ":
        return True
    if board[3] == board[4] == board[5] != " ":
        return True
    if board[6] == board[7] == board[8] != " ":
        return True
    if board[0] == board[3] == board[6] != " ":
        return True
    if board[1] == board[4] == board[7] != " ":
        return True
    if board[2] == board[5] == board[8] != " ":
        return True
    if board[0] == board[4] == board[8] != " ":
        return True
    if board[2] == board[4] == board[6] != " ":
        return True
    return False


def start_game():
    board = [" "] * 9
    won = False
    current_player = "x"

    while not won:
        board = placement(board, current_player)
        draw_board(board)
        won = check_if_won(board)
        if won:
            print(current_player + ", You win!")
        current_player = switch_player(current_player)

        is_full = False
        for spot in board:
            if spot == " ":
                is_full = True

        if not is_full and not won:
            print("Tie")
            won = True


start_game()
