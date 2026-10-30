"""
repository.py — JSON persistence for JobLens.

Isolates all file I/O behind a clear boundary. The rest of the app
never opens applications.json or skills.json directly.

File-path constants are read at call time (not as default arguments)
so tests can monkeypatch them.
"""

import json
from model import JobApplication
from ui import print_error  # transitional: presentation dependency in persistence layer


APPLICATIONS_FILE = "applications.json"
SKILLS_FILE = "skills.json"


# ── Generic helpers (used by tests with arbitrary tmp_path files) ─────

def save_json_file(filename, data):
    with open(filename, "w") as file:
        obj = [item.to_dict() for item in data]
        json.dump(obj, file, indent=4)


def load_json_file(filename):
    try:
        with open(filename, "r") as file:
            data = json.load(file)
            return [JobApplication.from_dict(item) for item in data]
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        print_error(f"Failed to decode JSON from {filename}.")
        return []


# ── Application-specific wrappers (read path constant at call time) ──

def load_applications():
    """Load all applications from the configured JSON file."""
    return load_json_file(APPLICATIONS_FILE)


def save_applications(applications):
    """Save all applications to the configured JSON file."""
    save_json_file(APPLICATIONS_FILE, applications)


def load_skills():
    """Load the skills list from the configured JSON file."""
    with open(SKILLS_FILE, "r", encoding="utf-8") as file:
        skills = json.load(file)

    stored_skills = set(skills)
    return stored_skills
