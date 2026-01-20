import os
import json

# ------------------------------
# CONFIG: skill keywords to detect
# ------------------------------
SKILL_KEYWORDS = [
    "python", "c", "c++", "java", "git", "linux", "verilog", "vhdl",
    "fpga", "embedded", "rtos", "assembly", "matlab", "bash", "sql",
    "docker", "aws", "microcontroller", "uart", "spi", "i2c",
    "raspberry pi", "arduino", "microprocessor", "debugging",
    "oop", "object-oriented", "data structures", "algorithms"
]


# ------------------------------
# Load candidate profile (JSON)
# ------------------------------
def load_candidate_profile(path="candidate_profile.json"):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


# ------------------------------
# Load job postings from postings/
# ------------------------------
def load_postings(folder="postings"):
    postings = []
    if not os.path.exists(folder):
        print(f"ERROR: Folder '{folder}' not found.")
        print("Make sure you have a postings/ folder with .txt files inside.")
        return postings

    for filename in os.listdir(folder):
        if filename.endswith(".txt"):
            full_path = os.path.join(folder, filename)
            with open(full_path, "r", encoding="utf-8") as f:
                text = f.read().strip()

            # Skip empty posting files
            if not text:
                continue

            postings.append({"filename": filename, "text": text})

    return postings


# ------------------------------
# Simple "skill extraction" (keyword scan)
# ------------------------------
def basic_skill_finder(text):
    lower = text.lower()
    found = []

    for skill in SKILL_KEYWORDS:
        if skill in lower:
            found.append(skill)

    # Remove duplicates and sort
    return sorted(set(found))


# ------------------------------
# Extract simple "season/start date" hints (keyword scan)
# ------------------------------
def detect_season_and_startdate(text):
    lower = text.lower()

    season = "Unknown"
    start_date = "Unknown"

    # Season detection
    if "summer" in lower:
        season = "Summer"
    elif "fall" in lower:
        season = "Fall"
    elif "spring" in lower:
        season = "Spring"
    elif "winter" in lower:
        season = "Winter"

    # Year detection (basic)
    for year in ["2025", "2026", "2027", "2028"]:
        if year in lower and season != "Unknown":
            season = f"{season} {year}"
            break

    # Start date hints (very basic)
    for month in [
        "january", "february", "march", "april", "may", "june",
        "july", "august", "september", "october", "november", "december"
    ]:
        if month in lower:
            start_date = month.capitalize()
            # if a year is nearby, attach it
            for year in ["2025", "2026", "2027", "2028"]:
                if year in lower:
                    start_date = f"{month.capitalize()} {year}"
                    break
            break

    return season, start_date


# ------------------------------
# Score a posting vs candidate profile
# ------------------------------
def score_match(candidate, posting_skills):
    """
    Scoring idea:
    - More overlap with candidate skills = higher score
    - Missing skills listed (so you can see why)
    """
    candidate_skills = set([s.lower() for s in candidate.get("skills", [])])
    required = set([s.lower() for s in posting_skills])

    matched = required.intersection(candidate_skills)
    missing = required.difference(candidate_skills)

    if len(required) == 0:
        score = 0.5  # neutral if we extracted nothing
    else:
        score = len(matched) / len(required)

    qualified = (len(missing) == 0) and score >= 0.55

    return {
        "score": round(score, 3),
        "qualified": qualified,
        "matched_skills": sorted(list(matched)),
        "missing_skills": sorted(list(missing))
    }


# ------------------------------
# MAIN
# ------------------------------
def main():
    # Load candidate profile
    candidate = load_candidate_profile()

    # Load postings
    postings_raw = load_postings()

    if not postings_raw:
        print("No non-empty postings found in the postings/ folder.")
        print("Paste job posting text into postings/posting1.txt etc. then run again.")
        return

    results = []

    for post in postings_raw:
        print(f"\nScanning: {post['filename']} ...")

        posting_text = post["text"]
        posting_skills = basic_skill_finder(posting_text)
        season, start_date = detect_season_and_startdate(posting_text)

        match = score_match(candidate, posting_skills)

        results.append({
            "filename": post["filename"],
            "score": match["score"],
            "qualified": match["qualified"],
            "season": season,
            "start_date": start_date,
            "extracted_skills": posting_skills,
            "matched_skills": match["matched_skills"],
            "missing_skills": match["missing_skills"]
        })

    # Sort high to low
    results.sort(key=lambda x: x["score"], reverse=True)

    # Print ranked list
    print("\n\n===== RANKED INTERNSHIPS (NO-AI MODE) =====\n")

    for i, r in enumerate(results, 1):
        status = "✅ QUALIFIED" if r["qualified"] else "⚠️ NOT QUALIFIED"

        print(f"{i}) {r['filename']}  |  Score: {r['score']}  {status}")
        print(f"   Season: {r['season']} | Start Date: {r['start_date']}")
        print(f"   Matched Skills: {', '.join(r['matched_skills']) if r['matched_skills'] else 'None'}")
        print(f"   Missing Skills: {', '.join(r['missing_skills']) if r['missing_skills'] else 'None'}")
        print("-" * 60)

    # Save output to JSON
    with open("ranked_results.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)

    print("\nSaved results to: ranked_results.json")


if __name__ == "__main__":
    main()
