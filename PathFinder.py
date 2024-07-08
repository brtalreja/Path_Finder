#importing the essential libraries for the code.
import sys #to get the arguments from the command line and timer to run.
import pandas as pd #to load the driving distance and straight line distance in pandas dataframes.
from queue import PriorityQueue #to implement the frontier, we use the PriorityQueue as per the psuedocode.
import time #to benchmark the code we are running.

#accepting the arguments from command line and performing necessary checks.
no_of_args = len(sys.argv) #number of arguments.

#we need 3 arguments:
#1. program file name.
#2. Start State label.
#3. Goal State label.
#if the user has provided  3 inputs, continue, else, print the error.
if no_of_args == 3:
    startState = sys.argv[1] #1st argument will be stored as the start state.
    goalState = sys.argv[2]  #2nd argument will be stored as the goal state.

    #scriptName = sys.argv[0]
    #print("\nScript name: ", scriptName)

    #startState = "OR"
    #goalState = "NY"

    #start of reporting the results.
    print("Talreja, Bhavesh Rajesh, solution:")
    print("Initial State:",startState)
    print("Goal State:", goalState)

    #executing the code in try and except blocks to make sure that any key indexing exception is handled and appropriate results are printed.
    try:

        #Defining the Node class.

        class Node:
            #Documentation for the class.
            '''
            We set the Node class with 6 parameters:
            state: label of the state (type -> string)
            parent: which node is the parent of the child (type -> node)
            pathCost: the cost of traversering a route; driving distances (type -> int)
            heuristics: the heuristics cost of a path; straight line distances (type -> int)
            algorithm: the algorithm being implemented and accordingly the evaluation function will be chosen (type -> string)
            children: all the nodes that are connected to the node we are currently at (type -> dictionary) key: state label, value: driving distance.
            '''

            #defining the encapsulated method __init__ for the Node class.
            def __init__(self, state, parent, pathCost, heuristics, algorithm, children):
                #Setting all the parameters of the class Node.
                self.STATE = state #state label
                self.PARENT = parent #parent node
                self.PATHCOST = pathCost #cost of travel
                self.HEURISTICS = heuristics #straight line distance in this case which is an approximation
                self.ALGORITHM = algorithm #which algorithm are we implementing

                #GBFS: it always uses just the heuristics value for its informed search.
                if self.ALGORITHM == 'GBFS':
                    self.EVAL = self.HEURISTICS
                #ASTAR: it always uses the pathcost as well as the heuristic value for its informed search which makes it more efficient.
                elif self.ALGORITHM == 'ASTAR':
                    self.EVAL = self.PATHCOST + self.HEURISTICS
                self.CHILDREN = children #storing all the children of a node along with their distance as key-value in a dictionary.

            #Getting the required parameter using the getParameter methods.
            #getState() will help us to get/return the label of the state/node we are at.
            def getState(self):
                return self.STATE

            #getParent() will help us to get/return the parent node of the state/node we are at. If we are at initial node, it will be None.
            def getParent(self):
                return self.PARENT

            #getPathCost() will help us to get/return the driving distance from the state/node we are at to the child nodes. Pathcost from self to self will be zero.
            def getPathCost(self):
                return self.PATHCOST

            #getHeuristics() will help us to get/return the straight line distance from the state/node we are at to the goal state/node.
            #We use straight line distance here as an admissible heuristics because it always underestimates and due to this gives the shortest path.
            def getHeuristics(self):
                return self.HEURISTICS

            #getAlgorithm() will help us to get/return the algorithm we are running at the present moment.
            def getAlgorithm(self):
                return self.ALGORITHM

            #getEval() will help us to get/return the final evaluation value as per the algorithm we are running at the present moment.
            def getEval(self):
                return self.EVAL

            #__lt__() is an encapsulated method which helps us to compare two nodes based on their evaluation values.
            def __lt__(self, other):
                return self.getEval() < other.getEval()

            #__str__() helps us to print the node in the form of state label.
            def __str__(self):
                return self.STATE

            #__repr__() helps us to get information about the node which can be easily understood by developers.
            def __repr__(self):
                return str(self)

            #getChildren() will help us to get/return the children of the state/node we are at the present moment.
            def getChildren(self):
                return self.CHILDREN


        #expanding the node to get all the viable states/nodes, we can traverse from the current state/node.
        def expandNode(state):
            #using this expand function to store all the possible paths each node can explore.

            #initializing the dictionary to store this data.
            possible_children = {}

            #the driving distance data is read into the driving_df dataframe using pandas and we iterate over all the values of driving distance for the current state/node.
            #if the driving distance for current and another state is greater than zero, it means that there is a path from the current state to that state.
            for index, driving_dist in driving_df.loc[state].iteritems():
                if driving_dist > 0:
                    possible_children[str(index)] = driving_dist

            return possible_children
            #once we have all the children data for current state/node, we return it to explore which state we can go next.

        #getHeuristic is a function we are using to get the heuristic value of start state and the goal state.
        #It gets this information using indexing, from the sline_df dataframe which contains data from straightline.csv.
        def getHeuristic(startState, goalState):
            return sline_df.loc[startState, goalState]

        #Greedy Best First Search: As the name suggests, it is a greedy algorithm which considers the best choice at present.
        #However, since it is an informed search algorithm, it takes heuristics value into consideration to make the greedy choice.
        #This makes it better than Hill-climbing algorithm.
        def GBFSSearch(startState, goalState, heuristic):
            print("\nGreedy Best First Search:")

            #we initialize the start state or our present location as the Node object and pass in all the parameters.
            node = Node(startState, None, 0, heuristic, "GBFS", expandNode(startState))

            #Here we have tried to implement the algorithm using the try-except logic.
            #try block code tries to find the path and if it is not able to find it, goes to the except block which tells us that it's a failure and no path is found.
            try:

                #As per the pseudocode, we initialize the frontier as the priority queue.
                frontier = PriorityQueue()

                #In the frontier, we put the tuple of heuristic value and current node object.
                frontier.put((node.getHeuristics(), node))

                #Since we have reached the current state, we have to add it to the path which as per the pseudocode is the reached.
                #We create the reached as GBFS_reached as a dictionary which has the state label as the key and the node object as the value.
                GBFS_reached = {startState:node}

                #In order to calculate the number of nodes expanded, we initialize and instantiate the counter as 0.
                GBFS_counter=0

                #following the pseudocode, we iterate until the frontier is empty or the goal state is reached.
                while frontier.empty() == False:
                    #get the node from the frontier with the highest priority (heuristic value).
                    #the node is at index=1 in the tuple, hence we use .get()[1].
                    node = frontier.get()[1]

                    #for my debug:
                    #print(node, node.getParent(),node.getPathCost(), node.getHeuristics())

                    #Check if we have reached the goal state, if yes, get out of the loop, else continue.
                    if node.getState() == goalState:
                        break

                    #Since, the current state we are at is not the goal state, we will expand this state/node.
                    GBFS_counter += 1 #Hence increment the counter.

                    #For every child state/node, check the following two conditions:
                    #1st: if it is already in our reached data structure, i.e., if we have already reached there or not.
                    #2nd: if it is in reached, it will have some pathcost, we have to check, if revisiting the child state/node has lower or higher pathcost.
                    #Once both the conditions are checked, we will add the respective child node to the frontier.
                    for child in node.getChildren():
                        if (child not in GBFS_reached) or (node.getPathCost() + node.getChildren()[child] < GBFS_reached[child].getPathCost()):
                            GBFS_reached[child] = Node(
                                state = child,
                                parent = node,
                                pathCost = node.getPathCost() + node.getChildren()[child],
                                heuristics = getHeuristic(child,goalState),
                                algorithm = "GBFS",
                                children = expandNode(child)
                            )
                            #for my debug:
                            #print(GBFS_reached[child].getParent().getState()," : ","Pathcost:", GBFS_reached[child].getParent().getPathCost(), "children: ",GBFS_reached[child].getParent().getChildren())
                            #print(child," : ","Pathcost:", GBFS_reached[child].getPathCost(), "children: ",GBFS_reached[child].getChildren())
                            frontier.put((GBFS_reached[child].getHeuristics(),GBFS_reached[child]))

                #for my debug:
                #print(GBFS_reached)

                #the cost of path traversed from the start state to the goal state is updated with every iteration, and at the end the final node we are at has the total path cost which we get using .getPathCost().
                miles_covered = node.getPathCost()
                traversed_path = node.getState() #this is the final node and in order to print the path, we store it in a variable.

                #To get the path traversed from start state to goal state, we will check for parent of each node. As when we begin with the start node, we set its parent to be None.
                #Hence this loop will run until it gets back to start state.
                #To print the path, we are traversing back.
                while node.getParent():
                    node = node.getParent()
                    traversed_path = node.getState() + " " + traversed_path

                #Implementing necessary formattings for the output as per the HW report.
                traversed_path_list = traversed_path.split(' ')

                print("Solution path:", str(traversed_path_list))
                print("Number of states on a path:", len(traversed_path_list))
                print("Number of expanded nodes:", GBFS_counter)
                print("Path cost:", miles_covered, "miles")

            except Exception as e:
                #for my debug:
                #print(e)
                print("Solution path: FAILURE: NO PATH FOUND")
                print("Number of states on a path: 0")
                print("Path cost: 0")

        #A* Search: Just like GBFS, it is also an informed search algorithm, it takes heuristics value along with the path cost into consideration to make the optimum choice.
        #This makes it better than GBFS algorithm and even better than Hill-climbing algorithm.
        def AstarSearch(startState, goalState, heuristic):
            print("\nA* Search:")

            #we initialize the start state or our present location as the Node object and pass in all the parameters.
            node = Node(startState, None, 0, heuristic, "ASTAR", expandNode(startState))

            #Here we have tried to implement the algorithm using the try-except logic.
            #try block code tries to find the path and if it is not able to find it, goes to the except block which tells us that it's a failure and no path is found.
            try:

                #As per the pseudocode, we initialize the frontier as the priority queue.
                frontier = PriorityQueue()

                #In the frontier, we put the tuple of heuristic value along with path cost value and current node object.
                frontier.put((node.getPathCost() + node.getHeuristics(), node)) #Here, we are adding the current node path cost, since it is zero, it doesn't matter much here.

                #Since we have reached the current state, we have to add it to the path which as per the pseudocode is the reached.
                #Similar to GBFS, we create the reached as ASTAR_reached as a dictionary which has the state label as the key and the node object as the value.
                ASTAR_reached = {startState:node}

                #In order to calculate the number of nodes expanded, we initialize and instantiate the counter as 0.
                ASTAR_counter=0

                #following the pseudocode, we iterate until the frontier is empty or the goal state is reached.
                while frontier.empty() == False:
                    #get the node from the frontier with the highest priority (heuristic plus path cost value).
                    #the node is at index=1 in the tuple, hence we use .get()[1].
                    node = frontier.get()[1]

                    #for my debug:
                    #print(node, node.getParent(),node.getPathCost(), node.getHeuristics())

                    #Check if we have reached the goal state, if yes, get out of the loop, else continue.
                    if node.getState() == goalState:
                        break

                    #Since, the current state we are at is not the goal state, we will expand this state/node.
                    ASTAR_counter += 1 #Hence increment the counter.

                    #For every child state/node, check the following two conditions:
                    #1st: if it is already in our reached data structure, i.e., if we have already reached there or not.
                    #2nd: if it is in reached, it will have some pathcost, we have to check, if revisiting the child state/node has lower or higher pathcost.
                    #Once both the conditions are checked, we will add the respective child node to the frontier.
                    for child in node.getChildren():
                        if (child not in ASTAR_reached) or (node.getPathCost() + node.getChildren()[child] < ASTAR_reached[child].getPathCost()):
                            ASTAR_reached[child] = Node(
                                state = child,
                                parent = node,
                                pathCost = node.getPathCost() + node.getChildren()[child],
                                heuristics = getHeuristic(child,goalState),
                                algorithm = "ASTAR",
                                children = expandNode(child)
                            )
                            #for my debug:
                            #print(ASTAR_reached[child].getParent().getState()," : ","Pathcost:", ASTAR_reached[child].getParent().getPathCost(), "children: ",ASTAR_reached[child].getParent().getChildren())
                            #print(child," : ","Pathcost:", ASTAR_reached[child].getPathCost(), "children: ",ASTAR_reached[child].getChildren())
                            frontier.put((ASTAR_reached[child].getPathCost() + ASTAR_reached[child].getHeuristics(),ASTAR_reached[child]))

                #for my debug:
                #print(ASTAR_reached)

                #the cost of path traversed from the start state to the goal state is updated with every iteration, and at the end the final node we are at has the total path cost which we get using .getPathCost().
                miles_covered = node.getPathCost()
                traversed_path = node.getState() #this is the final node and in order to print the path, we store it in a variable.

                #To get the path traversed from start state to goal state, we will check for parent of each node. As when we begin with the start node, we set its parent to be None.
                #Hence this loop will run until it gets back to start state.
                #To print the path, we are traversing back.
                while node.getParent():
                    node = node.getParent()
                    traversed_path = node.getState() + " " + traversed_path

                #Implementing necessary formattings for the output as per the HW report.
                traversed_path_list = traversed_path.split(' ')

                print("Solution path:", str(traversed_path_list))
                print("Number of states on a path:", len(traversed_path_list))
                print("Number of expanded nodes:", ASTAR_counter)
                print("Path cost:", miles_covered, "miles")

            except Exception as e:
                #for my debug:
                #print(e)
                print("Solution path: FAILURE: NO PATH FOUND")
                print("Number of states on a path: 0")
                print("Path cost: 0")

        #reading the driving distances data from driving.csv into pandas dataframe.
        driving_df = pd.read_csv(r".\driving.csv",index_col=0)
        
        #reading the straight line distances (heuristics) data from straightline.csv into pandas dataframe.
        sline_df = pd.read_csv(r".\straightline.csv",index_col=0)

        #to begin our implementation, we get the heuristic distance value between start state and goal state.
        heuristic = getHeuristic(startState, goalState)

        #GBFS
        timeStart = time.time() #start timer
        GBFSSearch(startState, goalState, heuristic) #calling the GBFS method to find the path between start state and goal state as per GBFS algorithm.
        timeEnd = time.time() #end timer
        elapsedTimeInSec = timeEnd - timeStart #calculate the difference between start time and end time.
        print("Execution Time: {:.3f} seconds".format(elapsedTimeInSec)) #printing the execution time.

        #A*
        timeStart = time.time() #start timer
        AstarSearch(startState, goalState, heuristic) #calling the GBFS method to find the path between start state and goal state as per GBFS algorithm.
        timeEnd = time.time() #end timer
        elapsedTimeInSec = timeEnd - timeStart #calculate the difference between start time and end time.
        print("Execution Time: {:.3f} seconds".format(elapsedTimeInSec)) #printing the execution time.

    except:
        #Additional function for printing in case of failure (without executing any algorithm)
        def print_failure_output(algorithm_name):
            print(f"\n{algorithm_name}:")
            print("Solution path: FAILURE: NO PATH FOUND")
            print("Number of states on a path: 0")
            print("Path cost: 0")
            print("Execution Time: 0.000 seconds")

        # calling the function for GBFS
        print_failure_output("Greedy Best First Search")

        # calling the function for A*
        print_failure_output("A* Search")

else:
    print("ERROR: Not enough or too many input arguments.")
    