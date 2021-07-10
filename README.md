# text-monopoly
Simplified and modified text based version of the game Monopoly. The none color set way of Monopoly

## Before Running
Have game.py, board_layout.txt, and properties_tax.json in the same folder before running

## Starting the game
Run game.py and then run the game function to start the game

## Game Rules
- Player goes to jail if they land on the go to jail or if they roll 3 consecutive doubles
    - Leave jail after 3 turns in jail or rolling a double.
    - When the player leaves they could roll the dice. E.g. player just rolled a double while in jail. They could no roll again and move
- Player can roll again if they rolled a double except if they just got out of jail. 
- If a player does not choose to buy the property they land on, THERE IS NO AUCTION
- Player could only upgrade/build a house on theur property when they land on the property and they can only build 1 house at a time.
- Game ends when the all but 1 player is bankrupt
    - Bankrupt = not having money even after mortgaging everything they own.
    - Before mortgaging the property they must sell/down grade the houses they have on their property. The money the player gets for selling 1 house or from hotel to 4 houses is half the upgrade cost.
## Current Status of the Game
The game currently runs and is functional but it does not have some features of monopoly such as Chance and Community Chest. Additionally the game does not currently stop right now when the player is out of money. Instead the player's money would become negative but not actions are limited.

The game currently only supports the rolling of die, going to jail/leaving jail, buying property, and paying rent.