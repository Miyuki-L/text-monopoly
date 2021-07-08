import random
import json
from time import sleep

layout = 'board_layout.txt'  # the text file with the name of each block on the board
description = "properties_tax.json" # file containing information aobut land, utilities, tax

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
        print(self.name, "going to jail\n")
        
        self.dbl_roll = 0      
        self.jail = True
        self.position = 10  

    def move(self, d1, d2):
        """
        updates player position and checks if player's position needs to be 
        reset because they have reached the end of the board index 39.
        d1, d2: dice roll outputs
        """
        self.position += d1 + d2

        if self.position >= 40:
            self.position -= 40
   
    def print_position(self,board):
        """
        Prints the block that landed on or is currently at 
        Input: board: the game board
        """

        if self.jail:                 # Player is in jail right now
            print(self.name, 'is currently in Jail\n')
        else:
            print(self.name, 'landed on', board[self.position])

    def player_turn(self, board):
        """
        Moves the player for their turn.
        Input: board: the game board
        """
        d1, d2 = self.dice_roll()
        print(self.name, 'rolled:', d1, d2)
        
        if self.jail:                           # In jail
            if self.jail_roll == 3 or d1 == d2: # rolled dbl or in jail for 3 rounds
                self.jail = False               # Update information
                self.jail_roll = 0

                self.move(d1, d2)               

                self.print_position(board) 
                       
            else:
                self.jail_roll += 1             # Update information

                self.print_position(board)

        else:
            while d1 == d2:                     # rolled double
                self.move(d1, d2)               # update information
                self.dbl_roll += 1

                self.print_position(board)

                if self.dbl_roll == 3:          # Go to jail for 3 consecutive dbls
                    print('Rolled 3 consecutive doubles\n')
                    self.go_to_jail()

                elif self.position == 30:       # Landed on go to jail
                    self.go_to_jail()

                else:                           # roll again
                    d1, d2 = self.dice_roll()
                    print(self.name, 'rolled:', d1, d2)
            
            self.move(d1, d2)           # update information
            self.dbl_roll = 0

            self.print_position(board)

            if self.position == 30:        # landed on go to jail
                self.go_to_jail()
                



def read_json(filename):
    """
    Takes in filename of json file that has the properties description 
    for the monopoly and reads in the json
    
    return: property_dict, dict
    """
    with open(filename) as f:
        property_dict = json.load(f)

    return property_dict

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
        board += [line[:-1]]         # get rid of \n at end of the line
    
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
            print()
        except ValueError:              #checks if an int was inputted
            print("Sorry, please try again")
            continue
        else:
            break

    players = []

    for i in range(n):
        name = input("What is the player name? ")
        print()
        players += [Player(name)]
    
    return players

def game(filename=layout):
    """
    Runs the Monopoly game
    Input:
      filename: .txt file, the file the contains the layout of the board
                    default set to file included (board_layout.txt)
    """
    board = create_board(filename)                  # setup
    players = create_players()

    p_index = 0
    while True:
        current_p = players[p_index]
        current_p.player_turn(board)
        sleep(1)

        p_index += 1                                # next player
        if p_index == len(players):                 # reset p_index
            p_index = 0 

    
