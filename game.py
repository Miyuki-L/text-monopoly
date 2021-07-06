import random
layout = 'board_layout.txt'  # the text file with the name of each block on the board

class Player:
    """ A data type representing a monopoly player
        with name, position, money, and other relavant 
        information
    """
    def __init__(self, name):
        """Construct object of type Player with the given name
        Attributes: dbl_roll: keeps count of consecutive doubles
                        jail: True/False in Jail
                   jail_roll: Number of rolls rolled in jail
                  properties: The properties they own"""
        self.name = name
        self.position = 0
        self.money = 1500
        self.dbl_roll = 0
        self.jail = False
        self.jail_roll = 0
        self.properties = []

    def dice_roll(self):
        """
        Rolls dice and returns the value of the two dices 
        Return: d1, d2
        """
        d1 = random.choice(range(1,7))
        d2 = random.choice(range(1,7))
        return d1,d2

    def go_to_jail(self):
        """
        Updates players information when they are sent to jail
        """
        self.dbl_roll = 0      
        self.jail = True
        self.position = 10  




           

def create_board(filename):
    """
    Takes in a filename that leads to a file that contains what each 
    block does on a new line for every block.

    Input: filename: txt file containing what each block does
    Output: list, the gameboard
    """
    f = open(filename, 'r')         # read file
    lines = f.readlines()

    board = []
    for line in lines:
        board += [line]
    
    return board

def create_players():
    """
    Prompts user for input of number of players to create and creates players

    Return: 
      players: list, contain n players 
    """
    while True:
        try:
            n = int(input("PLease enter the number of players: "))
        except ValueError:              #checks if an int was inputted
            print("Sorry, please try again")
            continue
        else:
            break

    players = []

    for i in range(n):
        name = input("What is the player name? ")
        players += [Player(name)]
    
    return players

def game(filename=layout):
    """
    Runs the Monopoly game
    Input:
      filename: .txt file, the file the contains the layout of the board
                    default set to file included (board_layout.txt)
    """
    board = create_board(filename)
    
