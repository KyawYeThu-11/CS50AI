from os import remove
import random
import sys

from crossword import *


class CrosswordCreator():

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size,
             self.crossword.height * cell_size),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        w, h = draw.textsize(letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack(dict())

    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """
        for var in self.domains:
            for word in self.domains[var].copy():
                if len(word) != var.length:
                    self.domains[var].remove(word)

    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        revised = False
        overlap = self.crossword.overlaps[x, y]

        for x_word in self.domains[x].copy():
            satisfaction = False
            for y_word in self.domains[y]:
                # if there is atleast one possible value that y can take on given a value of x
                if y_word[overlap[1]] == x_word[overlap[0]]:
                    satisfaction = True
                    break
            
            # if no value in y is compatible with a given value of x
            if satisfaction is False:
                self.domains[x].remove(x_word)
                revised = True

        return revised 

    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """
        all_arcs = [
            overlap for overlap in self.crossword.overlaps
            if self.crossword.overlaps[overlap]
        ]

        queue = arcs if arcs else all_arcs
        while queue:
            for arc in queue.copy():
                queue.remove(arc)
                if self.revise(arc[0], arc[1]):
                    # if no value of x offers a possible value for y to take on, there's no solution
                    if len(self.domains[arc[0]]) == 0:
                        return False

                    # To ensure other arcs that's connected with x arc consistent with it even after its domain changes
                    for neighbor in self.crossword.neighbors(arc[0]):
                        if neighbor != arc[1]:
                            queue.append((neighbor, arc[0]))
        
        return True


    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        for var in self.crossword.variables:
            if var not in assignment:
                return False
        return True


    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """
        for var in assignment:
            # Check the length is satisfied
            for word in self.domains[var]:
                if len(assignment[var]) != len(word):
                    return False

            # Check all values are distinct
            assignment_copy = assignment.copy()
            del assignment_copy[var]

            for other_var in assignment_copy:
                if assignment[var] == assignment_copy[other_var]:
                    return False

            # Check if there are conflicting characters
            for neighbor in self.crossword.neighbors(var):
                overlap = self.crossword.overlaps[neighbor, var]

                if neighbor in assignment:
                    if assignment[neighbor][overlap[0]] != assignment[var][overlap[1]]:
                        return False

        return True

    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
        rule_out = {var_word:0 for var_word in self.domains[var]}

        for neighbor in self.crossword.neighbors(var):      
            if neighbor not in assignment:
                overlap = self.crossword.overlaps[neighbor, var]
                
                for var_word in self.domains[var]:
                    for neighbor_word in self.domains[neighbor]:
                        if neighbor_word[overlap[0]] != var_word[overlap[1]]:
                            rule_out[var_word] += 1

        return sorted(rule_out, key=lambda word:rule_out[word])

    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """

        unassigned_variables = [
            var for var in self.crossword.variables
            if var not in assignment
        ]

        domain_counts = {
            var: len(self.domains[var])
            for var in unassigned_variables
        }
        smallest_var = min(domain_counts, key=lambda word:domain_counts[word])
        
        # check if there are multiple variables with the same minimum domain counts
        smallest_vars = [
            key for key, value in domain_counts.items() 
            if value == len(self.domains[smallest_var])
        ]
        if len(smallest_vars) == 1:
            return smallest_var

        neighbor_counts = {
            var: len(self.crossword.neighbors(var))
            for var in unassigned_variables
        }
        highest_var = max(neighbor_counts, key=lambda word:neighbor_counts[word])
        
        return highest_var

    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """
        if self.assignment_complete(assignment):
            return assignment

        var = self.select_unassigned_variable(assignment)
        for word in self.order_domain_values(var, assignment):
            assignment[var] = word
            if self.consistent(assignment):
                result = self.backtrack(assignment)
                if result is not None:
                    return result
            del assignment[var]
        
        return None

def main():

    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()
