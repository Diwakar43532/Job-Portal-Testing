# CareerForge: Job Portal & Comprehensive Tech Preparation Hub

An end-to-end, high-performance web platform combining a **Full Tech Job Portal**, **Preparation Hub (Aptitude, Core Technical CS, HR Behavioral)**, **Top Tech Companies Hiring Process Playbooks**, and a **Dedicated Topic-Wise DSA Preparation Sheet**.

---

## 🌟 Key Features

### 1. 💼 Job Portal
- **Rich Tech Job Listings**: High-paying roles across Google, Amazon, Microsoft, Infosys, TCS, Razorpay, Swiggy, Flipkart, NVIDIA, and Atlassian.
- **Search & Multi-Filters**: Filter by role keywords, location (Bangalore, Pune, Remote, etc.), job type (Full-time, Internship), and domain categories (Software Engineering, Backend, Frontend, Full Stack, AI/ML, DevOps).
- **Interactive Applications**: One-click "Apply Now" modal with candidate resume link, experience, portfolio, and cover letter tracking.
- **Bookmark System**: Save favorite openings for quick review.
- **Recruiter Posting**: In-app modal for recruiters to publish new openings instantly to the SQLite database.

### 2. 📚 Preparation Hub
- **Three Core Streams**:
  - **Aptitude**: Quantitative Aptitude (Percentages, Profit & Loss, Speed-Time-Distance, Work & Pipes) & Logical Reasoning (Syllogisms, Blood Relations, Coding-Decoding).
  - **Technical & Core CS**: DBMS (1NF-BCNF, SQL Joins, ACID, Isolation Levels), Operating Systems (Processes vs Threads, Coffman Deadlock Conditions, Paging), Computer Networks (OSI 7 layers, TCP 3-way handshake, DNS, HTTPS), OOP & High-Level System Design (SOLID, Caching, CAP Theorem).
  - **HR & Behavioral**: The STAR Method Framework, Amazon 16 Leadership Principles, Top 10 HR interview questions with model answers, and Salary Negotiation scripts.
- **Notes & Cheatsheets**: In-depth theoretical guides with code examples, formulas, and diagrams rendered in Markdown.
- **Interactive Practice Quiz Engine**: MCQ questions with instant scoring, feedback, and comprehensive logic explanations.

### 3. 🏢 Companies Hiring Process
- **In-Depth Recruiter Roadmaps**: Guides for **Google, Amazon, TCS, Infosys, Microsoft, Flipkart**, and more.
- **Exam Pattern**: Detailed breakdown of online assessments, sectional durations, platforms (HackerRank, Codility, TCS iON), question formats, and negative marking rules.
- **Eligibility Criteria Checklist**: Academic percentage/CGPA cutoffs, backlog allowances, eligible degree branches, and graduation batches.
- **Syllabus & Weightage**: Sectional weightage and high-frequency topics.
- **Sample Interview Questions**: Exact questions previously asked in technical and behavioral rounds.
- **Insider Tips**: Practical strategies to stand out from other candidates.

### 4. ⚡ Dedicated Topic-Wise DSA Prep Sheet
- **Curated Interview Problems**: Categorized into *Arrays & Hashing, Two Pointers & Sliding Window, Binary Search, Linked List, Stack & Queue, Trees & Graphs, Heaps & Priority Queues, Dynamic Programming, Backtracking, and Bit Manipulation*.
- **Interactive Status Tracking**: Cycle problem status between **Unsolved**, **In Progress**, **Solved**, and **Marked for Revision**.
- **Personal Notes**: Modal to write and persist custom takeaways and edge-case reminders for any problem.
- **Brute-to-Optimal Solutions**: Detailed approach breakdowns with Big-O time and space complexity analysis.
- **Multi-Language Code Implementations**: Clean Python and C++ source code with syntax highlighting and 1-click clipboard copy.
- **External Practice Links**: Quick shortcuts to LeetCode and GeeksforGeeks problem statements.
- **Progress Analytics**: Real-time progress bar and difficulty completion breakdown (Easy, Medium, Hard).

### 5. 📊 Candidate Dashboard & Application Tracker
- **Interview Readiness Gauge**: Composite metric calculated from DSA completion and quiz accuracy.
- **Submitted Applications Tracker**: Real-time status board tracking applied roles through the pipeline (`Applied`, `Reviewing`, `Shortlisted`, `Interview`, `Offer`).

---

## 🛠️ Architecture & Tech Stack

- **Backend**: Python 3.14 + [FastAPI](https://fastapi.tiangolo.com/) (Asynchronous, Type-annotated, RESTful)
- **Server**: [Uvicorn](https://www.uvicorn.org/) (Lightning-fast ASGI server)
- **Database**: SQLite3 (`portal.db`) with relational integrity and automatic migrations
- **Frontend**: Clean Vanilla JavaScript SPA (Modular architecture: `jobs.js`, `prep.js`, `companies.js`, `dsa.js`, `dashboard.js`)
- **Styling**: Tailwind CSS + Custom Dark Theme Glassmorphism
- **Icons & Syntax Highlighting**: FontAwesome 6.5.1 + Highlight.js + Marked.js

---

## 🚀 Getting Started

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Seed Database (Optional - Happens automatically on first start)
```bash
python seed_data.py
```

### 3. Start the Server
```bash
python -m uvicorn main:app --reload --port 8000
```

### 4. Open the Web Application
Open your browser and navigate to:
```
http://localhost:8000
```

Interactive API documentation (Swagger UI) is available at:
```
http://localhost:8000/docs
```
