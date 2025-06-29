import random
import heapq
import time

class Node:
    def __init__(self, puzzle, parent=None, g=0, h=0):
        self.puzzle = puzzle
        self.parent = parent
        self.g = g
        self.h = h
        self.f = self.g + self.h

    def __lt__(self, other):
        return self.f < other.f

# Recursive menu for running the algorithm
def main():
    print("CS 4200 Project 1")
    
    while True:
        # Test puzzle or exit program
        while True:
            print("Select:")
            print("[1] Test a Puzzle")
            print("[2] Exit")
            user_choice = input().replace(" ", "")

            if user_choice == '1':
                break
            elif user_choice == '2': 
                return
            else:
                print("Invalid selection.")

        # Input a puzzle or generate a random one
        while True:
            print("Select Input Method")
            print("[1] Random")
            print("[2] Input")
            user_choice = input().replace(" ", "")

            if user_choice == '1':
                puzzle = random_puzzle()
                break
            elif user_choice == '2':
                puzzle = enter_puzzle()
                break
            else:
                print("Invalid selection.")

        print("Puzzle:")
        print_puzzle(puzzle)

        if not is_solvable(puzzle):
            print("Not a solvable puzzle.")
            continue

        # Select heuristic(s) to run
        while True:
            print("Select H Function:")
            print("[1] H1")
            print("[2] H2")
            print("[3] Both (H1 then H2)")
            user_choice = input().replace(" ", "")

            if user_choice == '1':
                run_astar(puzzle, "H1")
                break
            elif user_choice == '2':
                run_astar(puzzle, "H2")
                break
            elif user_choice == '3':
                run_astar(puzzle, "H1")
                run_astar(puzzle, "H2")
                break
            else:
                print("Invalid selection.")

# Runs astar, printing search cost and runtime
def run_astar(puzzle: str, heuristic: str):
    start = time.time()
    solution = astar(puzzle, heuristic)
    end = time.time()

    print_solution(solution[0])
    print(f"{heuristic} Search Cost: {solution[1]}")
    print(f"{heuristic} Runtime: {end - start:.2f} seconds")

# The algorithm to be ran on a puzzle with either h1 or h2
def astar(puzzle: str, heuristic: str):
    # Initial state
    if heuristic == "H1":
        node = Node(puzzle, h=h1(puzzle))
    elif heuristic == "H2":
        node = Node(puzzle, h=h2(puzzle))

    # Priority queue with initial state (node) as only element
    frontier = []
    heapq.heappush(frontier, node)

    # Initialized as an empty set
    explored = set()

    # Number of nodes generated during algorithm
    search_cost = 0
    
    # Continues as long as frontier is not empty
    while frontier:
        # Lowest-cost node popped from frontier
        node = heapq.heappop(frontier)

        # Goal reached, puzzle is solved
        if node.puzzle == "012345678":
            return node, search_cost
        
        # Node's current state was reached with a lower f, skip
        if node.puzzle in explored:
            continue

        # Otherwise, explore this node's successors
        explored.add(node.puzzle)

        for child in successors(node, heuristic):
            # child = a generated successor
            search_cost += 1

            # Unexplored states are added to the frontier
            if child.puzzle not in explored:
                # Min-heap ensures nodes with lowest f are always explored first
                heapq.heappush(frontier, child)

# h1 = the number of misplaced tiles
def h1(puzzle: str) -> int:
    misplaced_tiles = 0
    goal_puzzle = "012345678"

    for i in range(9):
        # Evaluate position of every square except 0
        if puzzle[i] != '0' and puzzle[i] != goal_puzzle[i]:
            misplaced_tiles += 1

    return misplaced_tiles

# h2 = the sum of the Manhattan distances of the tiles from their goal positions
def h2(puzzle: str) -> int:
    goal_puzzle = "012345678"
    manhattan_sum = 0

    for i, square in enumerate(puzzle):
        # 0 square excluded
        if square != '0':
            # Correct index of current square
            target = goal_puzzle.index(square)

            # Current position of square
            x1, y1 = i % 3, i // 3

            # Goal position of square
            x2, y2 = target % 3, target // 3

            # Manhattan distance formula (between current and goal position of each square)
            manhattan_sum += abs(x1 - x2) + abs(y1 - y2)

    return manhattan_sum

