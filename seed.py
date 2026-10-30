"""
seed.py — Import JSON data into PostgreSQL for JobLens.

Reads applications.json and skills.json, inserts rows into the DB,
preserves existing IDs, then resets sequences so the next auto-ID
doesn't collide.

Safety: refuses to run if the applications table already has rows.

Also contains the JSON load/save helpers relocated from repository.py
so that tests for those pure-JSON functions remain functional.
"""

import json
import os
import sys

from dotenv import load_dotenv
from sqlalchemy import create_engine, text

from model import JobApplication

load_dotenv()


# ── JSON helpers (moved from repository.py; tests still import them) ──


def save_json_file(filename, data):
    """Save a list of JobApplication objects to a JSON file."""
    with open(filename, "w") as file:
        obj = [item.to_dict() for item in data]
        json.dump(obj, file, indent=4)


def load_json_file(filename):
    """Load a list of JobApplication objects from a JSON file."""
    try:
        with open(filename, "r") as file:
            data = json.load(file)
            return [JobApplication.from_dict(item) for item in data]
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        print(f"Failed to decode JSON from {filename}.")
        return []


# ── Seeding logic ─────────────────────────────────────────────────────


def seed(database_url=None):
    """Seed PostgreSQL from the JSON files in the repo root."""
    url = database_url or os.environ.get("DATABASE_URL")
    if not url:
        print("ERROR: DATABASE_URL is not set.")
        sys.exit(1)

    engine = create_engine(url)

    with engine.begin() as conn:
        # Safety check
        count = conn.execute(text("SELECT COUNT(*) FROM applications")).scalar()
        if count > 0:
            print("ERROR: applications table already has rows. Aborting seed.")
            sys.exit(1)

        # ── Load JSON data ────────────────────────────────────────────
        with open("applications.json", "r", encoding="utf-8") as f:
            apps_data = json.load(f)

        with open("skills.json", "r", encoding="utf-8") as f:
            skills_data = json.load(f)

        # ── Insert applications ───────────────────────────────────────
        for app in apps_data:
            conn.execute(text(
                "INSERT INTO applications "
                "(id, user_id, company, role, location, date_applied, status, job_link, notes) "
                "VALUES (:id, 1, :company, :role, :location, :date_applied, :status, :job_link, :notes)"
            ), {
                "id": app["id"],
                "company": app["company"],
                "role": app["role"],
                "location": app["location"],
                "date_applied": app["date_applied"],
                "status": app["status"],
                "job_link": app["job_link"],
                "notes": app["notes"],
            })

        # Reset the applications id sequence
        conn.execute(text(
            "SELECT setval(pg_get_serial_sequence('applications', 'id'), "
            "(SELECT COALESCE(MAX(id), 0) FROM applications))"
        ))

        # ── Insert skills ─────────────────────────────────────────────
        for skill_name in skills_data:
            conn.execute(text(
                "INSERT INTO skills (name) VALUES (:name)"
            ), {"name": skill_name})

        # Reset the skills id sequence
        conn.execute(text(
            "SELECT setval(pg_get_serial_sequence('skills', 'id'), "
            "(SELECT COALESCE(MAX(id), 0) FROM skills))"
        ))

    # ── Verify ────────────────────────────────────────────────────────
    with engine.connect() as conn:
        app_count = conn.execute(text("SELECT COUNT(*) FROM applications")).scalar()
        skill_count = conn.execute(text("SELECT COUNT(*) FROM skills")).scalar()
        max_id = conn.execute(text("SELECT MAX(id) FROM applications")).scalar()

        print(f"Seeded {app_count} applications and {skill_count} skills.")
        print(f"Max application ID: {max_id}")

        # Verify IDs match
        db_ids = sorted([r[0] for r in conn.execute(text("SELECT id FROM applications")).fetchall()])
        json_ids = sorted([a["id"] for a in apps_data])
        assert db_ids == json_ids, f"ID mismatch: DB={db_ids}, JSON={json_ids}"

        # Verify next insert gets max(id)+1
        next_val = conn.execute(text(
            "SELECT nextval(pg_get_serial_sequence('applications', 'id'))"
        )).scalar()
        assert next_val == max_id + 1, f"Sequence not reset: next={next_val}, expected={max_id + 1}"

        # Reset sequence back (nextval consumed one)
        conn.execute(text(
            "SELECT setval(pg_get_serial_sequence('applications', 'id'), :max_id)"
        ), {"max_id": max_id})
        conn.commit()

        print(f"Next auto ID will be: {max_id + 1}")
        print("All verifications passed.")

    engine.dispose()


if __name__ == "__main__":
    seed()
