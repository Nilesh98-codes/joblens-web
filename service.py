"""
service.py — Business logic for JobLens.

Pure operations on application data. No terminal I/O, no Rich, no
input(). This module calls repository for persistence and model for
data definitions.
"""

from model import JobApplication, STATUSES
from repository import load_applications, save_applications


def add_application(company, role, location, date_applied, status, job_link, notes):
    """
    Create and persist a new application.

    Returns the created JobApplication.
    Raises ValueError on validation failure (from JobApplication.__init__).
    """
    applications = load_applications()
    if applications:
        next_id = max(app.id for app in applications) + 1
    else:
        next_id = 1

    application = JobApplication(
        id=next_id,
        company=company,
        role=role,
        location=location,
        date_applied=date_applied,
        status=status,
        job_link=job_link,
        notes=notes
    )
    applications.append(application)
    save_applications(applications)
    return application


def get_all_applications():
    """Return all applications as a list of JobApplication objects."""
    return load_applications()


def get_application_by_id(app_id):
    """Return a single application by ID, or None if not found."""
    applications = load_applications()
    return next((app for app in applications if app.id == app_id), None)


def update_application_status(app_id, new_status):
    """
    Update the status of an application.

    Returns True if the application was found and updated, False if not found.
    """
    applications = load_applications()

    for app in applications:
        if app_id == app.id:
            app.status = new_status
            save_applications(applications)
            return True

    return False


def delete_application(app_id):
    """
    Delete an application by ID.

    Returns True if found and deleted, False if not found.
    """
    applications = load_applications()

    for app in applications:
        if app_id == app.id:
            applications.remove(app)
            save_applications(applications)
            return True

    return False


def search_applications(field, query):
    """
    Search applications by field using startswith matching.

    field: one of "company", "role", "location", "status"
    query: the search string (will be compared case-insensitively)

    Returns a list of matching JobApplication objects.
    """
    applications = load_applications()
    results = []
    query_lower = query.lower()

    for app in applications:
        value = getattr(app, field, "")
        if value.lower().startswith(query_lower):
            results.append(app)

    return results


def compute_statistics():
    """
    Compute application statistics.

    Returns (track, total) where:
    - track: dict mapping each status to its count
    - total: total number of applications
    """
    applications = load_applications()

    # build tracking dictionary dynamically
    track = {status: 0 for status in STATUSES}

    # count each status
    for app in applications:
        if app.status in track:
            track[app.status] += 1

    total = len(applications)
    return track, total
