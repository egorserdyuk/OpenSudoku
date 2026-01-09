from .constants import PAPER_SIZES, DEFAULT_MARGIN, MM_TO_POINTS, DEFAULT_PUZZLE_SPACING


class SheetDimensions:
    """Paper size specifications in mm and points."""

    def __init__(self, sheet_size):
        self.sheet_size = sheet_size
        self.width_mm, self.height_mm = PAPER_SIZES[sheet_size]
        self.width_points = self.width_mm * MM_TO_POINTS
        self.height_points = self.height_mm * MM_TO_POINTS
        self.margin = DEFAULT_MARGIN * MM_TO_POINTS

        # Available content area (excluding margins)
        self.content_width = self.width_points - 2 * self.margin
        self.content_height = self.height_points - 2 * self.margin


class LayoutCalculator:
    """Calculate optimal puzzle positioning on sheets."""

    def __init__(self, sheet_size, puzzles_per_page, puzzle_spacing=None):
        self.sheet_dimensions = SheetDimensions(sheet_size)
        self.puzzles_per_page = puzzles_per_page
        self.puzzle_spacing = (
            puzzle_spacing
            if puzzle_spacing is not None
            else DEFAULT_PUZZLE_SPACING * MM_TO_POINTS
        )

    def calculate_grid_layout(self):
        """Determine optimal rows and columns for puzzle grid."""
        # Try to find the most square-like arrangement
        best_cols = 1
        best_rows = self.puzzles_per_page
        best_ratio = float("inf")

        for cols in range(1, self.puzzles_per_page + 1):
            if self.puzzles_per_page % cols != 0:
                continue

            rows = self.puzzles_per_page // cols
            ratio = max(rows / cols, cols / rows)

            if ratio < best_ratio:
                best_ratio = ratio
                best_cols = cols
                best_rows = rows

        return best_rows, best_cols

    def compute_puzzle_positions(self):
        """Calculate x,y coordinates for each puzzle."""
        rows, cols = self.calculate_grid_layout()

        # Calculate puzzle size
        puzzle_width, puzzle_height = self.optimize_puzzle_size(rows, cols)

        positions = []

        for puzzle_idx in range(self.puzzles_per_page):
            row = puzzle_idx // cols
            col = puzzle_idx % cols

            # Calculate position with spacing between puzzles
            x = self.sheet_dimensions.margin + col * (
                puzzle_width + self.puzzle_spacing
            )
            y = (
                self.sheet_dimensions.height_points
                - self.sheet_dimensions.margin
                - (row + 1) * puzzle_height
                - row * self.puzzle_spacing
            )

            positions.append(
                {
                    "x": x,
                    "y": y,
                    "width": puzzle_width,
                    "height": puzzle_height,
                    "puzzle_number": puzzle_idx + 1,
                }
            )

        return positions

    def optimize_puzzle_size(self, rows, cols):
        """Maximize puzzle size while maintaining margins and spacing."""
        # Calculate available space per puzzle, accounting for spacing
        # Total spacing between puzzles: (cols-1) * spacing horizontally, (rows-1) * spacing vertically
        total_spacing_width = (cols - 1) * self.puzzle_spacing
        total_spacing_height = (rows - 1) * self.puzzle_spacing

        # Available space for puzzles after accounting for spacing
        available_width = (
            self.sheet_dimensions.content_width - total_spacing_width
        ) / cols
        available_height = (
            self.sheet_dimensions.content_height - total_spacing_height
        ) / rows

        # Use the smaller dimension to maintain square puzzles
        puzzle_size = min(available_width, available_height)

        return puzzle_size, puzzle_size

    def get_sheet_dimensions(self):
        """Return sheet dimensions object."""
        return self.sheet_dimensions

    def get_max_puzzles_for_sheet(self):
        """Calculate maximum number of puzzles that fit on sheet."""
        # This is a rough estimate based on minimum puzzle size
        min_puzzle_size = 50 * MM_TO_POINTS  # Minimum 50mm per puzzle

        max_cols = int(self.sheet_dimensions.content_width / min_puzzle_size)
        max_rows = int(self.sheet_dimensions.content_height / min_puzzle_size)

        return max_cols * max_rows
