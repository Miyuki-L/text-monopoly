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

def create_players(n):
    """
    Creates n players of class type Players
    Input: 
            n: int, number of players to create
    Return: 
      players: list, contain n players 
    """
    players = []

    for i in range(n):
        name = input("What is the player name? ")
        players += [Player(name)]
    
    return players


filename = 'board_layout.txt'  # the text file with the name of each block on the board