import csv
import random
from datetime import datetime, timedelta
from pathlib import Path

# =========================
# SETTINGS
# =========================
OUTPUT_FOLDER = Path(r"C:\Users\ToriSeymour\OneDrive - Faria Online Schools\Documents\Projects\Power BI Student Engagement")
NUM_STUDENTS = 250
NUM_COURSES = 12
MIN_COURSES_PER_STUDENT = 2
MAX_COURSES_PER_STUDENT = 4
ASSIGNMENTS_PER_COURSE = 6
SEED = 42

random.seed(SEED)

# =========================
# LOOKUPS
# =========================
FIRST_NAMES = [
    "Amelia", "Noah", "Olivia", "George", "Isla", "Harry", "Ava", "Jack",
    "Mia", "Charlie", "Lily", "Oscar", "Sophia", "Leo", "Grace", "Arthur",
    "Freya", "Henry", "Evie", "Theo", "Ella", "Jacob", "Poppy", "Lucas",
    "Ruby", "Thomas", "Sophie", "Archie", "Emily", "William"
]

LAST_NAMES = [
    "Smith", "Jones", "Taylor", "Brown", "Williams", "Wilson", "Johnson",
    "Davies", "Patel", "Wright", "Walker", "Roberts", "Thompson", "White",
    "Hughes", "Edwards", "Green", "Hall", "Thomas", "Clarke"
]

SUBJECTS = [
    ("Business Management", "HL"),
    ("Business Management", "SL"),
    ("Psychology", "HL"),
    ("Psychology", "SL"),
    ("Economics", "HL"),
    ("Economics", "SL"),
    ("Digital Society", "HL"),
    ("Digital Society", "SL"),
    ("English Literature", "HL"),
    ("Mathematics", "SL"),
    ("Biology", "HL"),
    ("History", "SL"),
]

TEACHERS = [
    "A. Carter", "J. Singh", "L. Thompson", "R. Ahmed",
    "M. Evans", "S. Morgan", "D. Patel", "K. Brown"
]

COHORTS = ["M2026", "N2026", "M2027", "N2027"]

WORKFLOW_STATES = ["graded", "submitted", "unsubmitted", "missing"]
ENROLLMENT_STATES = ["active", "active", "active", "completed"]
SUBMISSION_STATUSES = ["submitted", "missing", "late", "excused"]

GRADE_BANDS = ["A", "B", "C", "D", "E"]
ER_BANDS = ["EE", "ME", "AE", "IE", "NE"]

# =========================
# HELPERS
# =========================
def make_email(first_name, last_name, student_number):
    clean_first = first_name.lower().replace(" ", "")
    clean_last = last_name.lower().replace(" ", "")
    return f"{clean_first}.{clean_last}{student_number}@example-school.org"

def random_date(start_date, end_date):
    delta = end_date - start_date
    random_days = random.randint(0, delta.days)
    return start_date + timedelta(days=random_days)

def format_dt(dt):
    return dt.strftime("%Y-%m-%d %H:%M:%S")

def generate_grade():
    weights = [0.12, 0.22, 0.30, 0.22, 0.14]
    return random.choices(GRADE_BANDS, weights=weights, k=1)[0]

def generate_engagement():
    weights = [0.10, 0.22, 0.30, 0.22, 0.16]
    return random.choices(ER_BANDS, weights=weights, k=1)[0]

def risk_score(grade, engagement, missing_count):
    score = 0

    if grade in ["D", "E"]:
        score += 2
    elif grade == "C":
        score += 1

    if engagement in ["IE", "NE"]:
        score += 2
    elif engagement == "AE":
        score += 1

    if missing_count >= 2:
        score += 2
    elif missing_count == 1:
        score += 1

    return score

def risk_label(score):
    if score >= 5:
        return "High"
    if score >= 3:
        return "Medium"
    return "Low"

# =========================
# OUTPUT SETUP
# =========================
OUTPUT_FOLDER.mkdir(parents=True, exist_ok=True)

students_file = OUTPUT_FOLDER / "students.csv"
courses_file = OUTPUT_FOLDER / "courses.csv"
enrollments_file = OUTPUT_FOLDER / "enrollments.csv"
submissions_file = OUTPUT_FOLDER / "submissions.csv"

# =========================
# BUILD COURSES
# =========================
courses = []
course_ids = []

for i in range(NUM_COURSES):
    course_id = 1000 + i
    subject, level = SUBJECTS[i % len(SUBJECTS)]
    cohort = random.choice(COHORTS)
    teacher = random.choice(TEACHERS)
    course_name = f"{cohort} {subject} {level} Y1"
    section_name = f"Class {random.randint(1, 3)} - {teacher}"
    courses.append({
        "course_id": course_id,
        "course_name": course_name,
        "subject": subject,
        "level": level,
        "cohort_code": cohort,
        "teacher_name": teacher,
        "section_name": section_name
    })
    course_ids.append(course_id)

# =========================
# BUILD STUDENTS
# =========================
students = []

