# Path finder

This project implements two informed search algorithms, Greedy Best First Search (GBFS) and A* Search, to find the shortest path between two states based on driving distances and straight-line distances (heuristics).

## Getting Started

### Prerequisites

Python 3 with the following libraries:
- pandas
- queue

### Installing Dependencies

pip install pandas

### Running the Code

To run the code, execute main.py with the following arguments:

Start State label
Goal State label

### Example:

python main.py OR NY

### Project Structure

PathFinder.py: Entry point of the program.
driving.csv: CSV file containing driving distances between states.
straightline.csv: CSV file containing straight-line distances (heuristics) between states.
README.md: This file, providing an overview of the project.

### Algorithms Implemented

Greedy Best First Search (GBFS): GBFS is an informed search algorithm that selects the path which appears best based on heuristic information. It explores nodes in the order of their heuristic value, ignoring the path cost.

A* Search: A* Search is an informed search algorithm that uses both the path cost and heuristic value to select the path. It ensures the shortest path by combining the actual cost to reach a node and the estimated cost to reach the goal.

### Results

After running the program, it outputs:

Solution path: The sequence of states from Start State to Goal State.
Number of states on the path: Total states traversed from Start to Goal.
Number of expanded nodes: Total nodes expanded during the search.
Path cost: Total driving distance from Start State to Goal State.
Execution Time: Time taken to execute the algorithms.

### Authors

Bhavesh Rajesh Talreja
