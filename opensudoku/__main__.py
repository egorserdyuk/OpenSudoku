#!/usr/bin/env python3
"""Main entry point for OpenSudoku CLI application."""

from .cli import ApplicationController

if __name__ == "__main__":
    app = ApplicationController()
    app.run()
