# Configuration constants for OpenSudoku

# Paper sizes in mm
PAPER_SIZES = {
    "A1": (594, 841),
    "A2": (420, 594),
    "A3": (297, 420),
    "A4": (210, 297),
    "A5": (148, 210),
}

# Default settings
DEFAULT_DIFFICULTY = "medium"
DEFAULT_SHEET_SIZE = "A4"
DEFAULT_PAGES = 1
DEFAULT_PUZZLES_PER_PAGE = 4
DEFAULT_MARGIN = 10  # mm
DEFAULT_PUZZLE_SPACING = 5  # mm (spacing between puzzles)

# Difficulty settings - number of cells to remove
DIFFICULTY_SETTINGS = {
    "easy": {"min_remove": 30, "max_remove": 35, "symmetry": True},
    "medium": {"min_remove": 40, "max_remove": 45, "symmetry": False},
    "my-mom": {"min_remove": 46, "max_remove": 50, "symmetry": False},
    "hard": {"min_remove": 51, "max_remove": 57, "symmetry": False},
}

# Sudoku grid constants
GRID_SIZE = 9
BOX_SIZE = 3
TOTAL_CELLS = GRID_SIZE * GRID_SIZE

# PDF rendering constants
MM_TO_POINTS = 2.83465  # 1 mm = 2.83465 points
LINE_WIDTH_THICK = 0.15  # For box boundaries
LINE_WIDTH_THIN = 0.05  # For cell boundaries
FONT_SIZE_SCALE = 0.4  # Scale factor for number font size
