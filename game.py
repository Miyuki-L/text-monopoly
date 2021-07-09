import random
import json
from time import sleep

layout = 'board_layout.txt'  # the text file with the name of each block on the board
description = "properties_tax.json" # file containing information aobut land, utilities, tax

class Land:
    """
    Data Type representing Land in monopoly (those where the player could build
    houses). Contains the information of price, upgradeCost, colorset, rent and
    other relavant information
    """

    def __init__(self, name, description):
        """
        Construct object of type Class with the given name and description
        uses the description to get the information about price, rent, ...
        Attributes: 
        """
        self.name = name
        self.location = description['location']
        self.price = description['price']
        self.upgradeCost = description['upgradeCost']
        self.rent = description['rent']
        self.mortgage = description['mortgage']
        self.colorSet = description['colorSet']
        self.houses = 0
        self.owner = ''             #no one owns this property yet

    def cal_rent(self):
        """
        Calculates the Rent that a player needs to pay for this property
        if they land on it.

        return int, amount of rent to pay
        """

        houses = self.houses
        rent = self.rent[str(houses)]
        return rent


class Railroad:
    """
    Data Type representing Railroad in monopoly (Electric company/Water works). 
    Contains the information of price, rent and
    other relavant information
    """

    def __init__(self, name, description):
        """
        Construct object of type Class with the given name and description
        uses the description to get the information about price, rent, ...
        Attributes: 
        """
        self.name = name
        self.location = description['location']
        self.price = description['price']
        self.rent = description['rent']
        self.mortgage = description['mortgage']
        self.owner = ''             #Class Player

    def cal_rent(self):
        """
        Calculates the Rent that a player needs to pay for this property
        if they land on it.

        return int, amount of rent to pay
        """
        owner = self.owner
        num_owned = len(owner.railroad)
        rent = self.rent[str(num_owned)]
        return rent


class Utilities:
    """
    Data Type representing Utilities in monopoly (Electric company/Water works). 
    Contains the information of price, rent and
    other relavant information
    """

    def __init__(self, name, description):
        """
        Construct object of type Class with the given name and description
        uses the description to get the information about price, rent, ...
        Attributes: 
        """
        self.name = name
        self.location = description['location']
        self.price = description['price']
        self.rent = description['rent']
        self.mortgage = description['mortgage']
        self.owner = ''             #no one owns this property yet

    def cal_rent(self):
        """
        Finds the amount to times the dice roll by when a player lands on
        this property

        return int, amount to multiply by
        """
        owner = self.owner
        num_owned = len(owner.utilities)
        rent = self.rent[str(num_owned)]
        return rent


class Taxes:
    """
    Data Type representing Taxes in monopoly (Income/Luxury Tax). 
    Contains the information of price and
    other relavant information
    """

    def __init__(self, name, description):
        """
        Construct object of type Class with the given name and description
        uses the description to get the information about price, ...
        Attributes: 
        """
        self.name = name
        self.location = description['location']
        self.price = description['price']

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

        self.land = []
        self.railroad = []
        self.utilities = []

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
        block = board[self.position]

        if self.jail:                 # Player is in jail right now
            print(self.name, 'is currently in Jail\n')
        elif type(block) != str:      # landed on properties
            print(self.name, 'landed on', block.name,"\n")
        else:
            print(self.name, 'landed on', board[self.position],"\n")

    def post_jail(self):
        """
        Moves the player when they leave the jail
        This is a separate function because rules are slightly different
            (Players do not get to roll again when they rolled a double)
        """
        self.jail = False               # Update information
        self.jail_roll = 0

        print(self.name, 'leaving jail \n')

        d1, d2 = self.dice_roll()       # roll again (this time for moving)
        print(self.name, 'rolled:', d1, d2)

        self.move(d1, d2)               

    def player_turn(self, board):
        """
        Moves the player for their turn.
        Input: board: the game board
        """
        d1, d2 = self.dice_roll()
        print(self.name, 'rolled:', d1, d2)
        
        if self.jail:                           # In jail
            if self.jail_roll == 3:             # in jail for 3 rounds
                print(self.name, 'end of third turn in jail')

                self.post_jail()                             
                self.print_position(board) 

            elif d1 == d2:                      # rolled a double
                print(self.name, 'rolled a double while in jail')

                self.post_jail()
                self.print_position(board)
                       
            else:
                self.jail_roll += 1             # Update information

                self.print_position(board)

        else:
            while d1 == d2:                     # rolled double
                self.move(d1, d2)               # update information
                self.dbl_roll += 1
                
                self.check_block(board[self.position])  # Looks at the checks if they could buy or have to pay

                self.print_position(board)

                if self.dbl_roll == 3:          # Go to jail for 3 consecutive dbls
                    print('Rolled 3 consecutive doubles\n')
                    self.go_to_jail()
                    return                      # end turn

                elif self.position == 30:       # Landed on go to jail
                    self.go_to_jail()
                    return                      # end turn

                else:                           # roll again
                    d1, d2 = self.dice_roll()
                    print(self.name, 'rolled:', d1, d2)
            
            self.move(d1, d2)           # update information
            self.dbl_roll = 0

            self.print_position(board)

            if self.position == 30:        # landed on go to jail
                self.go_to_jail()
                return                     # end turn
         

def read_json(filename):
    """
    Takes in filename of json file that has the properties description 
    for the monopoly and reads in the json
    
    return: property_dict, dict
    """
    with open(filename) as f:
        property_dict = json.load(f)

    return property_dict

def create_board(f_layout, f_json):
    """
    Takes in a filename that leads to a file that contains what each 
    block does on a new line for every block.

    Input: filename: txt file containing what each block does
    Output: list, the gameboard
    """
    json_dict = read_json(f_json)

    f = open(f_layout, 'r')         # read layout file
    lines = f.readlines()

    board = []
    for line in lines:
        name = line[:-1]           # get rid of \n at end of the line
        try:
            info = json_dict[name]

        except KeyError:            # Not Land, utility or tax
            board += [name]

        else:                       # Land, utility or tax
            if info['type'] == "land":              # land
                board += [Land(name, info)]
            elif info['type'] == 'utilities':       # Utilities
                board += [Utilities(name,info)]
            elif info['type'] == 'railroad':        # Railroad
                board += [Railroad(name,info)]
            else:                                   # Tax
                board += [Taxes(name,info)]       
    
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

def game(f_layout=layout, f_json=description):
    """
    Runs the Monopoly game
    Input:
      filename: .txt file, the file the contains the layout of the board
                    default set to file included (board_layout.txt)
    """
    board = create_board(f_layout, f_json)                  # setup
    players = create_players()

    p_index = 0
    while True:
        current_p = players[p_index]
        current_p.player_turn(board)
        sleep(1)

        p_index += 1                                # next player
        if p_index == len(players):                 # reset p_index
            p_index = 0 

    
