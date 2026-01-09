import argparse
import sys
from .constants import PAPER_SIZES, DIFFICULTY_SETTINGS
from .generator import PuzzleGenerator
from .layout import LayoutCalculator
from .renderer import PDFGenerator


class CLIInterface:
    """Handles command-line argument parsing and validation."""

    def __init__(self):
        self.parser = argparse.ArgumentParser(
            description="OpenSudoku - Generate customizable Sudoku puzzle sheets in PDF format"
        )
        self._setup_arguments()

    def _setup_arguments(self):
        """Set up command-line arguments."""
        # Difficulty level
        self.parser.add_argument(
            "--difficulty",
            choices=list(DIFFICULTY_SETTINGS.keys()),
            default="medium",
            help="Difficulty level: easy, medium, my-mom, hard",
        )

        # Sheet size
        self.parser.add_argument(
            "--sheet-size",
            choices=list(PAPER_SIZES.keys()),
            default="A4",
            help="Paper size: A1, A2, A3, A4, A5",
        )

        # Number of pages
        self.parser.add_argument(
            "--pages", type=int, default=1, help="Number of pages to generate"
        )

        # Puzzles per page
        self.parser.add_argument(
            "--puzzles-per-page",
            type=int,
            default=4,
            help="Number of Sudoku puzzles per page",
        )

        # Puzzle spacing
        self.parser.add_argument(
            "--spacing",
            type=float,
            default=None,
            help="Spacing between puzzles in mm (default: 5mm)",
        )

        # Output file
        self.parser.add_argument(
            "--output", default="sudoku_puzzles.pdf", help="Output PDF filename"
        )

        # Include solutions
        self.parser.add_argument(
            "--solutions", action="store_true", help="Include solution pages in the PDF"
        )

    def parse_arguments(self):
        """Parse command-line arguments."""
        return self.parser.parse_args()

    def validate_inputs(self, args):
        """Validate user input parameters."""
        errors = []

        # Validate pages
        if args.pages < 1:
            errors.append("Number of pages must be at least 1")

        # Validate puzzles per page
        if args.puzzles_per_page < 1:
            errors.append("Number of puzzles per page must be at least 1")

        # Check if puzzles per page is reasonable for sheet size
        layout_calc = LayoutCalculator(args.sheet_size, args.puzzles_per_page)
        max_puzzles = layout_calc.get_max_puzzles_for_sheet()

        if args.puzzles_per_page > max_puzzles:
            errors.append(
                f"Too many puzzles for {args.sheet_size} sheet. "
                f"Maximum recommended: {max_puzzles}"
            )

        if errors:
            print("Input validation errors:")
            for error in errors:
                print(f"  - {error}")
            sys.exit(1)

        return True


class ApplicationController:
    """Orchestrates the entire puzzle generation and PDF creation process."""

    def __init__(self):
        self.cli = CLIInterface()
        self.puzzle_generator = PuzzleGenerator()
        self.pdf_generator = PDFGenerator()

    def run(self):
        """Main application entry point."""
        # Parse and validate arguments
        args = self.cli.parse_arguments()
        self.cli.validate_inputs(args)

        print("Generating Sudoku puzzles with settings:")
        print(f"  Difficulty: {args.difficulty}")
        print(f"  Sheet size: {args.sheet_size}")
        print(f"  Pages: {args.pages}")
        print(f"  Puzzles per page: {args.puzzles_per_page}")
        print(
            f"  Spacing: {args.spacing if args.spacing is not None else 'default (5mm)'}"
        )
        print(f"  Output file: {args.output}")
        print(f"  Include solutions: {args.solutions}")

        # Generate puzzles
        total_puzzles = args.pages * args.puzzles_per_page
        print(f"\nGenerating {total_puzzles} puzzles...")

        puzzles = self.puzzle_generator.generate_multiple_puzzles(
            total_puzzles, args.difficulty
        )

        print(f"Generated {len(puzzles)} puzzles successfully")

        # Calculate layout
        layout_calc = LayoutCalculator(
            args.sheet_size, args.puzzles_per_page, args.spacing
        )

        # Generate PDF
        print("Creating PDF...")
        self.pdf_generator.create_pdf(
            puzzles[: args.puzzles_per_page],  # First page only for now
            layout_calc,
            args.output,
            args.solutions,
        )

        print("Done!")