# Returns an array of all possible actions from a node
def successors(current: Node, heuristic: str) -> list[Node]:
    neighbors = []

    # Location of 0 in the puzzle
    i = current.puzzle.index('0')

    # Moving 0 down possible
    if i < 6:
        puzzle_list = list(current.puzzle)
        puzzle_list[i], puzzle_list[i+3] = puzzle_list[i+3], puzzle_list[i]
        h = h1(''.join(puzzle_list)) if heuristic == "H1" else h2(''.join(puzzle_list))
        neighbors.append(Node(''.join(puzzle_list), current, current.g+1, h))

    # Moving 0 up possible
    if i > 2:
        puzzle_list = list(current.puzzle)
        puzzle_list[i], puzzle_list[i-3] = puzzle_list[i-3], puzzle_list[i]
        h = h1(''.join(puzzle_list)) if heuristic == "H1" else h2(''.join(puzzle_list))
        neighbors.append(Node(''.join(puzzle_list), current, current.g+1, h))

    # Moving 0 left possible
    if i % 3 > 0:
        puzzle_list = list(current.puzzle)
        puzzle_list[i], puzzle_list[i-1] = puzzle_list[i-1], puzzle_list[i]
        h = h1(''.join(puzzle_list)) if heuristic == "H1" else h2(''.join(puzzle_list))
        neighbors.append(Node(''.join(puzzle_list), current, current.g+1, h))

    # Moving 0 right possible
    if i % 3 < 2:
        puzzle_list = list(current.puzzle)
        puzzle_list[i], puzzle_list[i+1] = puzzle_list[i+1], puzzle_list[i]
        h = h1(''.join(puzzle_list)) if heuristic == "H1" else h2(''.join(puzzle_list))
        neighbors.append(Node(''.join(puzzle_list), current, current.g+1, h))

    return neighbors

# Helper function to print a solution and its steps
def print_solution(solution: Node) -> None:
    path = []
    i = 0
    
    while solution:
        path.append(solution.puzzle)
        solution = solution.parent
    for puzzle in path[-2::-1]:
        i += 1
        print(f"Step: {i}")
        print_puzzle(puzzle)

# Helper function to neatly print a puzzle configuration
def print_puzzle(puzzle: str) -> None:
    print(f"{puzzle[0]} {puzzle[1]} {puzzle[2]}\n{puzzle[3]} {puzzle[4]} {puzzle[5]}\n{puzzle[6]} {puzzle[7]} {puzzle[8]}\n")

# Generates a solvable random puzzle
def random_puzzle() -> str:
    while True:
        squares = list("012345678")
        random.shuffle(squares)
        if is_solvable(''.join(squares)):
            return ''.join(squares)

# Evaluates whether an input puzzle is solvable, or warns the user if their input is wrong
def is_solvable(puzzle: str) -> bool:
    # Ensure input has the correct format
    if ''.join(sorted(puzzle)) != '012345678':
        print("Your input is not valid.")
        return False

    puzzle_arr = [int(x) for x in puzzle if x != '0']
    inversions = 0

    for i in range(0, len(puzzle_arr) - 1):
        for j in range(i + 1, len(puzzle_arr)):
            if puzzle_arr[i] > puzzle_arr[j]:
                inversions += 1
    
    # Solvable only if number of inversions is even
    if inversions % 2 != 0:
        return False
    
    return True

# Helper function to enter a puzzle configuration, used during the menu
def enter_puzzle():
    puzzle = ""
    print("Enter a Puzzle (row by row):")
    for i in range(3):
        row_input = ""
        while len(row_input) != 3:
            print(f"Row {i+1}: ", end="")
            row_input = input().replace(" ", "")
            if len(row_input) != 3:
                print("Please enter 3 numbers only.")
        puzzle += row_input
    return puzzle

# Helper function to print test cases with their search costs, used in creating report
def testing():
    # Tested with the provided files
    '''for test_cases in ["Length4.txt", "Length8.txt", "Length12.txt", "Length16.txt", "Length20.txt"]:
        with open(test_cases, "r") as file:
            lines = file.readlines()
            for i in range(0, len(lines), 4):
                puzzle = ""
                puzzle += lines[i+1].replace(" ", "").strip()
                puzzle += lines[i+2].replace(" ", "").strip()
                puzzle += lines[i+3].replace(" ", "").strip()
                h1 = astar(puzzle, "H1")
                h2 = astar(puzzle, "H2")
                print(f"{puzzle},{h1[0].g},{h1[1]},{h2[1]}")'''

    # 200 random cases generated to build a table from in the report
    i = 0
    while i < 200:
        puzzle = random_puzzle()
        h1 = astar(puzzle, "H1")
        h2 = astar(puzzle, "H2")

        # Testing to make sure h1 and h2 solutions have equal number of steps
        '''if h1[0].g != h2[0].g:
            print("ERROR")
            print(f"{h1[0].g} {h2[0].g}")
            return'''

        if h1[0].g % 2 == 0 and h1[0].g <= 24:
            # Output to be copied and pasted into a .csv file
            print(f"{puzzle},{h1[0].g},{h1[1]},{h2[1]}")
            i += 1

# testing()
main()