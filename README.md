# Internship Matcher (Python)

A lightweight Python tool that scans internship job postings and ranks them based on a student candidate’s skills and availability.

This project is designed as a portfolio-friendly MVP that demonstrates practical parsing, matching logic, and clean repo structure.

---

## ✅ Features
- Loads a candidate profile from JSON
- Scans job posting text files in `postings/`
- Extracts skills using keyword detection (no AI required)
- Ranks postings by best match score
- Shows matched vs missing skills for each posting
- Saves ranked results to `ranked_results.json`

---

## 📁 Project Structure
```txt
internship_matcher/
  main.py
  README.md
  requirements.txt
  candidate_profile.sample.json
  postings/
    sample_posting.txt
