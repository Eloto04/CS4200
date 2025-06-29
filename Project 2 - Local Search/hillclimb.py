import random
import time

class Node:
    def __init__(self, puzzle: str, steps=0):
        self.puzzle = puzzle
        self.attacks = num_attacks(puzzle)
        self.steps = steps

def main():
    test_case_count = int(input("Enter a number of cases to test: "))
    solved_case_count = 0
    solved_step_count = 0
    solved_example = ""

    start = time.time()
    for _ in range(test_case_count):
        random_puzzle = ''.join(str(random.randint(1, 8)) for _ in range(8))
        state = hillclimb(random_puzzle)

        # Count every solved puzzle
        if state.attacks == 0:
            solved_case_count += 1
            solved_step_count += state.steps
            if solved_example == "":
                solved_example = state         
    end = time.time()

    percentage_solved = (solved_case_count / test_case_count) * 100
    step_avg = solved_step_count/solved_case_count
    print(f"Out of {test_case_count} cases, {solved_case_count} were solved. ({percentage_solved:.2f}%)")
    print(f"Total runtime: {end - start:.2f} seconds")
    print(f"Average step count of solved problems: {step_avg:.2f}\n")
    if solved_example != "":
        print(f"Example: Solution {solved_example.puzzle} generated in {solved_example.steps} steps")
        print_board(solved_example.puzzle)

def hillclimb(puzzle: str) -> Node:
    current = Node(puzzle)

    while True:
        neighbor = gen_best_successor(current)

        # No sideways or risky moves allowed
        if neighbor.attacks >= current.attacks:
            return current
        
        current = neighbor

def num_attacks(puzzle: str) -> int:
    attacks = 0

    # Pair (i, j) represents each unique combination of rows with queens to check
    for i in range(0, 7):
        for j in range(i + 1, 8):
            # Attack possible if queens in row pair (i, j) share a column or diagonal
            if puzzle[i] == puzzle[j] or abs(int(puzzle[i]) - int(puzzle[j])) == j - i:
                attacks += 1
    return attacks

def gen_best_successor(current: Node) -> Node:
    best_node = current

    # Nested for-loop objective:
    # Iterate through every row of the puzzle (1), changing its column value to all numbers from 1-8 inclusive. (2)
    # If the column value is the same as the original puzzle, skip it, as this is just the original state. (3)
    # Otherwise, it is a new successor to be generated and checked. (4)

    for i in range(8): # (1)
        for j in range(1, 9): # (2)
            if int(current.puzzle[i]) == j: # (3)
                continue

            new_puzzle = list(current.puzzle)
            new_puzzle[i] = str(j)
            new_puzzle_str = ''.join(new_puzzle)
            successor = Node(new_puzzle_str, steps=current.steps+1) # (4)

            # Greedy search, node with local minimum is tracked and returned
            if successor.attacks < best_node.attacks:
                best_node = successor

    return best_node

def print_board(puzzle: str) -> None:
    # 8 rows total in a puzzle (each represented with a string character)
    for row in range(8):
        line = ""

        # Find queen's column position in each row
        queen = int(puzzle[row])

        # Possible range of columns: 1-8 inclusive
        for col in range(1, 9):
            # Print an [x] at the column where a queen is found
            if col == queen:
                line += "[x]"
            else:
                line += "[ ]"
        print(line)

main()