for i in range(NUM_STUDENTS):
    student_id = 5000 + i
    student_number = 100000 + i
    first_name = random.choice(FIRST_NAMES)
    last_name = random.choice(LAST_NAMES)
    student_name = f"{first_name} {last_name}"
    student_email = make_email(first_name, last_name, student_number)

    students.append({
        "student_id": student_id,
        "student_number": student_number,
        "student_name": student_name,
        "student_email": student_email
    })

# =========================
# BUILD ENROLLMENTS
# =========================
enrollments = []
enrollment_id_counter = 1

term_start = datetime(2025, 8, 20)
term_end = datetime(2026, 5, 20)

for student in students:
    num_courses = random.randint(MIN_COURSES_PER_STUDENT, MAX_COURSES_PER_STUDENT)
    chosen_courses = random.sample(courses, num_courses)

    for course in chosen_courses:
        enrolled_on = random_date(term_start, term_start + timedelta(days=20))
        last_activity = random_date(enrolled_on, term_end)
        enrollment_state = random.choice(ENROLLMENT_STATES)

        enrollments.append({
            "enrollment_id": enrollment_id_counter,
            "student_id": student["student_id"],
            "student_name": student["student_name"],
            "student_email": student["student_email"],
            "course_id": course["course_id"],
            "course_name": course["course_name"],
            "subject": course["subject"],
            "level": course["level"],
            "cohort_code": course["cohort_code"],
            "section_name": course["section_name"],
            "teacher_name": course["teacher_name"],
            "enrolled_on": format_dt(enrolled_on),
            "last_activity": format_dt(last_activity),
            "enrollment_state": enrollment_state
        })
        enrollment_id_counter += 1

# =========================
# BUILD SUBMISSIONS
# =========================
submissions = []
submission_id_counter = 1

for enrollment in enrollments:
    missing_count = 0

    for assignment_num in range(1, ASSIGNMENTS_PER_COURSE + 1):
        due_at = term_start + timedelta(days=assignment_num * 21 + random.randint(-4, 4))
        points_possible = random.choice([10, 20, 25, 30, 40, 50])
        submission_status = random.choices(
            SUBMISSION_STATUSES,
            weights=[0.72, 0.12, 0.10, 0.06],
            k=1
        )[0]

        if submission_status == "missing":
            workflow_state = "missing"
            submitted_at = ""
            late = "True"
            missing = "True"
            excused = "False"
            grade = ""
            score = ""
            attempt = 0
            missing_count += 1
        elif submission_status == "excused":
            workflow_state = "unsubmitted"
            submitted_at = ""
            late = "False"
            missing = "False"
            excused = "True"
            grade = ""
            score = ""
            attempt = 0
        else:
            submitted_date = random_date(due_at - timedelta(days=5), due_at + timedelta(days=7))
            submitted_at = format_dt(submitted_date)
            late = "True" if submitted_date > due_at else "False"
            missing = "False"
            excused = "False"
            workflow_state = "graded" if random.random() < 0.85 else "submitted"
            grade = generate_grade()
            score_map = {"A": 0.92, "B": 0.82, "C": 0.70, "D": 0.58, "E": 0.42}
            base_score = points_possible * score_map[grade]
            variation = random.uniform(-2.5, 2.5)
            score = max(0, min(points_possible, round(base_score + variation, 1)))
            attempt = random.randint(1, 2)

        engagement_rating = generate_engagement()

        temp_grade_for_risk = grade if grade else random.choice(["C", "D", "E"])
        risk = risk_label(risk_score(temp_grade_for_risk, engagement_rating, missing_count))

        submissions.append({
            "submission_id": submission_id_counter,
            "student_id": enrollment["student_id"],
            "student_name": enrollment["student_name"],
            "student_email": enrollment["student_email"],
            "course_id": enrollment["course_id"],
            "course_name": enrollment["course_name"],
            "subject": enrollment["subject"],
            "cohort_code": enrollment["cohort_code"],
            "teacher_name": enrollment["teacher_name"],
            "assignment_name": f"Assignment {assignment_num}",
            "submission_status": submission_status,
            "workflow_state": workflow_state,
            "missing": missing,
            "late": late,
            "excused": excused,
            "grade": grade,
            "score": score,
            "attempt": attempt,
            "points_possible": points_possible,
            "due_at": format_dt(due_at),
            "submitted_at": submitted_at,
            "engagement_rating": engagement_rating,
            "risk_flag": risk
        })
        submission_id_counter += 1

# =========================
# WRITE CSVS
# =========================
def write_csv(file_path, rows):
    if not rows:
        return

    with open(file_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

write_csv(students_file, students)
write_csv(courses_file, courses)
write_csv(enrollments_file, enrollments)
write_csv(submissions_file, submissions)

print("Fake Canvas-style data created successfully.")
print(f"Folder: {OUTPUT_FOLDER.resolve()}")
print(f"Students: {len(students)}")
print(f"Courses: {len(courses)}")
print(f"Enrollments: {len(enrollments)}")
print(f"Submissions: {len(submissions)}")