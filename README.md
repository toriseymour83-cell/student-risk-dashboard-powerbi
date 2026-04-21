# Student Risk Dashboard in Power BI

## Overview
This project is a Power BI dashboard built using fake Canvas-style student data. It is designed to identify at-risk students, monitor grades and engagement, and support cohort and subject-level analysis.

## Project Aim
The aim of this dashboard is to help staff answer a simple question:

**Which students are most at risk, and where should attention be focused first?**

## Files Included
- `student-risk-dashboard-powerbi.pbix`
- `students.csv`
- `courses.csv`
- `enrollments.csv`
- `submissions.csv`

## Dashboard Pages

### 1. Overview
This page gives a summary of:
- total students
- at-risk students
- average score
- missing submissions
- late submissions
- high risk percentage
- at-risk students by subject
- at-risk students by cohort

It also includes filters for:
- risk flag
- cohort
- subject
- teacher

### 2. Student Detail
This page allows a single student to be selected and shows:
- average score
- missing submissions
- late submissions
- high risk percentage
- assignment-level performance
- assignment status and risk flags

## Data Model
The dashboard uses four main tables:
- **students**
- **courses**
- **enrollments**
- **submissions**

Relationships were created using:
- `student_id`
- `course_id`

## Key Measures
Examples of DAX measures used:
- `Total Students`
- `At Risk Students`
- `Average Score`
- `Missing Submissions`
- `Late Submissions`
- `High Risk Rate`

## Skills Demonstrated
This project demonstrates:
- Power BI data modelling
- Power Query transformation
- DAX measures
- dashboard design
- data visualisation
- education data analysis

## Notes
This project uses fake data created for portfolio purposes and does not contain any real student information.
