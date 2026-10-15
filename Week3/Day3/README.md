# Week 3 · Day 3 — Student Data ETL Pipeline with n8n

## Overview

This project demonstrates how to build an ETL (Extract, Transform, Load) workflow in **n8n** to process student enrollment data from a CSV file. The workflow reads the source data, standardizes fields, removes duplicate email records, separates records by fee-payment status, and writes the results to CSV files.

## Objectives

- Read student enrollment data from a CSV file.
- Clean and normalize student information using JavaScript.
- Remove duplicate records based on email.
- Filter students by fee-payment status.
- Export the results to separate CSV files.
- Verify workflow execution by inspecting node status and item counts.

## Workflow

1. **Manual Trigger** — starts the workflow when executed manually.
2. **Read/Write Files from Disk** — reads the input CSV file.
3. **Extract from File** — converts the CSV into n8n JSON items.
4. **Code in JavaScript** — cleans and standardizes student fields.
5. **Remove Duplicates** — checks records using the email field.
6. **Filter — Paid Students** — keeps records where `Fee_Paid = yes`.
7. **Convert to File** — converts the paid records back to CSV.
8. **Read/Write Files from Disk** — writes `students_clean.csv`.
9. **Filter1 — Review Records** — keeps records where `Fee_Paid != yes`.
10. **Convert to File1** — converts the review records back to CSV.
11. **Read/Write Files from Disk2** — writes `students_review.csv`.

## Data Transformation

The JavaScript Code node performs these operations:

- Trims whitespace and collapses repeated spaces.
- Converts student names and city names to title case.
- Converts email addresses to lowercase.
- Standardizes course names, including `ML` to `Machine Learning`.
- Converts recognized enrollment dates to `YYYY-MM-DD`.
- Normalizes `Fee_Paid` to lowercase.

## Input and Outputs

### Input

Place the source file at:

`data/students.csv`

Expected columns:

- `Student_ID`
- `Name`
- `Email`
- `Phone`
- `Course`
- `Fee_Paid`
- `City`
- `Enrolled_Date`

### Output files

The workflow is configured to save output files in the project's `data` directory:

- `data/students_clean.csv` — records where `Fee_Paid = yes`.
- `data/students_review.csv` — records where `Fee_Paid != yes`.

> The review file is based on fee-payment status. It does not automatically mean the records contain invalid data.

## Results

The source file contains 50 records. The workflow's observed item counts were:

| Stage | Records |
|---|---:|
| Input CSV | 50 |
| After JavaScript cleaning | 50 |
| After duplicate removal | 50 |
| Fee paid (`yes`) | 33 |
| Fee not paid `yes` | 17 |
| Total across both branches | 50 |

The counts indicate that no records were removed by the duplicate-removal node in the observed run. Verify that both output files are successfully written after executing the complete workflow.

## Running the Workflow

1. Start n8n.
2. Open the `Week3-Day3-Student-ETL` workflow.
3. Confirm that `data/students.csv` exists and the file paths in the disk nodes match your local project directory.
4. Click **Save**.
5. Click **Execute Workflow** to run it manually.
6. Check that all nodes complete successfully.
7. Confirm that both `students_clean.csv` and `students_review.csv` exist in the `data` directory.

The Manual Trigger is sufficient for running this assignment on demand. You do not need to publish or activate the workflow for manual execution.

## Troubleshooting

- **File access error:** Ensure n8n is allowed to access the project `data` directory. If using `N8N_RESTRICT_FILE_ACCESS_TO`, include the intended directory and restart n8n.
- **Missing output file:** Check the Write File to Disk node's full path and ensure its **Input Binary Field** matches the binary field produced by Convert to File (typically `data`).
- **Unexpected item counts:** Inspect the Filter node's **Kept** and **Discarded** outputs and confirm the condition is configured correctly.
- **Workflow publish/activation error:** Use **Execute Workflow** for manual runs. A Manual Trigger does not need activation to run on demand.
- **Duplicate count unchanged:** This may mean there are no duplicates under the selected email comparison, or the node is not configured to compare the intended field.

## Key Learnings

- ETL separates extraction, transformation, and loading into clear stages.
- n8n passes records between nodes as JSON items.
- CSV files can be converted into JSON for processing and back into CSV for export.
- JavaScript can normalize inconsistent data before analysis.
- Filters can route records into separate processing branches.
- Item counts and node execution indicators help validate a workflow.
- Local file permissions and correct binary-field settings are important when writing files.

## Possible Improvements

- Validate email formats and route missing or invalid emails to a dedicated review output.
- Add a summary node or report showing totals, paid records, unpaid records, and invalid records.
- Add duplicate detection based on multiple fields when email is missing.
- Add automated scheduling only if the assignment requires recurring execution.
- Keep API keys and other secrets out of source control if future nodes use credentials.

## Project Status

The main workflow and two filtering branches have been configured. Before considering the assignment complete, execute the full workflow and verify that both output CSV files are written successfully.
