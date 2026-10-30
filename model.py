"""
model.py — Data definitions for JobLens.

Contains the JobApplication class, valid statuses, and status icons.
This module has no dependencies on persistence, business logic, or UI.
"""

from datetime import datetime


STATUSES = [
    "Applied",
    "Online Assessment",
    "Interview",
    "Offer",
    "Rejected"
]

# for a bit of personality, it looks too bland with just text
STATUS_ICONS = {
    "Applied": "\U0001f4dd",
    "Online Assessment": "\U0001f4bb",
    "Interview": "\U0001f4bc",
    "Offer": "\U0001f389",
    "Rejected": "\u274c"
}

class JobApplication:
    def __init__(self, id, company, role, location, date_applied, status , job_link, notes):
        self.id = id
        if not company or not role or not location:
            raise ValueError("Company, role, and location cannot be empty.") 
        self.company = company
        self.role = role
        self.location = location

        try:
            datetime.strptime(date_applied, "%Y-%m-%d")
        except ValueError:
            raise ValueError("Date must be in YYYY-MM-DD format.")
        self.date_applied = date_applied

        if status not in STATUSES:
            raise ValueError(f"Invalid status: {status}. Must be one of {STATUSES}")
        self.status = status
        self.job_link = job_link
        self.notes = notes

        
    def __str__(self):
        icon = STATUS_ICONS.get(self.status, "")
        return (
    # the comment with = below is to make it easier to see the table, below one is better for modification
    # f"\n========================================\n"
    f"{'-' * 18}\n"
    f"\U0001f4c4 Application #{self.id}\n"
    f"Company      : {self.company}\n"
    f"Role         : {self.role}\n"
    f"Location     : {self.location}\n"
    f"\nDate Applied : {self.date_applied}\n"
    f"Status       : {icon} {self.status}\n"

    f"\nJob Link     : {self.job_link}\n"

    f"\nNotes: \n{self.notes}\n"
    f"{'-' * 18}\n"
    # f"\n========================================\n"
    )
    
    def to_dict(self):
        return {
            "id": self.id,
            "company": self.company,
            "role": self.role,
            "location": self.location,
            "date_applied": self.date_applied,
            "status": self.status,
            "job_link": self.job_link,
            "notes": self.notes,
        }
    
    @classmethod
    def from_dict(cls, data):
        return cls(
            id=data["id"],
            company=data["company"],
            role=data["role"],
            location=data["location"],
            date_applied=data["date_applied"],
            status=data["status"],
            job_link=data["job_link"],
            notes=data["notes"]
        )
