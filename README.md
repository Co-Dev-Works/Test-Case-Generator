-> TEST CASE GENERATOR

A lightweight web-based tool that automatically generates test cases (valid + invalid inputs) for form fields like email, username, password, phone number, etc.
Built with Flask + Python, it helps developers and testers quickly produce structured test cases and export them in CSV, JSON, and XLSX formats.


-> PROBLEM IT SOLVES:
Manually creating test cases for form validation is repetitive, time-consuming, and error-prone.
Developers often miss edge cases like:

* Empty inputs
* Special characters
* Extra-long strings
* Unicode characters
* Invalid formats
* Random garbage input

This leads to missed bugs and inconsistent testing.
This project automates that process, generating dozens of meaningful test inputs instantly.


-> FEATURES:

 * Automated Test Case Generation

   Enter a high-level requirement like:
   Email field must be valid and 6–40 chars.


   The tool generates:
   Valid emails
   Invalid emails (missing '@', too long, special symbols, spaces, unicode, etc.)
   Edge cases (".", " ", null-like strings, etc.)


  * Pretty Web UI (Flask + Bootstrap)
    
     Simple, responsive input form
     Results page shows all generated cases
     Dashboard view with priority distribution

  * Export Options

   Download test cases in:
   CSV
   JSON
   XLSX

 
 * Requirement-Aware Metadata

  Every output includes:
  Title
  Category
  Estimated severity
  Priority (High/Medium/Low)


-> TECH STACK:

Python 3
Flask
HTML / CSS (Bootstrap)
Pandas + OpenPyXL (for exporting files)


-> HOW IT WORKS:

Enter your requirement in the text box (e.g., "Username: 5–15 chars, alphanumeric only").
Choose how many test cases to generate.
Click Generate.
View or download test cases instantly.

-> SCREENSHORTS:

<img width="951" height="449" alt="Screenshot 2025-11-19 200045" src="https://github.com/user-attachments/assets/00107b68-e734-4a2c-949d-5929d0b4a65f" />

<img width="952" height="466" alt="Screenshot 2025-11-19 200122" src="https://github.com/user-attachments/assets/4705188b-4943-43d5-82b0-81c7c47e5187" />

<img width="947" height="449" alt="Screenshot 2025-11-19 200151" src="https://github.com/user-attachments/assets/123287b9-0885-4b65-86c6-3f2ce8b95989" />


-> PROJECT STRUCTURE:

/project
 ├── app.py
 ├── generator.py
 ├── model.py              
 ├── exporter.py
 ├── templates/
 │    ├── index.html
 │    ├── results.html
 │    ├── dashboard.html
 │    └── documentation.html
 └── static/
      └── styles.css

-> RUN COMMAND:

python app.py


      
