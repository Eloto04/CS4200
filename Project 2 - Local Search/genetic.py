import random
import time

def main():
    solution_count = int(input("Enter desired number of genetic algorithm solutions: "))
    total_time = 0.0

    for i in range(solution_count):
        population = gen_population(100)
        start = time.time()
        individual = genetic_algorithm(population)
        end = time.time()

        print(f"Iteration {i + 1} found a solution: {individual} ({end - start:.2f} seconds)")
        print_board(individual)
        print()
        total_time += end - start
    
    print(f"{solution_count} solution(s) found in {total_time:.2f} seconds.")
    return

def genetic_algorithm(population: list[str]) -> str:
    children = 0
    while True:
        new_population = []
        for _ in range(len(population)):
            # Selection
            x = population[random.randint(0, len(population) - 1)]
            y = population[random.randint(0, len(population) - 1)]

            # Crossover
            child = reproduce(x, y)
            children += 1

            # Mutation
            child = mutate(child, 0.1)

            if fitness(child) == 28:
                print("Children generated: " + str(children))
                return child

            new_population.append(child)

        population = new_population

def gen_population(size: int) -> list[str]:
    population = []
    for _ in range(size): 
        puzzle = ""
        for _ in range(8):
            puzzle += str(random.randint(1, 8))
        population.append(puzzle)
    return population

def fitness(puzzle: str) -> int:
    safe_pairs = 28

    # Pair (i, j) represents each unique combination of rows with queens to check
    for i in range(0, 7):
        for j in range(i + 1, 8):
            # Attack possible if queens in row pair (i, j) share a column or diagonal
            if puzzle[i] == puzzle[j] or abs(int(puzzle[i]) - int(puzzle[j])) == j - i:
                safe_pairs -= 1

    return safe_pairs

def reproduce(x: str, y: str) -> str:
    c = random.randint(1, 8)
    child = x[0:c] + y[c:8]
    return child

def mutate(puzzle: str, mutation_rate: float) -> str:
    puzzle_list = list(puzzle)
    for i in range(len(puzzle_list)):
        if random.random() < mutation_rate:
            puzzle_list[i] = str(random.randint(1, 8))
    return ''.join(puzzle_list)

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