import random
from .constants import DIFFICULTY_SETTINGS, GRID_SIZE


class DifficultyEngine:
    """Handles difficulty-specific puzzle generation logic."""

    def __init__(self, difficulty="medium"):
        self.difficulty = difficulty
        self.settings = DIFFICULTY_SETTINGS.get(difficulty)
        if not self.settings:
            raise ValueError(f"Unknown difficulty level: {difficulty}")

    def calculate_removal_count(self):
        """Determine how many numbers to remove based on difficulty."""
        return random.randint(self.settings["min_remove"], self.settings["max_remove"])

    def select_removal_pattern(self, grid):
        """Choose removal strategy based on difficulty."""
        removal_count = self.calculate_removal_count()

        if self.settings["symmetry"]:
            # Symmetric removal for easy puzzles
            return self._symmetric_removal(grid, removal_count)
        else:
            # Asymmetric removal for harder puzzles
            return self._asymmetric_removal(grid, removal_count)

    def _symmetric_removal(self, grid, count):
        """Remove cells symmetrically (mirror pattern)."""
        puzzle = [row[:] for row in grid]
        removed = 0

        # Create a list of all cell positions
        all_cells = [(i, j) for i in range(GRID_SIZE) for j in range(GRID_SIZE)]
        random.shuffle(all_cells)

        for i, j in all_cells:
            if removed >= count:
                break

            # Check if symmetric counterpart is also removable
            sym_i, sym_j = GRID_SIZE - 1 - i, GRID_SIZE - 1 - j

            if puzzle[i][j] != 0 and puzzle[sym_i][sym_j] != 0:
                puzzle[i][j] = 0
                puzzle[sym_i][sym_j] = 0
                removed += 2

        return puzzle

    def _asymmetric_removal(self, grid, count):
        """Remove cells asymmetrically."""
        puzzle = [row[:] for row in grid]
        removed = 0

        # Create a list of all cell positions
        all_cells = [(i, j) for i in range(GRID_SIZE) for j in range(GRID_SIZE)]
        random.shuffle(all_cells)

        for i, j in all_cells:
            if removed >= count:
                break

            if puzzle[i][j] != 0:
                puzzle[i][j] = 0
                removed += 1

        return puzzle

    def validate_difficulty(self, puzzle, solution):
        """Verify puzzle matches difficulty rating."""
        # Count empty cells
        empty_count = sum(row.count(0) for row in puzzle)

        # Check if empty count is within expected range
        expected_min = self.settings["min_remove"]
        expected_max = self.settings["max_remove"]

        return expected_min <= empty_count <= expected_max

    def get_difficulty_name(self):
        """Get human-readable difficulty name."""
        return self.difficulty.replace("-", " ")
