from reportlab.pdfgen import canvas
from datetime import datetime
from .constants import LINE_WIDTH_THICK, LINE_WIDTH_THIN, FONT_SIZE_SCALE


class SudokuDrawer:
    """Draws individual Sudoku grids."""

    def __init__(self):
        pass

    def draw_sudoku_grid(self, canvas, puzzle, position, width, height):
        """Render a single Sudoku puzzle."""
        x, y = position["x"], position["y"]

        # Draw grid lines
        self.draw_grid_lines(canvas, x, y, width, height)

        # Fill in the numbers
        self.fill_numbers(canvas, puzzle, x, y, width, height)

        # Add puzzle number
        # self.draw_puzzle_number(canvas, position, width, height)

    def draw_grid_lines(self, canvas, x, y, width, height):
        """Draw Sudoku grid structure."""
        cell_size = width / 9

        # Draw thick lines for box boundaries
        canvas.setLineWidth(LINE_WIDTH_THICK)
        for i in range(0, 10, 3):
            # Vertical lines
            canvas.line(x + i * cell_size, y, x + i * cell_size, y + height)
            # Horizontal lines
            canvas.line(x, y + i * cell_size, x + width, y + i * cell_size)

        # Draw thin lines for cell boundaries
        canvas.setLineWidth(LINE_WIDTH_THIN)
        for i in range(9):
            if i % 3 != 0:  # Skip box boundaries (already drawn)
                # Vertical lines
                canvas.line(x + i * cell_size, y, x + i * cell_size, y + height)
                # Horizontal lines
                canvas.line(x, y + i * cell_size, x + width, y + i * cell_size)

    def fill_numbers(self, canvas, puzzle, x, y, width, height):
        """Add given numbers to the grid."""
        cell_size = width / 9
        font_size = cell_size * FONT_SIZE_SCALE

        canvas.setFont("Helvetica", font_size)

        for row in range(9):
            for col in range(9):
                value = puzzle[row][col]
                if value != 0:
                    # Calculate text position (centered in cell)
                    text_x = x + col * cell_size + cell_size / 2
                    text_y = y + row * cell_size + cell_size / 2 - font_size / 3

                    canvas.drawCentredString(text_x, text_y, str(value))

    def draw_puzzle_number(self, canvas, position, width, height):
        """Add puzzle number above the grid."""
        puzzle_number = position["puzzle_number"]
        x, y = position["x"], position["y"]

        font_size = width * 0.05  # 5% of puzzle width
        canvas.setFont("Helvetica-Bold", font_size)

        # Position above the puzzle
        text_x = x + width / 2
        text_y = y + height + font_size * 1.5

        canvas.drawCentredString(text_x, text_y, f"Puzzle {puzzle_number}")


class PDFGenerator:
    """Main PDF creation orchestrator."""

    def __init__(self):
        self.sudoku_drawer = SudokuDrawer()

    def create_pdf(
        self, puzzles, layout_calculator, output_path, include_solutions=False
    ):
        """Generate complete PDF with positioned puzzles."""
        # Get sheet dimensions
        sheet_dims = layout_calculator.get_sheet_dimensions()

        # Create canvas with appropriate page size
        page_size = (sheet_dims.width_points, sheet_dims.height_points)
        c = canvas.Canvas(output_path, pagesize=page_size)

        # Calculate puzzle positions
        puzzle_positions = layout_calculator.compute_puzzle_positions()

        # Draw puzzles on the first page
        for i, puzzle in enumerate(puzzles):
            if i >= len(puzzle_positions):
                break

            position = puzzle_positions[i]
            self.sudoku_drawer.draw_sudoku_grid(
                c,
                puzzle.get_puzzle_grid(),
                position,
                position["width"],
                position["height"],
            )

        # Add page metadata
        self.add_page_metadata(c, sheet_dims, 1, include_solutions)

        # Show the first page
        c.showPage()

        # If solutions are requested, add solution pages
        if include_solutions:
            for i, puzzle in enumerate(puzzles):
                if i >= len(puzzle_positions):
                    break

                position = puzzle_positions[i]
                self.sudoku_drawer.draw_sudoku_grid(
                    c,
                    puzzle.get_solution_grid(),
                    position,
                    position["width"],
                    position["height"],
                )

            self.add_page_metadata(
                c, sheet_dims, 2, include_solutions, is_solution=True
            )
            c.showPage()

        c.save()
        print(f"PDF generated successfully: {output_path}")

    def add_page_metadata(
        self, canvas, sheet_dims, page_number, include_solutions, is_solution=False
    ):
        """Add page numbers, generation date, and other metadata."""
        font_size = 10
        canvas.setFont("Helvetica", font_size)

        # Page number
        page_text = f"Page {page_number}"
        if include_solutions and is_solution:
            page_text += " (Solutions)"

        canvas.drawRightString(sheet_dims.width_points - 20, 20, page_text)

        # Generation date and time
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        canvas.drawString(20, 20, f"Generated: {now}")

        # Sheet size information
        canvas.drawString(
            20, sheet_dims.height_points - 20, f"Sheet Size: {sheet_dims.sheet_size}"
        )
