# Internship Matcher (MVP)

A Python tool that scans internship job postings and ranks them based on a student's skills and availability.

## Features
- Reads job postings from `postings/*.txt`
- Loads candidate info from `candidate_profile.json`
- Extracts skills using keyword detection
- Scores and ranks postings by best fit
- Shows matched vs missing skills
- Outputs results to `ranked_results.json`

## How to Run

### 1) Activate virtual environment
```bash
source venv/bin/activate

