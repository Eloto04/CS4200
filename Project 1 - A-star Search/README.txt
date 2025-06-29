"main.py" is the function containing the A* search algorithm for this project.
To initiate the main menu, run the program in a Python-supported IDE. 

At each step of the menu, you will enter a number depending on what you would like to do.

1: Enter '1' to Test a Puzzle, or enter '2' to exit.
2: (if '1' chosen in step 1): Enter '1' to randomly generate a puzzle, or enter '2' to manually input one.
3: (if '2' chosen in step 2): You will be prompted 3 times to enter 3 numbers for each row in your input square.
Whitespace is acceptable if desired, as it is removed after input.

i.e.
Row 1: 042
Row 2: 135
Row 3: 678

or

Row 1: 0 4 2
Row 2: 1 3 5
Row 3: 6 7 8

4: Once you have either entered a puzzle or selected random generation, you will pick a heuristic.
Enter '1' to select H1 (number of misplaced tiles), '2' to select H2 (sum of Manhattan distances from correct positions), or '3' to run the algorithm once for H1 and again for H2 subsequently.

5: Your solution(s) should be generated now. The program will start again from the beginning, at which you can enter '2' to exit if you wish.

The menu is safe to handle inputs that do not meet a valid decision. Examples include:

- Numeric menu selections less than 0 or greater than 2 or 3
- Non-numeric inputs (alphabet or special characters)
- Row inputs containing input other than 3 numbers

If any of the above cases are present, a warning (i.e. "Invalid selection.") will be displayed in the terminal.




