"""
cli.py — CLI interaction layer for JobLens.

Handles menus, user input/output, and terminal presentation.
Calls service.py for business logic, matcher.py for resume matching,
and ui.py for Rich rendering.
"""

import os
from matplotlib import pyplot as plt

from model import STATUSES, STATUS_ICONS
from repository import load_skills
import service
from matcher import extract_pdf_text, match_resume, format_skill
from ui import (
    console, prompt, wait_for_enter,
    print_success, print_error, print_warning, print_info,
    print_welcome, print_main_menu, print_exit,
    print_app_table, print_app_detail,
    print_section_header, print_status_select,
    print_search_menu, print_statistics_menu,
    print_statistics_dashboard,
    print_resume_report,
    STATUS_STYLE,
)


# ── Resume PDF path constant ─────────────────────────────────────────
RESUME_PDF_PATH = "resume/NILESH_CHIDAMBARAM_Resume.pdf"


def main():

    while True:
        print_welcome()
        print_main_menu()

        option = prompt("Enter your choice (1-8)")


        # new application
        if option == "1":
            add_application()
            
        elif option == "2":
            view_application()

        elif option == "3":
            update_status()

        elif option == "4":
            delete_application()
           
        elif option == "5":
            search_application()
            
        elif option == "6":
            show_statistics()

        elif option == "7":
            run_resume_matcher()

        elif option == "8" or option == "q" or option == "Q":
            # just break out of the loop
            print_exit()
            break


def add_application():
    print_section_header("Add Application")

    company = prompt("Enter company name").title().strip()
    role = prompt("Enter role").title().strip()
    location = prompt("Enter location").title().strip()
    date_applied = prompt("Enter date applied (YYYY-MM-DD)")
    status = prompt("Enter status (Applied, Online Assessment, Interview, Offer, Rejected)").strip().title()
    job_link = prompt("Enter job link")
    notes = prompt("Enter notes").strip()

    try: 
        service.add_application(
            company=company,
            role=role,
            location=location,
            date_applied=date_applied,
            status=status,
            job_link=job_link,
            notes=notes
        )
        print_success("Application added successfully!")

    except ValueError as e:
        print_error(str(e))
    
    wait_for_enter()


def view_application():
    applications = service.get_all_applications()
    if not applications:
        print_warning("No applications found")
        return
    
    # the short list of jobs will show here
    print_section_header("View Applications")
    print_app_table(applications)

    # Prompt user for detailed view
    try:
        choose = int(prompt("Enter application ID to view details"))
    except ValueError:
        print_error("Invalid input. Please enter a valid numerical ID.")
    else:
        console.print()
        # this will show a detailed window of the application
        matched_app = next((app for app in applications if app.id == choose), None)
        
        if matched_app:
            print_app_detail(matched_app)
        else:
            print_warning("Application not found")

    # Go back to menu
    wait_for_enter()


def update_status():
    applications = service.get_all_applications()
    if not applications:
            print_warning("No applications found")
            return
        
    # the short view of job applications
    print_section_header("Update Status")
    print_app_table(applications)

    update = int(prompt("Enter application ID to update"))
    found = False

    for app in applications:
        icon = STATUS_ICONS.get(app.status)
        if update == app.id:
            found = True
            style = STATUS_STYLE.get(app.status, "white")
            print_info(f"Current Status: [{style}]{icon} {app.status}[/]")

            print_status_select(STATUSES)

            try:
                choice = int(prompt("Choice"))

                # Validate the user's input
                if 1 <= choice <= len(STATUSES):
                    selected_status = STATUSES[choice - 1]
                    service.update_application_status(app.id, selected_status)
                    print_success(f"Successfully updated status to: {selected_status}")
                    return 
                else:
                    print_error("Invalid choice. Please enter a number from the list.")
            except ValueError:
                print_error("Invalid input. Please enter a valid number.")
            wait_for_enter()
            
    if not found:
        print_warning("Application not found")
        wait_for_enter()
        return

def delete_application():
    applications = service.get_all_applications()
    if not applications:
            print_warning("No applications found")
            return
        
    # the short view of job applications
    print_section_header("Delete Application")
    print_app_table(applications)

    try:
        delete = int(prompt("Enter application ID to delete"))
        deleted = service.delete_application(delete)
        if deleted:
            print_success("Application successfully deleted")
            return 
        print_warning("Application does not exist")

    except ValueError:
            print_error("Invalid input. Please enter a valid number.")

    
