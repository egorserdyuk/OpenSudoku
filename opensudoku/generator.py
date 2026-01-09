import random
from .constants import GRID_SIZE, BOX_SIZE
from .difficulty import DifficultyEngine


class SudokuPuzzle:
    """Represents a single Sudoku puzzle with solution."""

    def __init__(self, puzzle, solution, difficulty):
        self.puzzle = puzzle
        self.solution = solution
        self.difficulty = difficulty
        self.puzzle_id = f"{difficulty}-{random.randint(1000, 9999)}"

    def get_puzzle_grid(self):
        """Return the puzzle grid (with zeros for empty cells)."""
        return self.puzzle

    def get_solution_grid(self):
        """Return the complete solution grid."""
        return self.solution

    def get_difficulty(self):
        """Return the difficulty level."""
        return self.difficulty

    def get_id(self):
        """Return the puzzle ID."""
        return self.puzzle_id


class PuzzleGenerator:
    """Generates Sudoku puzzles with specified difficulty."""

    def __init__(self):
        self.difficulty_engine = None

    def generate_puzzle(self, difficulty="medium"):
        """Generate a complete Sudoku puzzle with specified difficulty."""
        # Initialize difficulty engine
        self.difficulty_engine = DifficultyEngine(difficulty)

        # Generate a complete solution
        solution = self.generate_solution()

        # Create puzzle by removing numbers based on difficulty
        puzzle = self.difficulty_engine.select_removal_pattern(solution)

        # Validate that the puzzle has exactly one solution
        if not self.validate_uniqueness(puzzle):
            # If not unique, try again
            return self.generate_puzzle(difficulty)

        return SudokuPuzzle(puzzle, solution, difficulty)

    def generate_solution(self):
        """Create a valid completed Sudoku grid using backtracking."""
        grid = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

        # Fill the grid using backtracking
        self._fill_grid(grid, 0, 0)

        return grid

    def _fill_grid(self, grid, row, col):
        """Recursive backtracking algorithm to fill the Sudoku grid."""
        # Move to next row if current row is complete
        if col == GRID_SIZE:
            row += 1
            col = 0

        # If we've filled all rows, we're done
        if row == GRID_SIZE:
            return True

        # Skip already filled cells
        if grid[row][col] != 0:
            return self._fill_grid(grid, row, col + 1)

        # Try numbers 1-9
        for num in range(1, GRID_SIZE + 1):
            if self._is_valid(grid, row, col, num):
                grid[row][col] = num

                if self._fill_grid(grid, row, col + 1):
                    return True

                # Backtrack
                grid[row][col] = 0

        return False

    def _is_valid(self, grid, row, col, num):
        """Check if placing num at (row, col) is valid."""
        # Check row
        if num in grid[row]:
            return False

        # Check column
        if num in [grid[i][col] for i in range(GRID_SIZE)]:
            return False

        # Check 3x3 box
        box_row, box_col = row // BOX_SIZE * BOX_SIZE, col // BOX_SIZE * BOX_SIZE
        for i in range(BOX_SIZE):
            for j in range(BOX_SIZE):
                if grid[box_row + i][box_col + j] == num:
                    return False

        return True

    def validate_uniqueness(self, puzzle):
        """Ensure puzzle has exactly one solution."""
        # Count solutions using backtracking
        solution_count = 0
        grid = [row[:] for row in puzzle]

        def count_solutions(grid, row, col):
            nonlocal solution_count

            if solution_count > 1:
                return  # Early exit if multiple solutions found

            if col == GRID_SIZE:
                row += 1
                col = 0

            if row == GRID_SIZE:
                solution_count += 1
                return

            if grid[row][col] != 0:
                count_solutions(grid, row, col + 1)
                return

            for num in range(1, GRID_SIZE + 1):
                if self._is_valid(grid, row, col, num):
                    grid[row][col] = num
                    count_solutions(grid, row, col + 1)
                    grid[row][col] = 0

        count_solutions(grid, 0, 0)
        return solution_count == 1

    def generate_multiple_puzzles(self, count, difficulty="medium"):
        """Generate multiple puzzles with the same difficulty."""
        puzzles = []
        for _ in range(count):
            puzzle = self.generate_puzzle(difficulty)
            puzzles.append(puzzle)
        return puzzles
