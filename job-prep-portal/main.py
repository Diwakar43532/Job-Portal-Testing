from fastapi import FastAPI, HTTPException, Query
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
import sqlite3
import json
import os
from datetime import datetime

from database import DB_PATH, get_db, init_db
from seed_data import seed_database

app = FastAPI(title="Job Portal & Tech Preparation Hub", version="2.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic schemas
class JobCreate(BaseModel):
    title: str
    company: str
    company_logo: Optional[str] = "briefcase"
    location: str
    job_type: str = "Full-time"
    experience: str = "0-2 years"
    salary: str = "₹12 - ₹18 LPA"
    category: str = "Software Engineering"
    description: str
    requirements: List[str]
    skills: List[str]
    deadline: Optional[str] = "2026-12-31"

class ApplicationCreate(BaseModel):
    candidate_name: str
    candidate_email: str
    candidate_phone: str
    experience_years: float = 0.0
    resume_url: Optional[str] = ""
    portfolio_url: Optional[str] = ""
    cover_letter: Optional[str] = ""

class QuizAnswerSubmit(BaseModel):
    selected_option: int

class DSAStatusUpdate(BaseModel):
    status: str  # 'Unsolved', 'In Progress', 'Solved', 'Revise'

class DSANotesUpdate(BaseModel):
    notes: str

# Ensure database exists
if not os.path.exists(DB_PATH):
    seed_database()

# ==========================================
# 1. JOB PORTAL ENDPOINTS
# ==========================================

@app.get("/api/jobs")
def get_jobs(
    search: Optional[str] = None,
    location: Optional[str] = None,
    job_type: Optional[str] = None,
    category: Optional[str] = None,
    bookmarked_only: bool = False
):
    with get_db() as conn:
        cursor = conn.cursor()
        query = """
        SELECT j.*, 
               CASE WHEN b.job_id IS NOT NULL THEN 1 ELSE 0 END as is_bookmarked,
               (SELECT COUNT(*) FROM applications WHERE job_id = j.id) as applicant_count
        FROM jobs j
        LEFT JOIN job_bookmarks b ON j.id = b.job_id
        WHERE j.is_active = 1
        """
        params = []

        if search:
            query += " AND (j.title LIKE ? OR j.company LIKE ? OR j.skills LIKE ? OR j.description LIKE ?)"
            term = f"%{search}%"
            params.extend([term, term, term, term])

        if location:
            query += " AND j.location LIKE ?"
            params.append(f"%{location}%")

        if job_type and job_type != "All":
            query += " AND j.job_type = ?"
            params.append(job_type)

        if category and category != "All":
            query += " AND j.category = ?"
            params.append(category)

        if bookmarked_only:
            query += " AND b.job_id IS NOT NULL"

        query += " ORDER BY j.id DESC"
        cursor.execute(query, params)
        rows = cursor.fetchall()

        jobs = []
        for r in rows:
            jobs.append({
                "id": r["id"],
                "title": r["title"],
                "company": r["company"],
                "company_logo": r["company_logo"],
                "location": r["location"],
                "job_type": r["job_type"],
                "experience": r["experience"],
                "salary": r["salary"],
                "category": r["category"],
                "description": r["description"],
                "requirements": json.loads(r["requirements"]),
                "skills": json.loads(r["skills"]),
                "posted_date": r["posted_date"],
                "deadline": r["deadline"],
                "is_bookmarked": bool(r["is_bookmarked"]),
                "applicant_count": r["applicant_count"]
            })
        return {"count": len(jobs), "jobs": jobs}

@app.get("/api/jobs/{job_id}")
def get_job_detail(job_id: int):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("""
        SELECT j.*, 
               CASE WHEN b.job_id IS NOT NULL THEN 1 ELSE 0 END as is_bookmarked,
               (SELECT COUNT(*) FROM applications WHERE job_id = j.id) as applicant_count
        FROM jobs j
        LEFT JOIN job_bookmarks b ON j.id = b.job_id
        WHERE j.id = ?
        """, (job_id,))
        row = cursor.fetchone()
        if not row:
            raise HTTPException(status_code=404, detail="Job not found")

        return {
            "id": row["id"],
            "title": row["title"],
            "company": row["company"],
            "company_logo": row["company_logo"],
            "location": row["location"],
            "job_type": row["job_type"],
            "experience": row["experience"],
            "salary": row["salary"],
            "category": row["category"],
            "description": row["description"],
            "requirements": json.loads(row["requirements"]),
            "skills": json.loads(row["skills"]),
            "posted_date": row["posted_date"],
            "deadline": row["deadline"],
            "is_bookmarked": bool(row["is_bookmarked"]),
            "applicant_count": row["applicant_count"]
        }

@app.post("/api/jobs")
def create_job(payload: JobCreate):
    with get_db() as conn:
        cursor = conn.cursor()
        today = datetime.now().strftime("%Y-%m-%d")
        cursor.execute("""
        INSERT INTO jobs (title, company, company_logo, location, job_type, experience, salary, category, description, requirements, skills, posted_date, deadline)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            payload.title,
            payload.company,
            payload.company_logo or "briefcase",
            payload.location,
            payload.job_type,
            payload.experience,
            payload.salary,
            payload.category,
            payload.description,
            json.dumps(payload.requirements),
            json.dumps(payload.skills),
            today,
            payload.deadline
        ))
        new_id = cursor.lastrowid
        return {"success": True, "job_id": new_id, "message": "Job opening posted successfully!"}

@app.post("/api/jobs/{job_id}/bookmark")
def toggle_bookmark(job_id: int):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT job_id FROM job_bookmarks WHERE job_id = ?", (job_id,))
        exists = cursor.fetchone()
        if exists:
            cursor.execute("DELETE FROM job_bookmarks WHERE job_id = ?", (job_id,))
            return {"bookmarked": False, "message": "Job removed from saved items"}
        else:
            now = datetime.now().isoformat()
            cursor.execute("INSERT INTO job_bookmarks (job_id, created_at) VALUES (?, ?)", (job_id, now))
            return {"bookmarked": True, "message": "Job saved to your bookmarks"}

@app.post("/api/jobs/{job_id}/apply")
def apply_to_job(job_id: int, app_data: ApplicationCreate):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT title, company FROM jobs WHERE id = ?", (job_id,))
        job = cursor.fetchone()
        if not job:
            raise HTTPException(status_code=404, detail="Job opening does not exist")

        now = datetime.now().strftime("%Y-%m-%d %H:%M")
        cursor.execute("""
        INSERT INTO applications (job_id, candidate_name, candidate_email, candidate_phone, experience_years, resume_url, portfolio_url, cover_letter, status, applied_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, 'Applied', ?)
        """, (
            job_id,
            app_data.candidate_name,
            app_data.candidate_email,
            app_data.candidate_phone,
            app_data.experience_years,
            app_data.resume_url,
            app_data.portfolio_url,
            app_data.cover_letter,
            now
        ))
        return {
            "success": True,
            "application_id": cursor.lastrowid,
            "message": f"Successfully applied for {job['title']} at {job['company']}!"
        }

@app.get("/api/applications")
def get_user_applications():
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("""
        SELECT a.*, j.title as job_title, j.company as job_company, j.location, j.salary, j.job_type
        FROM applications a
        JOIN jobs j ON a.job_id = j.id
        ORDER BY a.id DESC
        """)
        rows = cursor.fetchall()
        apps = []
        for r in rows:
            apps.append(dict(r))
        return {"count": len(apps), "applications": apps}

# ==========================================
# 2. PREPARATION HUB ENDPOINTS
# ==========================================

@app.get("/api/prep/categories")
def get_prep_categories():
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("""
        SELECT category, COUNT(*) as topic_count
        FROM prep_topics
        GROUP BY category
        """)
        topic_counts = {r["category"]: r["topic_count"] for r in cursor.fetchall()}

        cursor.execute("""
        SELECT category, COUNT(*) as question_count
        FROM prep_questions
        GROUP BY category
        """)
        question_counts = {r["category"]: r["question_count"] for r in cursor.fetchall()}

        categories = [
            {
                "id": "Aptitude",
                "name": "Quantitative & Logical Aptitude",
                "icon": "calculator",
                "color": "amber",
                "topics": topic_counts.get("Aptitude", 0),
                "questions": question_counts.get("Aptitude", 0),
                "description": "Percentages, Time & Work, Speed & Distance, Syllogisms, Blood Relations, and Deductive Reasoning."
            },
            {
                "id": "Technical",
                "name": "Technical & Core CS Subjects",
                "icon": "cpu",
                "color": "blue",
                "topics": topic_counts.get("Technical", 0),
                "questions": question_counts.get("Technical", 0),
                "description": "DBMS Normalization & SQL, Operating Systems, Computer Networks, OOP, and High-Level System Design."
            },
            {
                "id": "HR",
                "name": "HR & Behavioral Interview Prep",
                "icon": "users",
                "color": "emerald",
                "topics": topic_counts.get("HR", 0),
                "questions": question_counts.get("HR", 0),
                "description": "STAR Method, Amazon Leadership Principles, Googleyness, Top 10 HR questions, and Salary Negotiation."
            }
        ]
        return {"categories": categories}

@app.get("/api/prep/topics")
def get_prep_topics(category: Optional[str] = None):
    with get_db() as conn:
        cursor = conn.cursor()
        query = "SELECT id, category, sub_category, title, read_time, summary, order_idx FROM prep_topics"
        params = []
        if category and category != "All":
            query += " WHERE category = ?"
            params.append(category)
        query += " ORDER BY category, order_idx"
        cursor.execute(query, params)
        topics = [dict(r) for r in cursor.fetchall()]
        return {"count": len(topics), "topics": topics}

@app.get("/api/prep/topics/{topic_id}")
def get_prep_topic_detail(topic_id: int):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM prep_topics WHERE id = ?", (topic_id,))
        row = cursor.fetchone()
        if not row:
            raise HTTPException(status_code=404, detail="Topic not found")
        return dict(row)

@app.get("/api/prep/questions")
def get_prep_questions(
    category: Optional[str] = None,
    difficulty: Optional[str] = None
):
    with get_db() as conn:
        cursor = conn.cursor()
        query = """
        SELECT q.id, q.category, q.sub_category, q.difficulty, q.question, q.options, q.tags,
               a.selected_option, a.is_correct
        FROM prep_questions q
        LEFT JOIN user_quiz_attempts a ON q.id = a.question_id
        WHERE 1=1
        """
        params = []
        if category and category != "All":
            query += " AND q.category = ?"
            params.append(category)
        if difficulty and difficulty != "All":
            query += " AND q.difficulty = ?"
            params.append(difficulty)

        query += " ORDER BY q.id"
        cursor.execute(query, params)
        rows = cursor.fetchall()
        questions = []
        for r in rows:
            questions.append({
                "id": r["id"],
                "category": r["category"],
                "sub_category": r["sub_category"],
                "difficulty": r["difficulty"],
                "question": r["question"],
                "options": json.loads(r["options"]),
                "tags": json.loads(r["tags"]),
                "user_attempt": {
                    "selected_option": r["selected_option"],
                    "is_correct": bool(r["is_correct"])
                } if r["selected_option"] is not None else None
            })
        return {"count": len(questions), "questions": questions}

@app.post("/api/prep/questions/{question_id}/submit")
def submit_question_answer(question_id: int, answer: QuizAnswerSubmit):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT correct_index, explanation FROM prep_questions WHERE id = ?", (question_id,))
        row = cursor.fetchone()
        if not row:
            raise HTTPException(status_code=404, detail="Question not found")

        is_correct = 1 if answer.selected_option == row["correct_index"] else 0
        now = datetime.now().isoformat()

        # Update or insert attempt
        cursor.execute("DELETE FROM user_quiz_attempts WHERE question_id = ?", (question_id,))
        cursor.execute("""
        INSERT INTO user_quiz_attempts (question_id, selected_option, is_correct, attempted_at)
        VALUES (?, ?, ?, ?)
        """, (question_id, answer.selected_option, is_correct, now))

        return {
            "is_correct": bool(is_correct),
            "correct_index": row["correct_index"],
            "explanation": row["explanation"]
        }

@app.get("/api/prep/quiz-stats")
def get_quiz_stats():
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) as total_questions FROM prep_questions")
        total_q = cursor.fetchone()["total_questions"]

        cursor.execute("SELECT COUNT(*) as attempted, SUM(is_correct) as correct FROM user_quiz_attempts")
        att = cursor.fetchone()
        attempted = att["attempted"] or 0
        correct = att["correct"] or 0
        accuracy = round((correct / attempted * 100), 1) if attempted > 0 else 0.0

        return {
            "total_questions": total_q,
            "attempted": attempted,
            "correct": correct,
            "accuracy": accuracy
        }

# ==========================================
# 3. COMPANIES HIRING PROCESS ENDPOINTS
# ==========================================

@app.get("/api/companies")
def get_companies(category: Optional[str] = None):
    with get_db() as conn:
        cursor = conn.cursor()
        query = "SELECT id, name, slug, category, tagline, avg_salary, difficulty, frequently_asked_topics FROM companies"
        params = []
        if category and category != "All":
            query += " WHERE category = ?"
            params.append(category)
        query += " ORDER BY id"
        cursor.execute(query, params)
        rows = cursor.fetchall()
        result = []
        for r in rows:
            result.append({
                "id": r["id"],
                "name": r["name"],
                "slug": r["slug"],
                "category": r["category"],
                "tagline": r["tagline"],
                "avg_salary": r["avg_salary"],
                "difficulty": r["difficulty"],
                "frequently_asked_topics": json.loads(r["frequently_asked_topics"])
            })
        return {"count": len(result), "companies": result}

@app.get("/api/companies/{slug}")
def get_company_detail(slug: str):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM companies WHERE slug = ?", (slug,))
        row = cursor.fetchone()
        if not row:
            raise HTTPException(status_code=404, detail="Company guide not found")

        return {
            "id": row["id"],
            "name": row["name"],
            "slug": row["slug"],
            "category": row["category"],
            "tagline": row["tagline"],
            "avg_salary": row["avg_salary"],
            "difficulty": row["difficulty"],
            "eligibility": json.loads(row["eligibility"]),
            "exam_pattern": json.loads(row["exam_pattern"]),
            "syllabus": json.loads(row["syllabus"]),
            "rounds_breakdown": json.loads(row["rounds_breakdown"]),
            "frequently_asked_topics": json.loads(row["frequently_asked_topics"]),
            "sample_questions": json.loads(row["sample_questions"]),
            "tips": json.loads(row["tips"])
        }

# ==========================================
# 4. DEDICATED DSA PREP SHEET ENDPOINTS
# ==========================================

@app.get("/api/dsa/topics")
def get_dsa_topics():
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("""
        SELECT p.topic, 
               COUNT(*) as total,
               SUM(CASE WHEN u.status = 'Solved' THEN 1 ELSE 0 END) as solved,
               SUM(CASE WHEN u.status = 'In Progress' THEN 1 ELSE 0 END) as in_progress,
               SUM(CASE WHEN u.status = 'Revise' THEN 1 ELSE 0 END) as revise
        FROM dsa_problems p
        LEFT JOIN user_dsa_progress u ON p.id = u.problem_id
        GROUP BY p.topic
        ORDER BY MIN(p.order_idx)
        """)
        rows = cursor.fetchall()
        topics = []
        for r in rows:
            topics.append({
                "topic": r["topic"],
                "total": r["total"],
                "solved": r["solved"] or 0,
                "in_progress": r["in_progress"] or 0,
                "revise": r["revise"] or 0,
                "percentage": round(((r["solved"] or 0) / r["total"] * 100), 1)
            })
        return {"topics": topics}

@app.get("/api/dsa/problems")
def get_dsa_problems(
    topic: Optional[str] = None,
    difficulty: Optional[str] = None,
    status: Optional[str] = None,
    search: Optional[str] = None
):
    with get_db() as conn:
        cursor = conn.cursor()
        query = """
        SELECT p.id, p.topic, p.title, p.difficulty, p.leetcode_url, p.gfg_url,
               p.time_complexity, p.space_complexity, p.order_idx,
               COALESCE(u.status, 'Unsolved') as user_status,
               COALESCE(u.notes, '') as user_notes,
               u.updated_at
        FROM dsa_problems p
        LEFT JOIN user_dsa_progress u ON p.id = u.problem_id
        WHERE 1=1
        """
        params = []
        if topic and topic != "All":
            query += " AND p.topic = ?"
            params.append(topic)
        if difficulty and difficulty != "All":
            query += " AND p.difficulty = ?"
            params.append(difficulty)
        if status and status != "All":
            if status == "Unsolved":
                query += " AND (u.status IS NULL OR u.status = 'Unsolved')"
            else:
                query += " AND u.status = ?"
                params.append(status)
        if search:
            query += " AND p.title LIKE ?"
            params.append(f"%{search}%")

        query += " ORDER BY p.order_idx"
        cursor.execute(query, params)
        rows = cursor.fetchall()
        problems = [dict(r) for r in rows]
        return {"count": len(problems), "problems": problems}

@app.get("/api/dsa/problems/{problem_id}")
def get_dsa_problem_detail(problem_id: int):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("""
        SELECT p.*, 
               COALESCE(u.status, 'Unsolved') as user_status,
               COALESCE(u.notes, '') as user_notes,
               u.updated_at
        FROM dsa_problems p
        LEFT JOIN user_dsa_progress u ON p.id = u.problem_id
        WHERE p.id = ?
        """, (problem_id,))
        row = cursor.fetchone()
        if not row:
            raise HTTPException(status_code=404, detail="DSA problem not found")
        return dict(row)

@app.post("/api/dsa/problems/{problem_id}/status")
def update_dsa_status(problem_id: int, payload: DSAStatusUpdate):
    with get_db() as conn:
        cursor = conn.cursor()
        now = datetime.now().isoformat()
        cursor.execute("""
        INSERT INTO user_dsa_progress (problem_id, status, notes, updated_at)
        VALUES (?, ?, '', ?)
        ON CONFLICT(problem_id) DO UPDATE SET
            status = excluded.status,
            updated_at = excluded.updated_at
        """, (problem_id, payload.status, now))
        return {"success": True, "status": payload.status}

@app.post("/api/dsa/problems/{problem_id}/notes")
def update_dsa_notes(problem_id: int, payload: DSANotesUpdate):
    with get_db() as conn:
        cursor = conn.cursor()
        now = datetime.now().isoformat()
        cursor.execute("""
        INSERT INTO user_dsa_progress (problem_id, status, notes, updated_at)
        VALUES (?, 'In Progress', ?, ?)
        ON CONFLICT(problem_id) DO UPDATE SET
            notes = excluded.notes,
            updated_at = excluded.updated_at
        """, (problem_id, payload.notes, now))
        return {"success": True, "notes": payload.notes}

@app.get("/api/dsa/stats")
def get_dsa_overall_stats():
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) as total FROM dsa_problems")
        total = cursor.fetchone()["total"]

        cursor.execute("""
        SELECT 
            SUM(CASE WHEN u.status = 'Solved' THEN 1 ELSE 0 END) as solved,
            SUM(CASE WHEN u.status = 'In Progress' THEN 1 ELSE 0 END) as in_progress,
            SUM(CASE WHEN u.status = 'Revise' THEN 1 ELSE 0 END) as revise,
            SUM(CASE WHEN u.status = 'Solved' AND p.difficulty = 'Easy' THEN 1 ELSE 0 END) as solved_easy,
            SUM(CASE WHEN u.status = 'Solved' AND p.difficulty = 'Medium' THEN 1 ELSE 0 END) as solved_medium,
            SUM(CASE WHEN u.status = 'Solved' AND p.difficulty = 'Hard' THEN 1 ELSE 0 END) as solved_hard,
            SUM(CASE WHEN p.difficulty = 'Easy' THEN 1 ELSE 0 END) as total_easy,
            SUM(CASE WHEN p.difficulty = 'Medium' THEN 1 ELSE 0 END) as total_medium,
            SUM(CASE WHEN p.difficulty = 'Hard' THEN 1 ELSE 0 END) as total_hard
        FROM dsa_problems p
        LEFT JOIN user_dsa_progress u ON p.id = u.problem_id
        """)
        s = cursor.fetchone()
        solved = s["solved"] or 0
        return {
            "total": total,
            "solved": solved,
            "in_progress": s["in_progress"] or 0,
            "revise": s["revise"] or 0,
            "percentage": round((solved / total * 100), 1) if total > 0 else 0.0,
            "by_difficulty": {
                "easy": {"solved": s["solved_easy"] or 0, "total": s["total_easy"] or 0},
                "medium": {"solved": s["solved_medium"] or 0, "total": s["total_medium"] or 0},
                "hard": {"solved": s["solved_hard"] or 0, "total": s["total_hard"] or 0}
            }
        }

# ==========================================
# 5. OVERALL DASHBOARD & PLATFORM SUMMARY
# ==========================================

@app.get("/api/dashboard/stats")
def get_dashboard_summary():
    with get_db() as conn:
        cursor = conn.cursor()
        # Jobs count
        cursor.execute("SELECT COUNT(*) as total_jobs FROM jobs WHERE is_active = 1")
        total_jobs = cursor.fetchone()["total_jobs"]

        # Applications submitted
        cursor.execute("SELECT COUNT(*) as apps_count FROM applications")
        apps_count = cursor.fetchone()["apps_count"]

        # Bookmarked jobs
        cursor.execute("SELECT COUNT(*) as bookmarks_count FROM job_bookmarks")
        bookmarks_count = cursor.fetchone()["bookmarks_count"]

        # DSA problems & solved
        cursor.execute("SELECT COUNT(*) as total_dsa FROM dsa_problems")
        total_dsa = cursor.fetchone()["total_dsa"]
        cursor.execute("SELECT COUNT(*) as solved_dsa FROM user_dsa_progress WHERE status = 'Solved'")
        solved_dsa = cursor.fetchone()["solved_dsa"]

        # Quizzes
        cursor.execute("SELECT COUNT(*) as attempted_quizzes, SUM(is_correct) as correct_quizzes FROM user_quiz_attempts")
        q = cursor.fetchone()
        attempted_quizzes = q["attempted_quizzes"] or 0
        correct_quizzes = q["correct_quizzes"] or 0

        # Companies
        cursor.execute("SELECT COUNT(*) as companies_count FROM companies")
        companies_count = cursor.fetchone()["companies_count"]

        # Prep topics
        cursor.execute("SELECT COUNT(*) as topics_count FROM prep_topics")
        topics_count = cursor.fetchone()["topics_count"]

        # Readiness score (formula: 50% DSA + 30% Quiz + 20% Applications/Prep)
        dsa_pct = (solved_dsa / total_dsa * 100) if total_dsa > 0 else 0
        quiz_pct = (correct_quizzes / attempted_quizzes * 100) if attempted_quizzes > 0 else 0
        readiness_score = round((0.5 * dsa_pct) + (0.3 * quiz_pct) + min(20, (apps_count * 5) + (attempted_quizzes * 2)), 1)
        readiness_score = min(100.0, max(0.0, readiness_score))

        return {
            "total_jobs": total_jobs,
            "applications_submitted": apps_count,
            "saved_jobs": bookmarks_count,
            "dsa_total": total_dsa,
            "dsa_solved": solved_dsa,
            "dsa_percentage": round((solved_dsa / total_dsa * 100), 1) if total_dsa > 0 else 0,
            "quizzes_attempted": attempted_quizzes,
            "quizzes_accuracy": round((correct_quizzes / attempted_quizzes * 100), 1) if attempted_quizzes > 0 else 0,
            "companies_count": companies_count,
            "topics_count": topics_count,
            "readiness_score": readiness_score
        }

# ==========================================
# STATIC FILES SERVING
# ==========================================

static_dir = os.path.join(os.path.dirname(__file__), "static")
if not os.path.exists(static_dir):
    os.makedirs(static_dir)

app.mount("/static", StaticFiles(directory=static_dir), name="static")

@app.get("/")
def serve_index():
    index_path = os.path.join(static_dir, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return HTMLResponse("<h1>Job & Preparation Hub is starting...</h1>")