def search_application():
    while True:

        print_section_header("Search Applications")
        print_search_menu()

        choice = prompt("Enter choice")
        if choice == "1":
            print_section_header("Search By Company")

            search_company = prompt("Enter Company").lower()
            results = service.search_applications("company", search_company)
            if results:
                for app in results:
                    print_app_detail(app)
            else:
                print_warning("Company not found")

        if choice == "2":
            print_section_header("Search by Role")

            search_role = prompt("Enter Role").lower()
            results = service.search_applications("role", search_role)
            if results:
                for app in results:
                    print_app_detail(app)
            else:
                print_warning("Role not found")
            
        if choice == "3":
            print_section_header("Search by Location")
            
            search_location = prompt("Enter Location").lower()
            results = service.search_applications("location", search_location)
            if results:
                for app in results:
                    print_app_detail(app)
            else:
                print_warning("Applications in given location not found")

        if choice == "4":
            print_section_header("Search by Status")
            
            search_status = prompt("Enter Status").lower()
            results = service.search_applications("status", search_status)
            if results:
                for app in results:
                    print_app_detail(app)
            else:
                print_warning("Status not found")
        if choice == "5":
            break
                

def show_statistics():
    track, total = service.compute_statistics()

    print_section_header("Statistics")
    print_statistics_menu()
    
    try:
        choice = int(prompt("Enter your choice"))
    except ValueError:
        print_error("Invalid input. Please enter a valid number.")
        return

    # FOR THE TERMINAL STATS
    if 1 <= choice <= 3 and choice == 1:
        print_statistics_dashboard(track, total)
        wait_for_enter()
    

    # FOR THE VISUAL CHART
    elif 1 <= choice <= 3 and choice == 2:
        generate_chart(track)


def generate_chart(track):
    """Generate and save a matplotlib bar chart of application statistics."""

    # remove statuses with 0 applications
    filtered = {}
    for status, count in track.items():
        if count > 0:
            filtered[status] = count

    statuses = list(filtered.keys())
    counts = list(filtered.values())

    # consistent colors for each status
    status_colors = {
        "Applied": "#42A5F5",             
        "Online Assessment": "#FFCA28",   
        "Interview": "#AB47BC",           
        "Offer": "#66BB6A",               
        "Rejected": "#EF5350"             
    }

    # store the colors of each status so that each status bar has its appropiate color
    colors = []
    for status in statuses:
        colors.append(status_colors[status])

    plt.figure(figsize=(7, 5))

    bars = plt.bar(
        statuses,
        counts,
        width=0.25,
        color=colors,
        edgecolor="black",
        linewidth=1
    )

    plt.title("JobLens - Application Statistics", fontsize=18)
    plt.xlabel("Application Status", fontsize=12)
    plt.ylabel("Applications", fontsize=12)

    # light grid
    plt.grid(axis="y", linestyle="--", alpha=0.25)

    # add some headroom
    plt.ylim(0, max(counts) + 0.7)

    # display values above bars
    for bar in bars:
        height = bar.get_height()
        plt.text(
            bar.get_x() + bar.get_width() / 2,
            height + 0.05,
            str(int(height)),
            ha="center",
            va="bottom",
            fontsize=11,
            fontweight="bold"
        )

    # a bit of slight rotation looks cleaner, neat right?
    plt.xticks(rotation=10)

    plt.tight_layout()

    os.makedirs("charts", exist_ok=True)
    plt.savefig("charts/job_statistics.png", dpi=300)
    plt.show()
    print_info("Chart saved as charts/job_statistics.png")


def run_resume_matcher():
    """CLI handler for the resume matcher feature."""
    resume_text = extract_pdf_text(RESUME_PDF_PATH)
    skills = load_skills()

    print_section_header("Resume Matcher")
    job_desc = prompt("Paste Job Description")

    result = match_resume(resume_text, job_desc, skills)

    print_resume_report(
        result["score"],
        result["matched"],
        result["missing"],
        result["jd_skills"],
        format_skill,
    )

    wait_for_enter()
