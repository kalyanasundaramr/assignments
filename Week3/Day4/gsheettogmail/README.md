# Assignment 9 – n8n Automation: Google Sheets to Gmail

## Overview

This project automates reading student records from Google Sheets, formatting each record into a readable email, and sending the email through Gmail using n8n.

## Workflow

Manual Trigger → Google Sheets → IF → Edit Fields → Gmail

## Nodes Used

1. **Manual Trigger** – Starts the workflow manually.
2. **Google Sheets** – Reads student records from the `Students` worksheet.
3. **IF** – Checks whether the student's name is not empty.
4. **Edit Fields** – Creates the email subject and formatted message body.
5. **Gmail** – Sends the email to the configured recipient.

## Sample Data

The Google Sheet contains the following columns:

- Name
- Course
- Status

Example records include Python, Machine Learning, and Data Analytics courses.

## Email Format

**Subject:** Student Data Summary - Assignment 9

**Body:**

Hi,

Here is the latest student data from Google Sheets:

- Name: Student Name
- Course: Course Name
- Status: Enrollment Status

Regards,  
Your Automation Bot

## Validation

- Successfully retrieved three student records from Google Sheets.
- Successfully generated formatted email content.
- Successfully sent and received three emails.
- Verified that records with an empty name are routed to the IF node's false output.

**Limitation:** Handling a completely empty Google Sheet requires additional validation because the Google Sheets node may return zero items.

## Security

Credentials are managed through n8n credentials. No passwords, API tokens, or OAuth secrets should be committed to GitHub.

## How to Run

1. Import the workflow JSON into n8n.
2. Connect your own Google Sheets and Gmail credentials.
3. Select your spreadsheet and worksheet.
4. Configure the recipient email address.
5. Execute the workflow and verify the received emails.

## Deliverables

- Exported n8n workflow JSON
- This README file
- Working demonstration video shared with the course community
