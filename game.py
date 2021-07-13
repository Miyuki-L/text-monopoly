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
        self.mortgage_val = description['mortgage']
        self.mortgage = False
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
        self.mortgage_val = description['mortgage']
        self.mortgage = False
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
        self.mortgage_val = description['mortgage']
        self.mortgage = False
        self.owner = ''             #no one owns this property yet

    def cal_rent(self):
        """
        Finds the amount to times the dice roll by when a player lands on
        this property

        return int, amount to multiply by
        """
        owner = self.owner
        num_owned = len(owner.utilities)
        mult = self.rent[str(num_owned)]
        return mult


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

        self.bankrupt = False
        self.mortgage = []

    def dice_roll(self):
        """
        Rolls dice and returns the value of the two dices 
        Return: d1, d2
        """
        d1 = random.choice(range(1,7))
        d2 = random.choice(range(1,7))
        
        print(self.name, 'rolled:', d1, d2)
        
        return d1,d2

    def go_to_jail(self):
        """
        Updates players information when they are sent to jail
        """
        print(self.name, "going to jail.\n")
        
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
            print(f"{self.name} passed Go and collected $200.")
            self.money += 200
   
    def print_position(self,board):
        """
        Prints the block that landed on or is currently at 
        Input: board: the game board
        """
        block = board[self.position]

        if self.jail:                 # Player is in jail right now
            print(f"{self.name} is currently in Jail.\n")
        elif type(block) != str:      # landed on properties
            print(f"{self.name} landed on {block.name}.\n")
        else:
            print(f"{self.name} landed on {board[self.position]}.\n")

    def post_jail(self):
        """
        Moves the player when they leave the jail
        This is a separate function because rules are slightly different
            (Players do not get to roll again when they rolled a double)
        """
        self.jail = False               # Update information
        self.jail_roll = 0

        print(self.name, 'leaving jail. \n')

        d1, d2 = self.dice_roll()       # roll again (this time for moving)

        self.move(d1, d2)               

    def print_properties(self):
        """
        Prints all of the properties the Player owns and the Mortgage/House values of those properties
        Return prop_dict, dictionary of prop.name to property 
        """
        prop_dict = {}
        # Printing Property Names
        for prop_list in [self.land, self.railroad, self.utilities]:
            for prop in prop_list:
                if not prop.mortgage:                       # Not already mortgaged.
                    if type(prop) == Land:                      
                        print(f"{prop.name : <25} Mortgage Value: ${prop.mortgage_val: 4}  Houses: {prop.houses : <5} House value: ${((prop.upgradeCost)//2) : >4}")
                    else:
                        print(f"{prop.name : <25} Mortgage Value: ${prop.mortgage_val : 4}")

                    name = prop.name.lower()                       # have more flexibility with user input
                    prop_dict[name] = prop                         # Name: prop dict for easy access later

        print()
        return prop_dict 

    def mortgage_prop(self, owe):
        """
        Prompts the user to mortgage their property and adds the money they get from
        the mortgage to their money. Keeps prompting the user to sell houses/mortgage 
        properties until thier money is more than the amout they owe

        Input: owe, int, the amount that they have to pay
        """
        prop_dict = self.print_properties()

        while self.money < owe:
            print(f"{self.name}: You have ${self.money}. You owe ${owe}")
            prop_name = input(f"{self.name}: Which property to you want to sell a house on or mortgage? ")
            prop_name = prop_name.lower()

            while prop_name not in prop_dict or prop_dict[prop_name].mortgage:  # Make sure that they give a valid property
                prop_name = input(f"{self.name}: Which property to you want to sell a house on or mortgage? ")
                prop_name = prop_name.lower()

            prop = prop_dict[prop_name]
            if type(prop) == Land:                                # see if they have houses to sell
                houses = prop.houses
                house_val = prop.upgradeCost/2
                if houses != 0:                                   # They have houses they must sell first
                    if houses == 'hotel':
                        print(f"\n{self.name}: You have a hotel (5 houses) on {prop.name}. Value: {house_val}")
                        houses = 5                                # change to 5 so that it's easier to work with later
                    else:
                        print(f"\n{self.name}: You have {houses} houses on {prop.name}. Value: {house_val}")

                    n = 6                                         # place holder
                    while n > houses:
                        try:                                      # Check for valid input
                            n = int(input(f"{self.name}: How many houses on {prop.name} do you want to sell? "))
                            
                        except ValueError:              
                            print("Sorry, please try again")
                    print()
                    self.money += house_val * n                  # Update information
                    prop.houses = houses - n
                    continue                                     # Go back to the beginig of the while loop

            mortgage_val = prop.mortgage_val                     # mortgaging property
            self.mortgage += [prop]
            prop.mortgage = True
            self.money += mortgage_val
            prop_dict.pop(prop_name, None)                       # None is the type to specifiy as if they can't find the key
              
    def buy(self, block):
        """
        Prompts the user and askes if they want to buy the block they 
        landed on.
        If yes, conduct the transcation

        Input: block, Land (class)
        """
        print(f"{self.name}: You have ${self.money}.")
        decision = input(f"{self.name}: Do you want to buy {block.name} (Price:{block.price})? [y/n] ")

        while decision.lower() not in ['y', 'n', 'yes', 'no']:  # valid input?
            print(f"\n{self.name}: You have ${self.money}.")
            decision = input(f"{self.name}: Do you want to buy {block.name} (Price:{block.price})? [y/n] ")

        if decision.lower() in ['y','yes']:                         # buy
            if block.price <= self.money:                            # Have enough money
                self.money -= block.price                           # update information
                block.owner = self
                
                if type(block) == Land:
                    self.land += [block]
                elif type(block) == Utilities:
                    self.utilities += [block]
                elif type(block) == Railroad:
                    self.railroad += [block]

                print(f"{self.name} bought {block.name}.")
                print(f"{self.name}: You have ${self.money}.\n")
            else:                                                   # not enough money                    
                print(f"{self.name}: You do not have enough money.\n")
                return
        else:
            print()

    def upgrade(self, block):
        """
        Checks if an upgrade is avaliable if so
        Asks the owner of the block if they want to upgrade their property

        Input: block, class Land
        """
        if block.houses == 'hotel':
            print(f"No upgrades avaliable for {block.name}\n")
            return

        print(f"{self.name}: You have ${self.money}.")
        print(f"{block.name} has {block.houses} houses and the current rent is ${block.cal_rent()}.")
        if block.houses == 4:
            print(f"If you upgrade to hotel the rent would be ${block.rent['hotel']}.")
        else:
            print(f"If you upgrade to {block.houses+1} houses the rent would be {block.rent[str(block.houses+1)]}.")


        decision = input(f"{self.name}: Do you want to upgrade {block.name} (Cost:{block.upgradeCost})? [y/n] ")

        while decision.lower() not in ['y', 'n', 'yes', 'no']:  # valid input?
            print(f"\n{self.name}: You have ${self.money}.")
            decision = input(f"{self.name}: Do you want to upgrade {block.name} (Cost:{block.upgradeCost})? [y/n] ")

        if decision.lower() in ['y','yes']:                       # buy
            if block.upgradeCost <= self.money:                    # Have enough money
                block.houses += 1 

                if block.houses == 5:
                    block.houses = 'hotel'
                    print(f"\n{self.name} upgraded {block.name} to a hotel.")
                else:
                    print(f"\n{self.name} upgraded {block.name} to {block.houses} houses.")

                self.money -= block.upgradeCost

                print(f"{self.name}: You have ${self.money}.\n")
            else:
                print(f"{self.name}: You do not have enough money. \n")
        else:
            print()

    def rent(self, block):
        """
        checks the block that the player is on and see if they need to pay rent
            no rent if 1) their own block, 2) owner in jail or 3) property under mortgage
        """
        owner = block.owner

        if not owner.jail:                
            if not block.mortgage:           # property not under mortgage
                if type(block) in [Land, Railroad]:     # Land & Railroad have same method of rent calculation
                    rent = block.cal_rent()

                elif type(block) == Utilities:
                    d1, d2 = self.dice_roll()
                    mult = block.cal_rent()
                    rent = mult * (d1 + d2)

                if self.money < rent:                # Call Mortgaging functions
                    self.mortgage_prop(rent)

                self.money -= rent                      # Collect Rent 
                owner.money += rent

                print(f"{self.name} payed {owner.name} ${rent} for landing on {block.name}.")
                print(f"{self.name}: You have ${self.money}.\n")
            else:                                       # property played under mortgage
                print(f"{block.name} is under mortgage. No rent is payed. \n")
        else:                                           # owner in jail
            print(f"{owner.name} is in jail. No rent is payed.\n")

    def check_block(self, block):
        """
        Checks the Block that the player is currently on
        See if they could 1) buy the block, 2) upgrade the block, 3) pay
        
        Input: block: the block on the board the player is currently on
        """

        if type(block) == Land:                 
            if block.owner != '':               # Someone owns the land
                owner = block.owner

                if owner.name != self.name:     # pay rent?
                    self.rent(block)
                else:                           # upgrade?
                   self.upgrade(block) 
            else:                               # buy?
                self.buy(block)

        elif type(block) == Utilities:
            if block.owner != '':
                owner = block.owner

                if owner.name != self.name:     # pay?
                    self.rent(block)
            else:
                self.buy(block)                 # buy
        
        elif type(block) == Railroad:
            if block.owner != '':
                owner = block.owner

                if owner.name != self.name:     # pay?
                    self.rent(block)
            else:
                self.buy(block)                 # buy
        
        elif type(block) == Taxes:
            tax = block.price

            if self.money < tax:                # Call Mortgaging functions
                self.mortgage_prop(tax)

            self.money -= tax

            print(f"{self.name} payed ${tax} of {block.name}.")
            print(f"{self.name}: You have ${self.money}.\n")       

    def player_turn(self, board):
        """
        Moves the player for their turn.
        Input: board: the game board
        """
        d1, d2 = self.dice_roll()
        
        
        if self.jail:                           # In jail
            self.jail_roll += 1
            
            if self.jail_roll == 3:             # in jail for 3 rounds
                print(self.name, 'end of third turn in jail.')

                self.post_jail()                             
                self.print_position(board) 

            elif d1 == d2:                      # rolled a double
                print(self.name, 'rolled a double while in jail.')

                self.post_jail()
                self.print_position(board)
                       
            else:
                self.print_position(board)

        else:
            while d1 == d2:                     # rolled double
                self.move(d1, d2)               # update information
                self.dbl_roll += 1

                self.print_position(board)

                if self.dbl_roll == 3:          # Go to jail for 3 consecutive dbls
                    print('Rolled 3 consecutive doubles.\n')
                    self.go_to_jail()
                    return                      # end turn

                elif self.position == 30:       # Landed on go to jail
                    self.go_to_jail()
                    return                      # end turn

                else:                           # check block & roll again
                    self.check_block(board[self.position])  # Looks at the checks if they could buy or have to pay
                    d1, d2 = self.dice_roll()

            
            self.move(d1, d2)           # update information
            self.dbl_roll = 0

            self.print_position(board)

            if self.position == 30:        # landed on go to jail
                self.go_to_jail()
                return                     # end turn

            self.check_block(board[self.position])
         

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

if True:
    b = create_board(layout, description)
    p1 = Player('Hi')
    p1.land = [b[1], b[9], b[13], b[39]]
    b[1].houses = 'hotel'
    b[9].houses = 2
    p1.money = 10
    p1.utilities = [b[12]]
    p1.railroad = [b[5], b[25]]
    p1.mortgage_prop(500)