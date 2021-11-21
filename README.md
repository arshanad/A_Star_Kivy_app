# A_Star_Kivy_app
## Objectives:
Create an app that has the following features:
1. Allows a user to register their details, store them in a file and login
2. Create a board using player input for size
3. Allow player to place or remove obstacles on the board that a pawn has to navigate through
to reach from one end of a diagonal to the other.
## Requirements:
1. Python 3.7.7
2. kivy 1.11. 1
## A_StarGraph.py
This stores the class to provide functions to store the position of barriers, return the heuristic
function value of each cell, return neighbours of each cell, and the cost to move to a neighbouring
cell.

In the main, we define an object of AStarGraph type to store the size of the board and barriers
entered through the UI.
## database.py
It defines the class DataBase and all the associated functions to store data in a text file and access it.
In the main.py, we import this and define an object of type DataBase to store login details in the file
“users.txt”.
## main.py
This is the main file to be executed.
## Project Report.pdf
It is the project report containing additional details.
