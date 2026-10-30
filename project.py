"""
project.py — Entry point for JobLens CLI.

Preserves 'python project.py' as the start command.
All logic lives in cli.py, service.py, repository.py, model.py, and matcher.py.
"""

from cli import main

if __name__ == "__main__":
    main()