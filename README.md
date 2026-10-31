# JobLens v3

#### Video Demo: https://youtu.be/Oa-S7ZLmMcs?si=NcJKvpjNyIFh-O6P

**v3** - New version which will use a database and FastAPI, will be a Full stack app
<!-- TODO: Re-record demo video to show the updated Rich terminal UI -->
**v2** — Enhanced with a Rich-powered terminal UI after course submission.


#### Description

JobLens v3 is the new updated version of the command-line job application tracker built with Python as my final project for CS50’s Introduction to Programming with Python (CS50P).

This will be in the web and anyone can use it. I just felt the need to update it because as much as i like the CLI, this one would feel much better and would be a great learning experience in my opinion.

I created this project because keeping track of my own job applications, interview stages, and job links became difficult. JobLens allows users to store and manage job applications, search existing records, view application statistics, and compare their resume with a job description using a simple resume matcher.

My goal was to build a practical application that combines object-oriented programming, JSON file handling, testing with `pytest`, and modular Python design into a project that I can continue using and improving even after completing CS50P.


## Screenshots

COMING SOON

## Features

### Add Applications

Users can store information about job applications, including:

* Company name
* Job role
* Location
* Date applied
* Current application status
* Job link
* Notes

Each application is assigned a unique ID for easy management.

### View Applications

All saved applications are displayed in a formatted table, allowing users to quickly review their job search progress. There's also a detailed view that shows all the details.

### Update Status

Users can update the status of an existing application. Supported statuses include:

* Applied
* Online Assessment
* Interview
* Offer
* Rejected

Input validation ensures that only valid statuses are accepted.

### Delete Applications

Applications can be removed using their unique ID.

### Search

Users can search applications by company, role, location, or status, making it easier to find specific records.

### Resume Matcher

One of the main features of JobLens is its resume matcher.

The program extracts text from a PDF resume using the pypdf library. It compares the skills found in the resume with skills detected from the provided job description and generates a simple match report.

The matcher displays:

* Match percentage
* Matching skills
* Missing skills

This provides a quick estimate of how closely a resume aligns with a job posting.

### Statistics

JobLens generates statistics showing how applications are distributed across different stages of the hiring process.

Statistics include:

* Total applications
* Count for each application status
* Percentage breakdown
* Terminal-based bar chart

### Visualization

In addition to terminal statistics, JobLens can generate a bar chart using Matplotlib, providing a visual summary of application progress. The chart is also saved in the charts folder if you want to view it later, the program will create a new charts folder if it does not already exist when used the Statistics/Generate Applications by Status Chart.


## Project Structure

```
project/
│
├── project.py
├── resume_matcher.py
├── ui.py
├── test_project.py
├── applications.json
├── skills.json
├── requirements.txt
├── README.md
└── resume/
    └── NILESH_CHIDAMBARAM_Resume.pdf
```


## Testing

The project includes automated tests written with `pytest`. Instead of testing the interactive menu, I focused on testing the core logic of the application.

The test suite covers:

* Creating `JobApplication` objects
* Input validation
* Serialization with `to_dict()` and `from_dict()`
* JSON file loading and saving

Testing the application's core functionality helped ensure that the most important parts of the project work correctly and continue to behave as expected after making changes.


## Libraries Used

### Standard Library

* os
* json
* sys
* datetime

### Third-Party Libraries

* pypdf
* matplotlib
* rich (used for terminal rendering)
* pytest (used for testing)
* (MORE COMING SOON)


## Future Improvements

Although JobLens is complete, there are several possible enhancements, namely a few I think I'll do:

* Smarter skill matching using aliases and synonyms.
* Keyword extraction instead of exact text matching.
* Resume ranking against multiple job descriptions.
* CSV import/export.
* Database support using SQLite.
* A graphical user interface.
* Maybe an actual application.

## Updates

**V3** - Latest version: web

**v2** — Upgraded the terminal interface using the Rich library
(bordered panels, tables, color-coded statuses, styled prompts).
Also fixed two minor bugs found during this
pass: search by location/status was incorrectly matching on role,
and the resume matcher only read the last page of multi-page PDFs.

**v1** — Original CS50P submission.

