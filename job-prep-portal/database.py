import sqlite3
import json
import os
from contextlib import contextmanager

DB_PATH = os.path.join(os.path.dirname(__file__), "portal.db")

@contextmanager
def get_db():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()

def init_db():
    with get_db() as conn:
        cursor = conn.cursor()
        
        # 1. Jobs table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS jobs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            company TEXT NOT NULL,
            company_logo TEXT,
            location TEXT NOT NULL,
            job_type TEXT NOT NULL,
            experience TEXT NOT NULL,
            salary TEXT NOT NULL,
            category TEXT NOT NULL,
            description TEXT NOT NULL,
            requirements TEXT NOT NULL,
            skills TEXT NOT NULL,
            posted_date TEXT NOT NULL,
            deadline TEXT,
            is_active INTEGER DEFAULT 1
        )
        """)

        # 2. Applications table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS applications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            job_id INTEGER NOT NULL,
            candidate_name TEXT NOT NULL,
            candidate_email TEXT NOT NULL,
            candidate_phone TEXT NOT NULL,
            experience_years REAL DEFAULT 0,
            resume_url TEXT,
            portfolio_url TEXT,
            cover_letter TEXT,
            status TEXT DEFAULT 'Applied',
            applied_at TEXT NOT NULL,
            FOREIGN KEY (job_id) REFERENCES jobs (id)
        )
        """)

        # 3. Saved / Bookmarked jobs
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS job_bookmarks (
            job_id INTEGER PRIMARY KEY,
            created_at TEXT NOT NULL,
            FOREIGN KEY (job_id) REFERENCES jobs (id)
        )
        """)

        # 4. Preparation notes/topics
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS prep_topics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category TEXT NOT NULL,
            sub_category TEXT NOT NULL,
            title TEXT NOT NULL,
            read_time TEXT NOT NULL,
            summary TEXT NOT NULL,
            content TEXT NOT NULL,
            order_idx INTEGER DEFAULT 0
        )
        """)

        # 5. Practice Questions
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS prep_questions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category TEXT NOT NULL,
            sub_category TEXT NOT NULL,
            difficulty TEXT NOT NULL,
            question TEXT NOT NULL,
            options TEXT NOT NULL,
            correct_index INTEGER NOT NULL,
            explanation TEXT NOT NULL,
            tags TEXT NOT NULL
        )
        """)

        # 6. User quiz answers / attempts
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_quiz_attempts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            question_id INTEGER NOT NULL,
            selected_option INTEGER NOT NULL,
            is_correct INTEGER NOT NULL,
            attempted_at TEXT NOT NULL
        )
        """)

        # 7. Companies hiring process
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS companies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            slug TEXT UNIQUE NOT NULL,
            category TEXT NOT NULL,
            tagline TEXT NOT NULL,
            avg_salary TEXT NOT NULL,
            difficulty TEXT NOT NULL,
            eligibility TEXT NOT NULL,
            exam_pattern TEXT NOT NULL,
            syllabus TEXT NOT NULL,
            rounds_breakdown TEXT NOT NULL,
            frequently_asked_topics TEXT NOT NULL,
            sample_questions TEXT NOT NULL,
            tips TEXT NOT NULL
        )
        """)

        # 8. DSA Problems
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS dsa_problems (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            topic TEXT NOT NULL,
            title TEXT NOT NULL,
            difficulty TEXT NOT NULL,
            leetcode_url TEXT,
            gfg_url TEXT,
            description TEXT NOT NULL,
            approach_notes TEXT NOT NULL,
            time_complexity TEXT NOT NULL,
            space_complexity TEXT NOT NULL,
            code_python TEXT NOT NULL,
            code_cpp TEXT NOT NULL,
            order_idx INTEGER DEFAULT 0
        )
        """)

        # 9. User DSA progress
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_dsa_progress (
            problem_id INTEGER PRIMARY KEY,
            status TEXT DEFAULT 'Unsolved',
            notes TEXT DEFAULT '',
            updated_at TEXT NOT NULL,
            FOREIGN KEY (problem_id) REFERENCES dsa_problems (id)
        )
        """)

        print("Database schema verified and initialized.")

if __name__ == "__main__":
    init_db()
