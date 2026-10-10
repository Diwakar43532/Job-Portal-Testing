import sqlite3
import json
import os
from database import DB_PATH, init_db

def seed_database():
    init_db()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Check if already seeded
    cursor.execute("SELECT COUNT(*) FROM jobs")
    if cursor.fetchone()[0] > 0:
        print("Database already has data. Clearing and re-seeding to ensure latest rich content...")
        cursor.execute("DELETE FROM jobs")
        cursor.execute("DELETE FROM prep_topics")
        cursor.execute("DELETE FROM prep_questions")
        cursor.execute("DELETE FROM companies")
        cursor.execute("DELETE FROM dsa_problems")
        # Keep user progress or reset
        # We can keep user progress tables

    print("Seeding Jobs...")
    jobs = [
        (
            "Software Development Engineer I (SDE-1)",
            "Google",
            "google",
            "Bangalore, India (Hybrid)",
            "Full-time",
            "0-2 years / Freshers",
            "₹24 - ₹32 LPA",
            "Software Engineering",
            "Join Google's core engineering teams building scalable distributed systems that serve billions of global users. You will design, develop, test, deploy, and maintain software solutions across Google Cloud, Search, or Workspace.",
            json.dumps([
                "Bachelor's or Master's degree in Computer Science, related technical field, or equivalent practical experience.",
                "Strong proficiency in one or more general-purpose languages: C++, Java, Python, or Go.",
                "Solid grasp of Data Structures, Algorithms, Complexity Analysis, and Object-Oriented Design.",
                "Familiarity with distributed systems, cloud computing, or modern web architectures."
            ]),
            json.dumps(["Data Structures", "Algorithms", "C++", "Python", "Distributed Systems", "System Design"]),
            "2026-10-08",
            "2026-11-15"
        ),
        (
            "SDE II - AWS Cloud Infrastructure",
            "Amazon",
            "amazon",
            "Hyderabad, India (On-site)",
            "Full-time",
            "2-5 years",
            "₹35 - ₹48 LPA",
            "Backend",
            "Amazon Web Services (AWS) is looking for an experienced SDE II to build high-throughput, low-latency microservices for AWS Elastic Compute Cloud (EC2). You will participate in architecture reviews and lead implementation of mission-critical services.",
            json.dumps([
                "2+ years of non-internship professional software development experience.",
                "Deep experience with Java, C++, or Go, and relational/NoSQL databases (DynamoDB, PostgreSQL).",
                "Proven track record of designing fault-tolerant distributed cloud architectures.",
                "Strong knowledge of concurrency, multithreading, and RESTful APIs."
            ]),
            json.dumps(["AWS", "Java", "Distributed Systems", "DynamoDB", "Microservices", "Docker"]),
            "2026-10-05",
            "2026-11-10"
        ),
        (
            "Frontend Engineer - Modern Web Apps",
            "Microsoft",
            "microsoft",
            "Bangalore, India (Remote)",
            "Full-time",
            "1-3 years",
            "₹22 - ₹30 LPA",
            "Frontend",
            "Build next-generation user interfaces for Microsoft 365 and Teams Web. You will craft accessible, high-performance web components used daily by hundreds of millions of enterprise users worldwide.",
            json.dumps([
                "B.Tech/B.E in CS/IT or equivalent industry experience.",
                "Expertise in modern JavaScript/TypeScript, React.js, HTML5, CSS3, and state management (Redux/Zustand).",
                "Strong understanding of Web Performance optimization, SSR, and Web Accessibility (WCAG 2.1).",
                "Experience writing unit and integration tests using Jest, Cypress, or Playwright."
            ]),
            json.dumps(["React.js", "TypeScript", "Next.js", "CSS3/Tailwind", "Web Performance", "Jest"]),
            "2026-10-09",
            "2026-11-20"
        ),
        (
            "Digital Specialist Engineer (DSE)",
            "Infosys",
            "infosys",
            "Pune / Bangalore / Hyderabad",
            "Full-time",
            "Fresher (2025/2026 Batch)",
            "₹6.25 - ₹9.5 LPA",
            "Software Engineering",
            "Infosys Digital Specialist Engineer role focuses on developing advanced digital solutions, full-stack enterprise applications, AI integrations, and cloud services for global Fortune 500 clients.",
            json.dumps([
                "BE / B.Tech / M.Tech / MCA in any engineering stream with 60%+ throughout academics.",
                "Strong coding skill in Java, Python, or C++ with knowledge of SQL and Web basics.",
                "Candidates cleared via InfyTQ or HackWithInfy coding competition get direct preference.",
                "Good analytical thinking and communication skills."
            ]),
            json.dumps(["Python", "Java", "SQL", "Data Structures", "Spring Boot", "Git"]),
            "2026-10-07",
            "2026-11-30"
        ),
        (
            "Prime / Digital Software Engineer",
            "TCS",
            "tcs",
            "Pan India (Chennai / Bangalore / Delhi)",
            "Full-time",
            "Fresher (2025/2026 Batch)",
            "₹7.0 - ₹11.5 LPA",
            "Software Engineering",
            "TCS Prime & Digital cadre hiring through TCS NQT. Work on cutting-edge engineering projects including GenAI, Cybersecurity, Cloud, and Big Data platforms.",
            json.dumps([
                "B.Tech / B.E / M.Tech / MCA with minimum 65% or 6.5 CGPA with no active backlogs.",
                "Top percentile in TCS NQT Advanced Cognitive and Advanced Coding sections.",
                "Good proficiency in Object Oriented Programming, DBMS, and problem-solving.",
                "Excellent interpersonal and teamwork capabilities."
            ]),
            json.dumps(["Data Structures", "Python", "Java", "DBMS", "Cloud Basics", "REST API"]),
            "2026-10-06",
            "2026-11-25"
        ),
        (
            "Backend Platform Engineer",
            "Razorpay",
            "razorpay",
            "Bangalore, India (Hybrid)",
            "Full-time",
            "1-3 years",
            "₹20 - ₹28 LPA",
            "Backend",
            "Join India's leading fintech payment gateway. You will build high-reliability transaction processing systems processing billions of dollars in daily payments with 99.999% uptime.",
            json.dumps([
                "Bachelor's degree in Computer Science or related branch.",
                "Strong backend development experience in Go, Node.js, or Python.",
                "Deep knowledge of ACID transactions, MySQL/PostgreSQL, Redis caching, and Kafka.",
                "Understanding of financial domain security standards (PCI-DSS) is a plus."
            ]),
            json.dumps(["Golang", "PostgreSQL", "Kafka", "Redis", "Distributed Systems", "FinTech"]),
            "2026-10-04",
            "2026-11-05"
        ),
        (
            "Full Stack Developer (Customer Experience)",
            "Swiggy",
            "swiggy",
            "Bangalore, India (Remote-first)",
            "Full-time",
            "1-4 years",
            "₹25 - ₹35 LPA",
            "Full Stack",
            "Build blazing-fast, delightful ordering and delivery tracking experiences for Swiggy and Instamart. Work on micro-frontends and event-driven backend services.",
            json.dumps([
                "Proficiency in React.js, React Native, or modern JavaScript frameworks.",
                "Strong backend programming in Java (Spring Boot) or Node.js.",
                "Solid understanding of REST APIs, WebSockets, Kafka, and Redis.",
                "Passion for product UX, performance optimizations, and metrics."
            ]),
            json.dumps(["React.js", "Node.js", "Java", "Kafka", "Redis", "Microservices"]),
            "2026-10-09",
            "2026-11-18"
        ),
        (
            "Software Engineer - Core Systems",
            "Flipkart",
            "flipkart",
            "Bangalore, India (Hybrid)",
            "Full-time",
            "Fresher - 2 years",
            "₹22 - ₹28 LPA",
            "Software Engineering",
            "Work on India's premier e-commerce ecosystem. You will develop backend search, inventory indexing, and checkout checkout microservices that scale during the Big Billion Days.",
            json.dumps([
                "B.Tech/M.Tech in CS/IT from a recognized university.",
                "Exceptional algorithmic problem-solving and coding ability.",
                "Experience with Java/Spring or C++, RDBMS, and caching mechanisms.",
                "Sound knowledge of Multi-threading, Design Patterns, and OOP."
            ]),
            json.dumps(["Java", "Spring Boot", "Data Structures", "MySQL", "Kafka", "System Design"]),
            "2026-10-02",
            "2026-11-12"
        ),
        (
            "AI / Machine Learning Engineer Intern",
            "NVIDIA",
            "nvidia",
            "Pune / Bangalore, India",
            "Internship",
            "College Final Year / Pre-final",
            "₹75,000 / month Stipend + PPO",
            "AI/ML",
            "Collaborate with NVIDIA researchers on deep learning frameworks, CUDA acceleration, computer vision, and LLM fine-tuning pipelines.",
            json.dumps([
                "Pursuing B.Tech/M.Tech in CS, AI, EE, or related quantitative field.",
                "Hands-on experience with PyTorch, TensorFlow, NumPy, and Scikit-learn.",
                "Strong mathematical foundation in Linear Algebra, Calculus, and Probability.",
                "Knowledge of GPU programming or CUDA is an advantage."
            ]),
            json.dumps(["PyTorch", "Python", "Deep Learning", "Computer Vision", "CUDA", "LLMs"]),
            "2026-10-09",
            "2026-11-30"
        ),
        (
            "Associate Software Engineer",
            "Wipro",
            "wipro",
            "Hyderabad / Bangalore / Chennai",
            "Full-time",
            "Fresher (2025/2026 Batch)",
            "₹4.5 - ₹6.5 LPA",
            "Software Engineering",
            "Hiring enthusiastic fresh graduates for Wipro Elite & Turbo technology cohorts. Role encompasses software development, cloud infrastructure management, and QA automation.",
            json.dumps([
                "Full-time BE/B.Tech/MCA with 60% or 6.0 CGPA throughout 10th, 12th, and Degree.",
                "Basic understanding of any language: Java, C++, Python, or C#.",
                "Strong quantitative aptitude, logical reasoning, and English comprehension.",
                "Willingness to work across global client projects."
            ]),
            json.dumps(["Java", "SQL", "HTML/CSS", "Python", "Problem Solving"]),
            "2026-10-01",
            "2026-11-20"
        ),
        (
            "Platform Engineer - Jira & Confluence Cloud",
            "Atlassian",
            "atlassian",
            "Bangalore, India (Remote)",
            "Full-time",
            "1-3 years",
            "₹30 - ₹42 LPA",
            "Backend",
            "Help build the collaborative tools used by 80% of Fortune 500 companies. Design scalable distributed databases, GraphQL endpoints, and resilience frameworks.",
            json.dumps([
                "Bachelor's degree in Computer Science or equivalent practical experience.",
                "Proficiency in Java, Kotlin, or Go with strong OOP and clean code principles.",
                "Experience with AWS (Lambda, DynamoDB, SQS), Docker, and Kubernetes.",
                "Commitment to high code quality, automated testing, and CI/CD."
            ]),
            json.dumps(["Java", "Kotlin", "AWS", "GraphQL", "Kubernetes", "Microservices"]),
            "2026-10-08",
            "2026-11-22"
        ),
        (
            "DevOps & Cloud Engineer",
            "CRED",
            "cred",
            "Bangalore, India (On-site)",
            "Full-time",
            "1-3 years",
            "₹26 - ₹36 LPA",
            "DevOps",
            "Design, automate, and safeguard the zero-trust cloud infrastructure that powers CRED's financial services and reward experiences.",
            json.dumps([
                "Demonstrated experience in Linux system administration and cloud platforms (AWS/GCP).",
                "Proficiency with Infrastructure as Code (Terraform) and Kubernetes cluster management.",
                "Experience configuring CI/CD pipelines (GitHub Actions, ArgoCD).",
                "Strong grasp of Observability tools: Prometheus, Grafana, Datadog."
            ]),
            json.dumps(["Kubernetes", "Terraform", "AWS", "Docker", "CI/CD", "Linux"]),
            "2026-10-03",
            "2026-11-15"
        )
    ]

    for j in jobs:
        cursor.execute("""
        INSERT INTO jobs (title, company, company_logo, location, job_type, experience, salary, category, description, requirements, skills, posted_date, deadline)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, j)

    # -------------------------------------------------------------
    # Seeding Preparation Notes / Topics
    # -------------------------------------------------------------
    print("Seeding Preparation Notes...")
    prep_topics = [
        # APTITUDE - Quantitative
        (
            "Aptitude",
            "Quantitative Aptitude",
            "Percentages, Profit & Loss Master Guide",
            "12 min read",
            "Comprehensive formulas, shortcut tricks, and standard patterns for Percentages, Profit, Loss, Marked Price, and Successive Discounts.",
            """### Core Concepts & Formulas

#### 1. Percentage Basics
* **Fraction to Percentage Multipliers:**
  * $1/2 = 50\\%$
  * $1/3 = 33.33\\%$
  * $1/4 = 25\\%$
  * $1/5 = 20\\%$
  * $1/6 = 16.66\\%$
  * $1/7 = 14.28\\%$
  * $1/8 = 12.5\\%$
  * $1/9 = 11.11\\%$
  * $1/11 = 9.09\\%$
  * $1/12 = 8.33\\%$
* **Percentage Change:**
  $$\\text{Percentage Change} = \\left(\\frac{\\text{Final Value} - \\text{Initial Value}}{\\text{Initial Value}}\\right) \\times 100$$
* **Successive Percentage Change:**
  $$\\text{Net Change} = \\left(a + b + \\frac{ab}{100}\\right)\\%$$

#### 2. Profit & Loss Formulas
* **Profit:** $\\text{SP} - \\text{CP}$ (when $\\text{SP} > \\text{CP}$)
* **Loss:** $\\text{CP} - \\text{SP}$ (when $\\text{CP} > \\text{SP}$)
* **Profit %:** $\\left(\\frac{\\text{Profit}}{\\text{CP}}\\right) \\times 100$
* **Loss %:** $\\left(\\frac{\\text{Loss}}{\\text{CP}}\\right) \\times 100$
* **Marked Price (MP) & Discount:**
  * $\\text{Discount} = \\text{MP} - \\text{SP}$
  * $\\text{Discount \\%} = \\left(\\frac{\\text{Discount}}{\\text{MP}}\\right) \\times 100$

#### 3. Standard Exam Shortcuts
> **Trick 1:** If price of a commodity increases by $R\\%$, then the reduction in consumption so as not to increase expenditure is:
> $$\\left(\\frac{R}{100 + R} \\times 100\\right)\\%$$

> **Trick 2:** If two items are sold at the same selling price, one at $x\\%$ profit and the other at $x\\%$ loss, there is ALWAYS an overall loss given by:
> $$\\text{Loss \\%} = \\left(\\frac{x}{10}\\right)^2 = \\frac{x^2}{100}\\%$$
""",
            1
        ),
        (
            "Aptitude",
            "Quantitative Aptitude",
            "Time, Speed, Distance & Trains",
            "15 min read",
            "Essential concepts of relative speed, train crossing stationary & moving objects, boats & streams, and average speed.",
            """### Key Principles & Shortcut Formulas

#### 1. Unit Conversion
* **km/h to m/s:** Multiply by $\\frac{5}{18}$
* **m/s to km/h:** Multiply by $\\frac{18}{5}$

#### 2. Average Speed
* When distance is constant and speeds are $u$ and $v$:
  $$\\text{Average Speed} = \\frac{2uv}{u + v}$$
* When time intervals are equal:
  $$\\text{Average Speed} = \\frac{u + v}{2}$$

#### 3. Relative Speed
* **Same Direction:** Relative Speed = $|u - v|$
* **Opposite Direction:** Relative Speed = $u + v$

#### 4. Problems on Trains
* **Train crossing a pole/person:** Distance = Length of Train ($L_t$)
  $$t = \\frac{L_t}{v}$$
* **Train crossing a platform/bridge ($L_p$):** Distance = $L_t + L_p$
  $$t = \\frac{L_t + L_p}{v}$$
* **Two trains crossing each other:** Distance = $L_1 + L_2$
  $$t = \\frac{L_1 + L_2}{v_1 \\pm v_2} \\quad (-\\text{ if same direction, } +\\text{ if opposite})$$

#### 5. Boats and Streams
* Speed in Still Water = $B$, Speed of Stream = $S$
* **Downstream Speed ($D$):** $B + S$
* **Upstream Speed ($U$):** $B - S$
* $B = \\frac{D + U}{2}, \\quad S = \\frac{D - U}{2}$
""",
            2
        ),
        (
            "Aptitude",
            "Quantitative Aptitude",
            "Time & Work, Pipes & Cisterns",
            "10 min read",
            "Unitary method, LCM method, efficiency ratios, alternate day problems, and leak problems in pipes.",
            """### The LCM Method (Fastest Approach)

#### 1. The Core Concept
* Always calculate Total Work as the **LCM of days** taken by individual workers.
* **Efficiency (Work done per day)** = $\\frac{\\text{Total Work}}{\\text{Days taken}}$
* **Days needed** = $\\frac{\\text{Total Work}}{\\text{Combined Efficiency}}$

#### 2. Example:
* A can do a work in 12 days, B in 15 days, C in 20 days.
* $\\text{LCM}(12, 15, 20) = 60$ units of total work.
* Efficiency of A = $60/12 = 5$ units/day
* Efficiency of B = $60/15 = 4$ units/day
* Efficiency of C = $60/20 = 3$ units/day
* Combined Efficiency = $5 + 4 + 3 = 12$ units/day
* Time taken together = $60 / 12 = 5$ days!

#### 3. Work & Wages
* Wages are distributed strictly in proportion to the **work done** (or efficiency when working for equal days).

#### 4. Pipes & Cisterns
* Inflow pipes contribute positive work ($+E$).
* Drainage / Leak pipes contribute negative work ($-E$).
""",
            3
        ),

        # APTITUDE - Logical Reasoning
        (
            "Aptitude",
            "Logical Reasoning",
            "Syllogisms & Deductive Logic",
            "10 min read",
            "Rules of Syllogisms, Venn diagram approaches, 'Some', 'All', 'No', and 'Some Not' deductions, plus Either-Or cases.",
            """### Syllogism Rules & Techniques

#### 1. Standard Quantifiers
1. **Universal Affirmative (All A are B):** Set A is completely inside Set B.
2. **Universal Negative (No A is B):** Set A and Set B have zero intersection.
3. **Particular Affirmative (Some A are B):** Set A and Set B have at least one common element.
4. **Particular Negative (Some A are not B):** At least one element of A is not in B.

#### 2. Golden Rules for Syllogisms
* If both statements are affirmative (+), conclusions must be affirmative.
* If one statement is negative (-), any valid conclusion must be negative.
* Two negative premises yield **no valid conclusion**.
* Two particular premises (e.g. Some A is B + Some B is C) yield **no definite conclusion**.

#### 3. The 'Either-Or' Complementary Pairs
A pair is 'Either-Or' if:
1. Both individual conclusions do not follow definitely.
2. Both share the same subject and predicate.
3. One is affirmative and one is negative:
   * **Pair 1:** 'Some' + 'No'
   * **Pair 2:** 'All' + 'Some Not'
""",
            4
        ),
        (
            "Aptitude",
            "Logical Reasoning",
            "Blood Relations & Coding Decoding",
            "8 min read",
            "Generation tree diagrams, standard notation symbols, letter shift patterns, and matrix deciphering.",
            """### Blood Relations: Family Tree Method

#### 1. Standard Notations
* Male: $[+]$ or Square $\\square$
* Female: $[-]$ or Circle $\\bigcirc$
* Married Couple: Double horizontal line $(A = B)$
* Siblings: Single horizontal line $(A - B)$
* Generational Gap: Vertical line (Parent above, child below)

#### 2. Key Generational Relationships
* Paternal: Father's side (Paternal Uncle = Father's Brother)
* Maternal: Mother's side (Maternal Aunt = Mother's Sister)
* Cousin: Son/Daughter of Uncle/Aunt (never brother/sister)
* Brother-in-law: Spouse's brother OR Sister's husband

#### 3. Coding - Decoding Quick Tricks
* **EJOTY rule:** Position markers $E(5), J(10), O(15), T(20), Y(25)$
* **Opposite Letters (Sum = 27):**
  * $A \\leftrightarrow Z$ (AZad)
  * $B \\leftrightarrow Y$ (BoY)
  * $C \\leftrightarrow X$ (CruX)
  * $D \\leftrightarrow W$ (Dew)
  * $E \\leftrightarrow V$ (EVen)
  * $M \\leftrightarrow N$ (MaN)
""",
            5
        ),

        # TECHNICAL - DBMS
        (
            "Technical",
            "DBMS",
            "Database Normalization & SQL Masterclass",
            "18 min read",
            "Deep dive into 1NF, 2NF, 3NF, BCNF, SQL Joins, Indexing (B-Tree), ACID properties, and Transaction Isolation Levels.",
            """### 1. Database Normalization

#### Why Normalize?
Eliminate data redundancy, avoid insertion/update/deletion anomalies, and ensure data integrity.

* **1NF (First Normal Form):**
  * Each column must have atomic (indivisible) values.
  * No repeating groups or arrays.
  * Each record must have a unique identifier (Primary Key).

* **2NF (Second Normal Form):**
  * Must be in 1NF.
  * **No Partial Dependency:** Every non-prime attribute must be fully functionally dependent on the entire Candidate Key (not a proper subset).

* **3NF (Third Normal Form):**
  * Must be in 2NF.
  * **No Transitive Dependency:** If $X \\rightarrow Y$ and $Y \\rightarrow Z$, then non-prime $Z$ must not depend on $X$ through non-prime $Y$.
  * Formal condition: For every FD $X \\rightarrow A$, either $X$ is a super key or $A$ is a prime attribute.

* **BCNF (Boyce-Codd Normal Form):**
  * Strictly: For every non-trivial functional dependency $X \\rightarrow A$, **$X$ MUST be a super key**.

---

### 2. ACID Properties
1. **Atomicity:** All operations within a transaction succeed, or all are rolled back ("All or Nothing").
2. **Consistency:** Database transitions from one valid state to another, satisfying all constraints.
3. **Isolation:** Concurrent transactions execute without interfering with each other.
4. **Durability:** Once committed, changes survive system crashes and power failures.

---

### 3. Transaction Isolation Levels & Read Phenomena
| Isolation Level | Dirty Read | Non-Repeatable Read | Phantom Read |
|---|---|---|---|
| **Read Uncommitted** | Possible | Possible | Possible |
| **Read Committed** | Prevented | Possible | Possible |
| **Repeatable Read** | Prevented | Prevented | Possible |
| **Serializable** | Prevented | Prevented | Prevented |

---

### 4. SQL Joins Illustrated
```sql
-- Inner Join: Rows matching both tables
SELECT e.name, d.department_name
FROM employees e
INNER JOIN departments d ON e.dept_id = d.id;

-- Left Outer Join: All employees, plus dept if matched
SELECT e.name, d.department_name
FROM employees e
LEFT JOIN departments d ON e.dept_id = d.id;

-- Group By with Having (Filter aggregated result)
SELECT dept_id, COUNT(*) as emp_count, AVG(salary) as avg_sal
FROM employees
GROUP BY dept_id
HAVING AVG(salary) > 75000;
```
""",
            6
        ),

        # TECHNICAL - Operating Systems
        (
            "Technical",
            "Operating Systems",
            "Processes, Threads, Deadlocks & Memory Management",
            "16 min read",
            "Process vs Thread, PCB, CPU Scheduling, Deadlock Coffman conditions & Banker's Algorithm, Virtual Memory, and Paging.",
            """### 1. Process vs. Thread

| Attribute | Process | Thread (Lightweight Process) |
|---|---|---|
| **Definition** | An executing program with isolated resources | Smallest unit of execution inside a process |
| **Memory** | Own independent virtual address space | Shares code, data, and heap with peer threads |
| **Creation Overhead** | High (fork/exec requires memory allocation) | Low (shares existing process space) |
| **Context Switching** | Slower (requires flushing TLB, page tables) | Faster (page tables remain identical) |
| **Communication** | IPC (Pipes, Sockets, Shared Memory) | Direct memory access via shared variables |

---

### 2. Deadlocks: The 4 Coffman Conditions
A deadlock can arise if and ONLY if all 4 conditions hold simultaneously:
1. **Mutual Exclusion:** At least one resource is held in a non-shareable mode.
2. **Hold and Wait:** A process is holding at least one resource and requesting additional resources held by others.
3. **No Preemption:** Resources cannot be forcibly taken from a process holding them.
4. **Circular Wait:** A closed chain of processes exists: $P_0$ waits for $P_1$, $P_1$ waits for $P_2$, ..., $P_n$ waits for $P_0$.

#### Deadlock Handling:
* **Deadlock Prevention:** Violate at least one of the 4 Coffman conditions (e.g. enforce strict resource ordering).
* **Deadlock Avoidance:** Banker's Algorithm evaluates safe states before granting resources.
* **Deadlock Detection & Recovery:** Resource allocation graph cycle detection; kill process or preempt resource.
* **Ostrich Algorithm:** Ignore the problem if it happens rarely (standard in modern general OS).

---

### 3. Virtual Memory & Paging
* **Logical vs Physical Address:** CPU generates logical addresses, converted to physical addresses via the Memory Management Unit (MMU) using the Page Table.
* **Page Fault:** Occurs when a program tries to access a page that is mapped in address space but not currently loaded in physical RAM.
* **Thrashing:** When the OS spends more time swapping pages in and out of disk than executing instructions.
* **Page Replacement Algorithms:** FIFO, LRU (Least Recently Used), Optimal (Bélády's Anomaly affects FIFO, not LRU/Optimal).
""",
            7
        ),

        # TECHNICAL - Computer Networks
        (
            "Technical",
            "Computer Networks",
            "OSI Layers, TCP/IP, DNS & HTTP/HTTPS",
            "14 min read",
            "OSI 7-layer model, TCP 3-way handshake & 4-way termination, UDP vs TCP, DNS resolution walkthrough, and TLS/HTTPS handshake.",
            """### 1. The OSI 7 Layers vs TCP/IP

| OSI Layer | Protocol Data Unit | Key Protocols / Devices | Core Function |
|---|---|---|---|
| **7. Application** | Data | HTTP, HTTPS, FTP, DNS, SMTP | User interface & network services |
| **6. Presentation** | Data | SSL/TLS, JPEG, ASCII | Encryption, compression, serialization |
| **5. Session** | Data | NetBIOS, RPC, Sockets | Session establishment & maintenance |
| **4. Transport** | Segment (TCP) / Datagram (UDP) | TCP, UDP | End-to-end delivery, ports, reliability |
| **3. Network** | Packet | IP (IPv4, IPv6), ICMP, Routers | Routing, IP addressing, best path selection |
| **2. Data Link** | Frame | Ethernet, MAC, Switches | Node-to-node hop, error detection (CRC) |
| **1. Physical** | Bits | Cables, Fiber, Hubs, Radio | Physical transmission of raw bit streams |

---

### 2. TCP vs. UDP
* **TCP (Transmission Control Protocol):** Connection-oriented, reliable (guaranteed order & delivery via ACK), flow control (sliding window), congestion control. Used for: Web (HTTP/HTTPS), Email, File transfer.
* **UDP (User Datagram Protocol):** Connectionless, lightweight, low-latency, no guarantee of delivery or order. Used for: DNS lookups, Video streaming (WebRTC), Online multiplayer gaming, VoIP.

---

### 3. TCP 3-Way Handshake
1. **Client $\\rightarrow$ Server:** `SYN` (Sequence Number = $X$)
2. **Server $\\rightarrow$ Client:** `SYN-ACK` (Seq = $Y$, Ack = $X+1$)
3. **Client $\\rightarrow$ Server:** `ACK` (Seq = $X+1$, Ack = $Y+1$)
*Connection is now ESTABLISHED!*

---

### 4. What Happens When You Type google.com in a Browser?
1. **Browser Cache Check:** Inspects browser cache, OS hosts file, local resolver cache.
2. **DNS Resolution:** Recursive query to Local DNS Server $\\rightarrow$ Root Nameserver $\\rightarrow$ TLD (.com) Server $\\rightarrow$ Authoritative Nameserver $\\rightarrow$ returns IP address.
3. **TCP Connection:** 3-way handshake between client IP and server IP on port 443.
4. **TLS/SSL Handshake:** Client Hello, Server Hello, Certificate verification, symmetric key generation.
5. **HTTP Request:** Browser sends `GET / HTTP/2` request.
6. **Server Response:** Server generates HTML response with status code `200 OK`.
7. **DOM Rendering:** Browser parses HTML, fetches CSS/JS/images, builds DOM and Render tree, and paints pixels.
""",
            8
        ),

        # TECHNICAL - System Design & OOP
        (
            "Technical",
            "System Design & OOP",
            "SOLID Principles & High-Level System Architecture",
            "15 min read",
            "Clean architecture with SOLID principles, Caching patterns, Load Balancing, Database Sharding, and CAP Theorem.",
            """### 1. The SOLID Principles

1. **S - Single Responsibility Principle (SRP):**
   * A class should have one, and only one, reason to change.
2. **O - Open/Closed Principle (OCP):**
   * Software entities should be open for extension, but closed for modification. Use interfaces and inheritance/composition.
3. **L - Liskov Substitution Principle (LSP):**
   * Subtypes must be substitutable for their base types without altering system correctness.
4. **I - Interface Segregation Principle (ISP):**
   * Clients should not be forced to depend upon interfaces that they do not use. Split large interfaces into smaller, targeted ones.
5. **D - Dependency Inversion Principle (DIP):**
   * High-level modules should not depend on low-level modules; both should depend on abstractions.

---

### 2. High-Level System Design Fundamentals

#### The CAP Theorem
In any distributed asynchronous data store, you can guarantee at most **two out of three**:
* **Consistency (C):** Every read receives the most recent write or an error.
* **Availability (A):** Every non-failing node returns a non-error response (without guarantee that it contains the newest write).
* **Partition Tolerance (P):** The system continues to operate despite arbitrary network dropped messages.
> *In real networks, network partitions (P) are inevitable. Hence, distributed systems must choose between **CP** (e.g. HBase, MongoDB) or **AP** (e.g. Cassandra, DynamoDB).*

#### Caching Strategies
* **Cache-Aside (Lazy Loading):** App checks cache; if miss, reads from DB and writes to cache.
* **Write-Through:** App writes to cache, and cache synchronously writes to DB.
* **Write-Back (Write-Behind):** App writes to cache immediately; cache asynchronously flushes writes to DB in batches.
* **Eviction Policies:** LRU (Least Recently Used), LFU (Least Frequently Used), FIFO.

#### Load Balancing Algorithms
* **Round Robin / Weighted Round Robin**
* **Least Connections**
* **IP Hash (Sticky Sessions)**
* **Consistent Hashing (Used in distributed caches and DHTs to minimize re-indexing on node addition/removal)**
""",
            9
        ),

        # HR INTERVIEW PREPARATION
        (
            "HR",
            "HR & Behavioral",
            "Mastering the STAR Method for Behavioral Rounds",
            "12 min read",
            "How to structure stories using Situation, Task, Action, and Result to ace Amazon Leadership Principles and Google Googleyness.",
            """### The STAR Method Framework

When an interviewer asks: *"Tell me about a time when you faced a technical disagreement with a teammate"* or *"Describe a project where requirements changed last minute"*, standard rambling answers will fail. Use **STAR**:

```
[S] Situation  -> Set the scene: context, constraints, and stakes (15%)
[T] Task       -> What was your specific responsibility? What was at risk? (15%)
[A] Action     -> The steps YOU took: technical decisions, communication, initiative (55%)
[R] Result     -> Quantifiable outcome, business impact, and key learnings (15%)
```

---

### High-Impact Example: "Describe a Time You Solved a Difficult Bug"

* **Situation:** During the final week before releasing our college hackathon food-delivery web app, our live demo began crashing whenever more than 15 concurrent users added items to their cart.
* **Task:** As the backend lead, I had to diagnose the latency spike and root cause within 24 hours without disrupting ongoing frontend testing.
* **Action:** I used APM logging and PostgreSQL query analyzers to pinpoint unindexed subqueries on our cart items table. I implemented a Redis caching layer for active user cart sessions and added database composite indexes on `(user_id, status)`. Furthermore, I set up a Locust load-testing script to stress-test the fix up to 200 concurrent simulated users.
* **Result:** Server response times dropped from 3.2 seconds down to 48 milliseconds. The presentation ran flawlessly, handling 50 live judges simultaneously, and our project was awarded 1st place among 40 participating teams.

---

### Pro-Tips for HR Rounds:
1. Always speak in **"I"** rather than **"We"** when describing actions. Interviewers evaluate YOU, not your team.
2. Have **5 versatile stories** prepped in advance:
   * A major technical accomplishment.
   * A failure or mistake and how you recovered.
   * A conflict with a peer/manager and how you resolved it diplomatically.
   * A time you learned a new technology under tight deadlines.
   * A time you showed leadership or mentored someone.
""",
            10
        ),
        (
            "HR",
            "HR & Behavioral",
            "Top 10 Classic HR Questions & Model Answers",
            "14 min read",
            "Exact scripts and strategies for 'Tell me about yourself', 'Why should we hire you?', 'Strengths/Weaknesses', and Salary negotiation.",
            """### 1. "Tell Me About Yourself"
* **Structure:** **Present $\\rightarrow$ Past $\\rightarrow$ Future** (Keep it to 90 seconds)
* **Model Answer:**
> "I am a passionate software engineer with a strong foundation in data structures, algorithms, and full-stack web systems. Currently, I have been building scalable applications using React, Python FastAPI, and PostgreSQL, including an end-to-end candidate preparation platform that handles interactive quiz evaluations and topic-wise sheets. Previously, I honed my fundamentals through competitive programming, solving 300+ problems on LeetCode and leading my college hackathon team to top honors. What excites me most about [Company Name] is your work on high-scale distributed systems, and I'm eager to bring my strong problem-solving and rapid learning capabilities to contribute to your engineering team."

---

### 2. "What Is Your Greatest Weakness?"
* **Formula:** Name a real professional weakness + Explain the concrete system or habit you adopted to overcome it.
* **Model Answer:**
> "Earlier, I had a tendency to dive straight into writing code without spending enough time documenting edge cases and mapping out component architecture first. While this felt fast initially, it sometimes led to refactoring mid-way. Over the past year, I adopted a strict habit of writing lightweight design docs and drafting test cases on paper before touching code. This has significantly reduced bugs and made my code reviews much smoother."

---

### 3. "Why Do You Want to Join Us?"
* **Formula:** Show specific company knowledge + align with personal career goals + how you add value.
* **Avoid generic answers like:** "Because you are a big multinational company."
* **Say instead:**
> "I've been following your recent tech blog posts on how you migrated your core transactional ledger to event-driven Kafka architecture. The engineering challenges you tackle at this scale—processing millions of events with sub-second SLA—is exactly the high-impact environment where I want to push my limits. Moreover, your engineering culture emphasizes mentorship and ownership for early-career developers, which makes this the ideal team for me to grow and contribute."

---

### 4. "Do You Have Any Questions for Me?" (Never say 'No'!)
Great questions to ask the interviewer:
1. *"What does a typical day or sprint cycle look like for an engineer on this team?"*
2. *"What are the biggest technical or architectural challenges the team is currently aiming to solve this quarter?"*
3. *"How does the team foster continuous learning and engineering best practices?"*
""",
            11
        )
    ]

    for p in prep_topics:
        cursor.execute("""
        INSERT INTO prep_topics (category, sub_category, title, read_time, summary, content, order_idx)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """, p)

    # -------------------------------------------------------------
    # Seeding Practice Questions / MCQs
    # -------------------------------------------------------------
    print("Seeding Practice Problems...")
    questions = [
        # Aptitude - Quants
        (
            "Aptitude",
            "Quantitative Aptitude",
            "Easy",
            "A man buys a cycle for ₹1400 and sells it at a loss of 15%. What is the selling price of the cycle?",
            json.dumps(["₹1190", "₹1200", "₹1160", "₹1250"]),
            0,
            "SP = CP × (100 - Loss%)/100 = 1400 × (85/100) = 14 × 85 = ₹1190.",
            json.dumps(["Profit & Loss", "Percentages"])
        ),
        (
            "Aptitude",
            "Quantitative Aptitude",
            "Medium",
            "A train 240 m long passes a pole in 24 seconds. How long will it take to pass a platform 650 m long?",
            json.dumps(["65 seconds", "89 seconds", "100 seconds", "75 seconds"]),
            1,
            "Speed of the train = Length of train / Time = 240 / 24 = 10 m/s. Total distance to cross platform = 240 + 650 = 890 m. Time = 890 / 10 = 89 seconds.",
            json.dumps(["Time Speed Distance", "Trains"])
        ),
        (
            "Aptitude",
            "Quantitative Aptitude",
            "Medium",
            "A can do a piece of work in 15 days, and B can do it in 20 days. If they work on it together for 4 days, what fraction of work is left?",
            json.dumps(["7/15", "8/15", "11/15", "1/4"]),
            1,
            "Total work = LCM(15, 20) = 60 units. A's efficiency = 4 units/day, B's efficiency = 3 units/day. Combined in 4 days = (4 + 3) × 4 = 28 units. Remaining work = 60 - 28 = 32 units. Fraction remaining = 32 / 60 = 8/15.",
            json.dumps(["Time & Work", "Fractions"])
        ),
        (
            "Aptitude",
            "Quantitative Aptitude",
            "Hard",
            "Two pipes A and B can fill a tank in 20 and 30 minutes respectively. A third pipe C empties it in 15 minutes. If all three are opened together, how long will it take to fill the tank?",
            json.dumps(["60 minutes", "45 minutes", "90 minutes", "The tank will never fill"]),
            0,
            "Total capacity = LCM(20, 30, 15) = 60 units. Efficiency of A = +3, B = +2, C = -4. Combined efficiency = 3 + 2 - 4 = +1 unit/min. Time required = 60 / 1 = 60 minutes.",
            json.dumps(["Pipes and Cisterns", "Work"])
        ),

        # Aptitude - Logical
        (
            "Aptitude",
            "Logical Reasoning",
            "Medium",
            "Pointing to a photograph, Rohit said, 'She is the daughter of my grandfather's only son.' How is the girl in the photograph related to Rohit?",
            json.dumps(["Daughter", "Sister", "Cousin", "Mother"]),
            1,
            "Rohit's grandfather's only son is Rohit's Father. The daughter of Rohit's father is Rohit's sister.",
            json.dumps(["Blood Relations", "Deduction"])
        ),
        (
            "Aptitude",
            "Logical Reasoning",
            "Easy",
            "In a certain code, COMPUTER is written as RFUVQNPC. How is MEDICINE written in that code?",
            json.dumps(["EOJDJEFM", "EOJDEJFM", "MFEJDJOE", "EOJDJFEM"]),
            0,
            "The first and last letters are swapped and reversed in pairs with +1 shift. Applying the exact pattern to MEDICINE produces EOJDJEFM.",
            json.dumps(["Coding-Decoding", "Patterns"])
        ),

        # Technical - DBMS
        (
            "Technical",
            "DBMS",
            "Medium",
            "Which normal form is based on the concept of 'Full Functional Dependency' and eliminates partial dependencies?",
            json.dumps(["First Normal Form (1NF)", "Second Normal Form (2NF)", "Third Normal Form (3NF)", "Boyce-Codd Normal Form (BCNF)"]),
            1,
            "2NF requires the relation to be in 1NF and that no non-prime attribute is partially dependent on any candidate key (eliminating partial dependencies).",
            json.dumps(["DBMS", "Normalization", "2NF"])
        ),
        (
            "Technical",
            "DBMS",
            "Hard",
            "Which Transaction Isolation Level prevents Dirty Reads and Non-Repeatable Reads, but still allows Phantom Reads?",
            json.dumps(["Read Uncommitted", "Read Committed", "Repeatable Read", "Serializable"]),
            2,
            "Repeatable Read prevents Dirty Reads and Non-Repeatable Reads. Phantom Reads can only be completely eliminated at the Serializable isolation level.",
            json.dumps(["DBMS", "Transactions", "Isolation"])
        ),
        (
            "Technical",
            "DBMS",
            "Easy",
            "Which of the following SQL clauses is used to filter records resulting from an aggregate function?",
            json.dumps(["WHERE", "HAVING", "GROUP BY", "ORDER BY"]),
            1,
            "The HAVING clause was added to SQL because the WHERE keyword could not be used with aggregate functions.",
            json.dumps(["SQL", "Aggregation"])
        ),

        # Technical - OS
        (
            "Technical",
            "Operating Systems",
            "Medium",
            "Which of the following is NOT a necessary condition for a deadlock to occur (Coffman conditions)?",
            json.dumps(["Mutual Exclusion", "Hold and Wait", "Preemption of resources", "Circular Wait"]),
            2,
            "The condition is 'No Preemption' (resources cannot be forcibly taken away). Having preemption actually PREVENTS deadlocks.",
            json.dumps(["Operating Systems", "Deadlocks"])
        ),
        (
            "Technical",
            "Operating Systems",
            "Medium",
            "What is Bélády's Anomaly in operating systems?",
            json.dumps([
                "CPU utilization drops while paging increases",
                "Increasing the number of page frames results in an increase in the number of page faults",
                "Deadlock occurring in circular memory allocation",
                "Processes starving indefinitely in priority scheduling"
            ]),
            1,
            "Bélády's anomaly is the phenomenon in which increasing the number of page frames results in an increase in the number of page faults for certain memory access patterns (most commonly seen in FIFO page replacement).",
            json.dumps(["Operating Systems", "Paging", "Virtual Memory"])
        ),

        # Technical - Networks
        (
            "Technical",
            "Computer Networks",
            "Easy",
            "At which OSI layer does the IP (Internet Protocol) operate?",
            json.dumps(["Data Link Layer", "Transport Layer", "Network Layer", "Session Layer"]),
            2,
            "IP operates at Layer 3 (Network Layer), handling logical addressing and packet routing across networks.",
            json.dumps(["Networks", "OSI Model"])
        ),
        (
            "Technical",
            "Computer Networks",
            "Medium",
            "What flags are sent in sequence during the classic TCP 3-way handshake to establish a connection?",
            json.dumps(["SYN -> ACK -> SYN-ACK", "SYN -> SYN-ACK -> ACK", "ACK -> SYN -> SYN-ACK", "SYN -> FIN -> ACK"]),
            1,
            "Client sends SYN; Server responds with SYN-ACK; Client replies with ACK to establish connection.",
            json.dumps(["Networks", "TCP", "Handshake"])
        ),

        # Technical - OOP / System Design
        (
            "Technical",
            "System Design & OOP",
            "Medium",
            "In object-oriented design, what does the 'Liskov Substitution Principle' state?",
            json.dumps([
                "A class should only have one reason to change",
                "Derived classes must be substitutable for their base classes without altering the correctness of the program",
                "Depend on abstractions, not on concretions",
                "Many specific interfaces are better than one general-purpose interface"
            ]),
            1,
            "LSP states that objects of a superclass should be replaceable with objects of its subclasses without breaking the application logic.",
            json.dumps(["OOP", "SOLID", "Architecture"])
        ),

        # HR / Behavioral
        (
            "HR",
            "HR & Behavioral",
            "Easy",
            "What does the acronym 'STAR' stand for in behavioral interview evaluations?",
            json.dumps([
                "Strategy, Timeline, Action, Review",
                "Situation, Task, Action, Result",
                "Skill, Training, Aptitude, Readiness",
                "Scope, Target, Accomplishment, Resolution"
            ]),
            1,
            "STAR stands for Situation, Task, Action, and Result - the globally recognized framework for structured behavioral responses.",
            json.dumps(["HR", "Interview Prep", "STAR"])
        )
    ]

    for q in questions:
        cursor.execute("""
        INSERT INTO prep_questions (category, sub_category, difficulty, question, options, correct_index, explanation, tags)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, q)

    # -------------------------------------------------------------
    # Seeding Companies Hiring Process
    # -------------------------------------------------------------
    print("Seeding Companies Hiring Process...")
    companies = [
        (
            "Google",
            "google",
            "Big Tech / FAANG",
            "Organizing the world's information and building at planet scale.",
            "₹25 - ₹55 LPA (SWE L3/L4)",
            "Hard",
            json.dumps({
                "cgpa": "No strict cutoff, generally 7.0+ CGPA preferred for campus drives",
                "backlogs": "No active backlogs allowed during onboarding",
                "branches": "B.Tech/B.E, M.Tech, MS in CS, IT, ECE, Mathematics or related fields",
                "batches": "2024, 2025, 2026 Batch Graduates",
                "notes": "Emphasis is overwhelmingly on algorithmic excellence, clean code, edge-case analysis, and Googleyness."
            }),
            json.dumps([
                {
                    "round_num": 1,
                    "name": "Online Assessment (OA)",
                    "duration": "90 Minutes",
                    "questions": "2 LeetCode Medium/Hard algorithmic questions",
                    "negative_marking": "No",
                    "platform": "HackerEarth / Google Internal Sandbox",
                    "focus": "Dynamic Programming, Graph algorithms, Trees, Greedy"
                },
                {
                    "round_num": 2,
                    "name": "Technical Phone Screen",
                    "duration": "45 Minutes",
                    "questions": "1-2 Coding questions with live shared Google Doc",
                    "negative_marking": "N/A",
                    "platform": "Google Meet + Google Docs (No auto-complete)",
                    "focus": "Data Structures, Time/Space complexities, dry run test cases"
                },
                {
                    "round_num": 3,
                    "name": "Onsite Virtual Loop (3 Technical Rounds)",
                    "duration": "45 Mins each (3 separate rounds)",
                    "questions": "Deep problem solving on Trees, Graphs, DP, Trie, Sliding Window",
                    "negative_marking": "N/A",
                    "platform": "Google Meet",
                    "focus": "Algorithm optimization from O(N^2) to O(N log N), edge-case handling"
                },
                {
                    "round_num": 4,
                    "name": "Googleyness & Leadership Round",
                    "duration": "45 Minutes",
                    "questions": "Behavioral scenarios, handling ambiguity, teamwork, ethical dilemmas",
                    "negative_marking": "N/A",
                    "platform": "Google Meet",
                    "focus": "Collaboration, intellectual humility, doing the right thing"
                }
            ]),
            json.dumps({
                "dsa_weightage": "85%",
                "core_cs_weightage": "10%",
                "behavioral_weightage": "5%",
                "key_syllabus_topics": [
                    "Dynamic Programming (1D, 2D, Knapsack, Digit DP)",
                    "Graphs (Dijkstra, Topological Sort, Disjoint Set Union / Kruskal)",
                    "Binary Search on Answer / Monotonicity",
                    "Tries, Segment Trees, Priority Queues",
                    "Clean, production-ready code with meaningful variable names"
                ]
            }),
            json.dumps([
                "Coding Round 1 (Data Structures & Algorithms)",
                "Coding Round 2 (Algorithms & Data Structures)",
                "Coding Round 3 (Advanced Problem Solving / System Design for L4+)",
                "Googleyness & Leadership Interview"
            ]),
            json.dumps(["Dynamic Programming", "Graphs (BFS/DFS/Shortest Path)", "Binary Search", "Trees", "Sliding Window", "Googleyness"]),
            json.dumps([
                "Given a list of words, find the longest word that can be built one character at a time by other words in the list.",
                "Design a logger rate limiter that prints messages at most once every 10 seconds.",
                "Find the shortest path in a 2D grid with obstacle elimination (K obstacles allowed).",
                "Serialize and Deserialize a Binary Tree."
            ]),
            json.dumps([
                "Write code directly on Google Docs without syntax highlighting or compiler assistance to practice.",
                "Always ask clarifying questions before writing a single line of code (e.g. Can input array have negative numbers? Can it fit in memory?).",
                "State brute force first, discuss time/space complexity, and then transition smoothly into optimal approaches.",
                "Dry run your code with a sample test case manually line-by-line before declaring you are done."
            ])
        ),
        (
            "Amazon",
            "amazon",
            "Big Tech / FAANG",
            "Earth's most customer-centric company and cloud pioneer.",
            "₹28 - ₹45 LPA (SDE 1)",
            "Hard",
            json.dumps({
                "cgpa": "6.5+ CGPA or 65% in B.Tech/BE/MCA",
                "backlogs": "Zero active backlogs at the time of interview",
                "branches": "All Engineering branches eligible, CSE/IT preferred",
                "batches": "2025, 2026 Batch",
                "notes": "Every interview round evaluates 50% DSA and 50% Amazon 16 Leadership Principles (LPs)."
            }),
            json.dumps([
                {
                    "round_num": 1,
                    "name": "Amazon OA (Online Assessment)",
                    "duration": "90 - 105 Minutes",
                    "questions": "2 Coding questions + Work Style Assessment (LP scenarios)",
                    "negative_marking": "No",
                    "platform": "HackerRank / Mettl",
                    "focus": "Arrays, Strings, HashMaps, Heaps, Trees"
                },
                {
                    "round_num": 2,
                    "name": "Technical Round 1",
                    "duration": "60 Minutes",
                    "questions": "1-2 Coding questions + 2 Leadership Principle questions",
                    "negative_marking": "N/A",
                    "platform": "Amazon Chime / LiveCode",
                    "focus": "Binary Trees, Heaps, Graph BFS/DFS, Customer Obsession LP"
                },
                {
                    "round_num": 3,
                    "name": "Technical Round 2",
                    "duration": "60 Minutes",
                    "questions": "Complex DSA + Object-Oriented Design (LLD)",
                    "negative_marking": "N/A",
                    "platform": "Amazon Chime",
                    "focus": "Design a Parking Lot, Movie Ticket Booking, Ownership LP"
                },
                {
                    "round_num": 4,
                    "name": "Bar Raiser Round",
                    "duration": "60 Minutes",
                    "questions": "DSA + Deep Leadership Principle interrogation",
                    "negative_marking": "N/A",
                    "platform": "Amazon Chime",
                    "focus": "Conducted by an independent senior leader outside the hiring team"
                }
            ]),
            json.dumps({
                "dsa_weightage": "50%",
                "leadership_principles": "40%",
                "system_design_lld": "10%",
                "key_syllabus_topics": [
                    "Trees & Binary Search Trees (LCA, Diameter, Level Order)",
                    "Heaps & Priority Queues (Top K Frequent, Merge K Sorted Lists)",
                    "Dynamic Programming (Coin Change, Word Break)",
                    "Object-Oriented Design (SOLID, Design Patterns: Factory, Singleton, Strategy)",
                    "Amazon 16 Leadership Principles (Customer Obsession, Ownership, Bias for Action)"
                ]
            }),
            json.dumps([
                "Technical Interview 1 (DSA + LPs)",
                "Technical Interview 2 (DSA + LLD + LPs)",
                "Technical Interview 3 (DSA / Problem Solving + LPs)",
                "Bar Raiser Round (Strict threshold keeper)"
            ]),
            json.dumps(["Binary Trees", "Heaps", "Graphs", "Dynamic Programming", "LLD / OOD", "Amazon Leadership Principles"]),
            json.dumps([
                "Rotting Oranges (BFS on Grid)",
                "LRU Cache implementation with O(1) get and put",
                "Word Ladder (Shortest transformation sequence)",
                "Trapping Rain Water",
                "LP Question: Tell me about a time you had to make a decision with incomplete data (Bias for Action)."
            ]),
            json.dumps([
                "Master all 16 Amazon Leadership Principles. Have 2 unique STAR stories prepared for each principle.",
                "In coding rounds, code must be modular, handle null pointers, and have clean variable naming.",
                "The Bar Raiser holds veto power: perform exceptionally well on behavioral communication and trade-off analysis."
            ])
        ),
        (
            "TCS",
            "tcs",
            "Mass IT / Service",
            "Global leader in IT services, consulting, and digital business solutions.",
            "₹3.36 LPA (Ninja), ₹7.0 LPA (Digital), ₹9-11.5 LPA (Prime)",
            "Easy-Medium",
            json.dumps({
                "cgpa": "Minimum 60% or 6.0 CGPA throughout 10th, 12th, Diploma, and Graduation",
                "backlogs": "Maximum 1 active backlog permitted at the time of appearing",
                "branches": "All Engineering branches, B.Sc (IT/CS), BCA, MCA",
                "batches": "2025, 2026 Batch",
                "notes": "TCS National Qualifier Test (NQT) determines placement into Ninja, Digital, or Prime cadred offers based on percentile score."
            }),
            json.dumps([
                {
                    "round_num": 1,
                    "name": "TCS NQT Part A: Foundation Cognitive Section",
                    "duration": "75 Minutes",
                    "questions": "Numerical Ability (20 Q), Verbal Ability (25 Q), Reasoning Ability (20 Q)",
                    "negative_marking": "No negative marking",
                    "platform": "TCS iON platform",
                    "focus": "Aptitude, Percentages, Syllogisms, Para Jumbles"
                },
                {
                    "round_num": 2,
                    "name": "TCS NQT Part B: Advanced Section (Digital & Prime Qualifier)",
                    "duration": "90 Minutes",
                    "questions": "Advanced Quantitative (15 Q), Advanced Reasoning (15 Q), Advanced Coding (2 Q)",
                    "negative_marking": "No",
                    "platform": "TCS iON platform",
                    "focus": "Higher-level logic + 1 Medium coding problem + 1 Hard coding problem"
                },
                {
                    "round_num": 3,
                    "name": "Technical Interview (TR)",
                    "duration": "30 - 45 Minutes",
                    "questions": "Resume grilling, Final year project, Core CS (DBMS, OS, OOP), Basic Coding",
                    "negative_marking": "N/A",
                    "platform": "In-person / MS Teams",
                    "focus": "Confidence, fundamentals of C/Java/Python, SQL queries"
                },
                {
                    "round_num": 4,
                    "name": "Managerial & HR Interview (MR & HR)",
                    "duration": "20 - 30 Minutes",
                    "questions": "Willingness to relocate, work shifts, strengths, situational questions",
                    "negative_marking": "N/A",
                    "platform": "In-person / MS Teams",
                    "focus": "Communication skills, cultural adaptability"
                }
            ]),
            json.dumps({
                "aptitude_weightage": "45%",
                "coding_weightage": "35%",
                "technical_cs_weightage": "20%",
                "key_syllabus_topics": [
                    "Quantitative: Numbers, P&C, Probability, Speed & Distance, Geometry",
                    "Reasoning: Seating Arrangement, Data Sufficiency, Blood Relations",
                    "Verbal: Sentence Completion, Error Identification, Reading Comprehension",
                    "Coding: String manipulation, Arrays, Matrix rotations, Dynamic Programming basics"
                ]
            }),
            json.dumps([
                "TCS NQT Foundation + Advanced Test",
                "Technical Interview (Project & CS Fundamentals)",
                "Managerial Round",
                "HR Round"
            ]),
            json.dumps(["Aptitude & Reasoning", "C/C++/Java/Python basics", "SQL Queries & Joins", "Final Year Project", "Data Structures Basics"]),
            json.dumps([
                "Write a program to find the non-repeating characters in a given string.",
                "Find the maximum subarray sum (Kadane's Algorithm).",
                "Explain the difference between Primary Key and Unique Key.",
                "What is a dangling pointer in C?",
                "Are you willing to relocate anywhere in India and work in rotational shifts?"
            ]),
            json.dumps([
                "Speed is crucial in NQT Part A. Practice shortcut formulas for Quants to finish within time.",
                "To qualify for Digital (₹7 LPA) or Prime (₹9-11 LPA), you MUST solve both coding questions in Part B with all hidden test cases passing.",
                "Know every single line of your resume and final year project inside out."
            ])
        ),
        (
            "Infosys",
            "infosys",
            "Mass IT / Service",
            "Next-generation digital services and consulting multinational.",
            "₹3.6 LPA (System Engineer), ₹6.25 LPA (DSE), ₹9.5 LPA (Specialist Programmer)",
            "Easy-Medium",
            json.dumps({
                "cgpa": "60% or 6.0 CGPA minimum in 10th, 12th, and Graduation",
                "backlogs": "Zero active backlogs allowed during final offer letter issuance",
                "branches": "BE/B.Tech/ME/M.Tech, MCA, M.Sc (CS/IT/Electronics)",
                "batches": "2025, 2026 Batch",
                "notes": "InfyTQ certification test and HackWithInfy provide direct routes to DSE (₹6.25 LPA) and Specialist Programmer (₹9.5 LPA)."
            }),
            json.dumps([
                {
                    "round_num": 1,
                    "name": "Infosys Online Qualifier Test",
                    "duration": "100 Minutes",
                    "questions": "Reasoning Ability (15 Q), Technical Ability / Math (10 Q), Verbal Ability (20 Q), Pseudo-code (5 Q), Numerical Puzzle (4 Q)",
                    "negative_marking": "No",
                    "platform": "Infosys Assessment Platform",
                    "focus": "High logical difficulty, cryptarithmetic, pseudo-code analysis"
                },
                {
                    "round_num": 2,
                    "name": "HackWithInfy / SP Coding Round (For High Packages)",
                    "duration": "180 Minutes",
                    "questions": "3 Complex Algorithmic Coding Problems",
                    "negative_marking": "No",
                    "platform": "HackerEarth",
                    "focus": "Dynamic Programming, Trees, Greedy, Graph Algorithms"
                },
                {
                    "round_num": 3,
                    "name": "Technical Interview",
                    "duration": "30 - 45 Minutes",
                    "questions": "Coding problems, OOP concepts, DBMS, Web technologies, Project deep dive",
                    "negative_marking": "N/A",
                    "platform": "Infosys Platform / Webex",
                    "focus": "Problem breakdown, explanation of written code"
                },
                {
                    "round_num": 4,
                    "name": "HR Interview",
                    "duration": "15 - 20 Minutes",
                    "questions": "Self-introduction, relocation, communication, cultural fit",
                    "negative_marking": "N/A",
                    "platform": "Infosys Platform",
                    "focus": "English fluency, confidence, willingness to learn"
                }
            ]),
            json.dumps({
                "logical_reasoning_weightage": "30%",
                "pseudocode_puzzle_weightage": "25%",
                "verbal_weightage": "20%",
                "coding_weightage": "25%",
                "key_syllabus_topics": [
                    "Mathematical Reasoning & Cryptarithmetic Puzzles",
                    "Data Interpretation and Logical Deductions",
                    "Pseudo-code tracing (Nested loops, recursion, bitwise operations)",
                    "Core Java / Python / C++ concepts",
                    "SQL commands, Joins, Normalization"
                ]
            }),
            json.dumps([
                "Infosys Qualifier Round (Puzzles + Pseudo-code)",
                "Technical Interview",
                "HR Round"
            ]),
            json.dumps(["Cryptarithmetic Puzzles", "Pseudo-code Execution", "OOP Principles", "DBMS & SQL", "Data Structures"]),
            json.dumps([
                "Solve cryptarithmetic addition puzzle: SEND + MORE = MONEY.",
                "Trace output of recursive Fibonacci function with memoization.",
                "Explain Polymorphism with a real-world software example.",
                "Write an SQL query to find the 2nd highest salary from an Employee table."
            ]),
            json.dumps([
                "The pseudo-code and puzzle sections have high cutoffs; practice tracing code manually.",
                "Participate seriously in HackWithInfy to bypass standard aptitude rounds and compete directly for ₹9.5 LPA Specialist Programmer role."
            ])
        ),
        (
            "Microsoft",
            "microsoft",
            "Big Tech / FAANG",
            "Empowering every person and organization on the planet to achieve more.",
            "₹24 - ₹48 LPA (SDE 1)",
            "Hard",
            json.dumps({
                "cgpa": "7.0+ CGPA preferred, 60% minimum throughout academics",
                "backlogs": "No active backlogs allowed",
                "branches": "CS, IT, ECE, EE, Math & Computing",
                "batches": "2025, 2026 Batch",
                "notes": "Heavy emphasis on clean code, memory safety, test cases, and collaborative problem-solving with the interviewer."
            }),
            json.dumps([
                {
                    "round_num": 1,
                    "name": "Online Assessment (OA)",
                    "duration": "90 Minutes",
                    "questions": "2-3 Algorithmic Coding Questions",
                    "negative_marking": "No",
                    "platform": "Codility",
                    "focus": "Arrays, Strings, Dynamic Programming, Greedy"
                },
                {
                    "round_num": 2,
                    "name": "Virtual Onsite Round 1 (Data Structures)",
                    "duration": "45 - 60 Minutes",
                    "questions": "Coding problem on Trees/Graphs/Linked Lists + System Concepts",
                    "negative_marking": "N/A",
                    "platform": "Microsoft Teams + Codility live editor",
                    "focus": "Edge cases, Big-O complexity, test-driven thinking"
                },
                {
                    "round_num": 3,
                    "name": "Virtual Onsite Round 2 (Algorithms & Design)",
                    "duration": "45 - 60 Minutes",
                    "questions": "Hard Algorithm / Low-Level Object Oriented Design",
                    "negative_marking": "N/A",
                    "platform": "Microsoft Teams",
                    "focus": "Design patterns, thread safety, clean architecture"
                },
                {
                    "round_num": 4,
                    "name": "AA Round (As Appropriate / Partner Director)",
                    "duration": "60 Minutes",
                    "questions": "Culture fit, architectural design, passion projects, growth mindset",
                    "negative_marking": "N/A",
                    "platform": "Microsoft Teams",
                    "focus": "Growth mindset, handling setbacks, curiosity"
                }
            ]),
            json.dumps({
                "dsa_weightage": "60%",
                "design_clean_code": "25%",
                "growth_mindset_culture": "15%",
                "key_syllabus_topics": [
                    "Binary Search & Two Pointers",
                    "Trees, BST, Tries (Lowest Common Ancestor, Inorder Successor)",
                    "Dynamic Programming & Memoization",
                    "Multithreading, Concurrency, and Synchronization primitives",
                    "Low Level Design (Elevator System, Chess, Rate Limiter)"
                ]
            }),
            json.dumps([
                "Online Assessment (Codility)",
                "Technical Interview 1 (Data Structures)",
                "Technical Interview 2 (Algorithms & Architecture)",
                "Partner Director / AA Interview (Growth Mindset)"
            ]),
            json.dumps(["Binary Trees & BST", "Dynamic Programming", "Low-Level Design", "Operating Systems & Concurrency", "Growth Mindset"]),
            json.dumps([
                "Reverse Nodes in k-Group in a Linked List.",
                "Serialize and Deserialize a Binary Search Tree.",
                "Design an in-memory Key-Value store with TTL (Time To Live).",
                "Tell me about a technical project where you failed and what you learned."
            ]),
            json.dumps([
                "Microsoft values 'Growth Mindset' above almost everything else: be open to feedback during the interview when the interviewer hints at an issue.",
                "Write clean, modular code with descriptive variable names and explicit unit test cases."
            ])
        ),
        (
            "Flipkart",
            "flipkart",
            "Top Product",
            "India's homegrown e-commerce pioneer, driving commerce through technology.",
            "₹22 - ₹32 LPA (SDE 1)",
            "Hard",
            json.dumps({
                "cgpa": "6.5+ CGPA or 65% in B.Tech/BE/MCA",
                "backlogs": "No active backlogs allowed",
                "branches": "CS, IT, Circuit branches",
                "batches": "2025, 2026 Batch",
                "notes": "Famous for its unique 'Machine Coding Round' where you must write fully working, modular object-oriented code in 90 minutes."
            }),
            json.dumps([
                {
                    "round_num": 1,
                    "name": "Flipkart GRiD / Online Assessment",
                    "duration": "90 Minutes",
                    "questions": "3 Coding Questions (Medium-Hard)",
                    "negative_marking": "No",
                    "platform": "HackerEarth / Mettl",
                    "focus": "Graphs, Dynamic Programming, Strings"
                },
                {
                    "round_num": 2,
                    "name": "Machine Coding Round (Signature Round)",
                    "duration": "90 Minutes coding + 30 Minutes defense",
                    "questions": "Build a working LLD application (e.g. In-memory Trello, Ride Sharing, Splitwise)",
                    "negative_marking": "N/A",
                    "platform": "Your own IDE (IntelliJ, VS Code)",
                    "focus": "Clean code, OOP principles, design patterns, separation of concerns, working driver code"
                },
                {
                    "round_num": 3,
                    "name": "Problem Solving & Data Structures (PS/DS)",
                    "duration": "60 Minutes",
                    "questions": "2 Algorithmic problems on Trees, Graphs, DP",
                    "negative_marking": "N/A",
                    "platform": "Google Meet",
                    "focus": "Optimality, time/space trade-offs"
                },
                {
                    "round_num": 4,
                    "name": "Hiring Manager Round",
                    "duration": "45 Minutes",
                    "questions": "System design concepts, past internships, behavioral scenarios, culture fit",
                    "negative_marking": "N/A",
                    "platform": "Google Meet",
                    "focus": "High energy, ownership, ability to work in fast-paced startup culture"
                }
            ]),
            json.dumps({
                "machine_coding_lld": "40%",
                "dsa_weightage": "40%",
                "culture_and_projects": "20%",
                "key_syllabus_topics": [
                    "Object-Oriented Design & Clean Code Practices",
                    "SOLID Principles, Strategy Pattern, Observer Pattern, Factory Pattern",
                    "Graphs (Bipartite, Dijkstra, Bridges)",
                    "Advanced Dynamic Programming",
                    "Concurrency and In-memory thread safety"
                ]
            }),
            json.dumps([
                "Online Coding Qualifier",
                "Machine Coding Round (Design + Working Code)",
                "Problem Solving & DSA Round",
                "Hiring Manager Round"
            ]),
            json.dumps(["Machine Coding", "Object-Oriented Design (LLD)", "Graphs", "Dynamic Programming", "Clean Architecture"]),
            json.dumps([
                "Machine Coding: Design a Ride Sharing application (Ride booking, matching drivers, billing).",
                "Machine Coding: Design a Splitwise expense sharing application with simplify debts.",
                "Find the median in a stream of running integers.",
                "Alien Dictionary (Topological Sort)."
            ]),
            json.dumps([
                "Practice completing full LLD problems within 90 minutes. Code MUST compile and run without runtime exceptions.",
                "Use clean package structures: models, services, repositories, and exception handlers."
            ])
        )
    ]

    for c in companies:
        cursor.execute("""
        INSERT INTO companies (name, slug, category, tagline, avg_salary, difficulty, eligibility, exam_pattern, syllabus, rounds_breakdown, frequently_asked_topics, sample_questions, tips)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, c)

    # -------------------------------------------------------------
    # Seeding Dedicated DSA Prep Sheet (Topic Wise Sheet)
    # -------------------------------------------------------------
    print("Seeding DSA Sheet Problems...")
    dsa_problems = [
        # Topic 1: Arrays & Hashing
        (
            "Arrays & Hashing",
            "Two Sum",
            "Easy",
            "https://leetcode.com/problems/two-sum/",
            "https://www.geeksforgeeks.org/check-if-pair-with-given-sum-exists-in-array/",
            "Given an array of integers nums and an integer target, return indices of the two numbers such that they add up to target. You may assume that each input would have exactly one solution, and you may not use the same element twice.",
            "Use a Hash Map to store previously seen numbers and their indices. For each number x, calculate complement = target - x. If complement exists in map, return current index and map[complement].",
            "O(N)",
            "O(N)",
            """def twoSum(nums: list[int], target: int) -> list[int]:
    seen = {}
    for i, num in enumerate(nums):
        complement = target - num
        if complement in seen:
            return [seen[complement], i]
        seen[num] = i
    return []""",
            """#include <vector>
#include <unordered_map>
using namespace std;

vector<int> twoSum(vector<int>& nums, int target) {
    unordered_map<int, int> seen;
    for (int i = 0; i < nums.size(); i++) {
        int complement = target - nums[i];
        if (seen.find(complement) != seen.end()) {
            return {seen[complement], i};
        }
        seen[nums[i]] = i;
    }
    return {};
}""",
            1
        ),
        (
            "Arrays & Hashing",
            "Best Time to Buy and Sell Stock",
            "Easy",
            "https://leetcode.com/problems/best-time-to-buy-and-sell-stock/",
            "https://www.geeksforgeeks.org/best-time-to-buy-and-sell-stock/",
            "You are given an array prices where prices[i] is the price of a given stock on the ith day. You want to maximize your profit by choosing a single day to buy one stock and choosing a different day in the future to sell that stock.",
            "Track the minimum price seen so far as you iterate through the list. At each day, calculate current profit = price - min_price and update max_profit.",
            "O(N)",
            "O(1)",
            """def maxProfit(prices: list[int]) -> int:
    min_price = float('inf')
    max_profit = 0
    for price in prices:
        if price < min_price:
            min_price = price
        elif price - min_price > max_profit:
            max_profit = price - min_price
    return max_profit""",
            """#include <vector>
#include <algorithm>
using namespace std;

int maxProfit(vector<int>& prices) {
    int minPrice = 1e9, maxProfit = 0;
    for (int price : prices) {
        minPrice = min(minPrice, price);
        maxProfit = max(maxProfit, price - minPrice);
    }
    return maxProfit;
}""",
            2
        ),
        (
            "Arrays & Hashing",
            "Maximum Subarray (Kadane's Algorithm)",
            "Medium",
            "https://leetcode.com/problems/maximum-subarray/",
            "https://www.geeksforgeeks.org/largest-sum-contiguous-subarray/",
            "Given an integer array nums, find the subarray with the largest sum, and return its sum.",
            "Kadane's Algorithm: Maintain current_sum and max_sum. For each element, either add it to the running subarray or start a new subarray at that element (current_sum = max(num, current_sum + num)).",
            "O(N)",
            "O(1)",
            """def maxSubArray(nums: list[int]) -> int:
    curr_sum = max_sum = nums[0]
    for num in nums[1:]:
        curr_sum = max(num, curr_sum + num)
        max_sum = max(max_sum, curr_sum)
    return max_sum""",
            """#include <vector>
#include <algorithm>
using namespace std;

int maxSubArray(vector<int>& nums) {
    int curr = nums[0], maxSub = nums[0];
    for (size_t i = 1; i < nums.size(); i++) {
        curr = max(nums[i], curr + nums[i]);
        maxSub = max(maxSub, curr);
    }
    return maxSub;
}""",
            3
        ),
        (
            "Arrays & Hashing",
            "Product of Array Except Self",
            "Medium",
            "https://leetcode.com/problems/product-of-array-except-self/",
            "https://www.geeksforgeeks.org/a-product-array-puzzle/",
            "Given an integer array nums, return an array answer such that answer[i] is equal to the product of all the elements of nums except nums[i], without using division and in O(N).",
            "Two-pass approach: Compute prefix products in the result array in the first pass from left to right. Then multiply with suffix products in a second pass from right to left using a single running integer.",
            "O(N)",
            "O(1) extra space",
            """def productExceptSelf(nums: list[int]) -> list[int]:
    n = len(nums)
    res = [1] * n
    # Prefix pass
    prefix = 1
    for i in range(n):
        res[i] = prefix
        prefix *= nums[i]
    # Suffix pass
    suffix = 1
    for i in range(n - 1, -1, -1):
        res[i] *= suffix
        suffix *= nums[i]
    return res""",
            """#include <vector>
using namespace std;

vector<int> productExceptSelf(vector<int>& nums) {
    int n = nums.size();
    vector<int> res(n, 1);
    int prefix = 1;
    for (int i = 0; i < n; i++) {
        res[i] = prefix;
        prefix *= nums[i];
    }
    int suffix = 1;
    for (int i = n - 1; i >= 0; i--) {
        res[i] *= suffix;
        suffix *= nums[i];
    }
    return res;
}""",
            4
        ),

        # Topic 2: Two Pointers & Sliding Window
        (
            "Two Pointers & Sliding Window",
            "3Sum",
            "Medium",
            "https://leetcode.com/problems/3sum/",
            "https://www.geeksforgeeks.org/find-triplets-array-whose-sum-equal-zero/",
            "Given an integer array nums, return all the triplets [nums[i], nums[j], nums[k]] such that i != j, i != k, and j != k, and nums[i] + nums[j] + nums[k] == 0 without duplicate triplets.",
            "Sort the array. Fix the first element nums[i]. Use two pointers (left and right) on the remaining suffix to find pairs that sum to -nums[i]. Skip duplicate elements at every pointer step to prevent duplicates.",
            "O(N^2)",
            "O(1) extra space",
            """def threeSum(nums: list[int]) -> list[list[int]]:
    nums.sort()
    res = []
    n = len(nums)
    for i in range(n - 2):
        if i > 0 and nums[i] == nums[i-1]:
            continue
        l, r = i + 1, n - 1
        while l < r:
            s = nums[i] + nums[l] + nums[r]
            if s == 0:
                res.append([nums[i], nums[l], nums[r]])
                l += 1
                r -= 1
                while l < r and nums[l] == nums[l-1]:
                    l += 1
                while l < r and nums[r] == nums[r+1]:
                    r -= 1
            elif s < 0:
                l += 1
            else:
                r -= 1
    return res""",
            """#include <vector>
#include <algorithm>
using namespace std;

vector<vector<int>> threeSum(vector<int>& nums) {
    sort(nums.begin(), nums.end());
    vector<vector<int>> res;
    int n = nums.size();
    for (int i = 0; i < n - 2; i++) {
        if (i > 0 && nums[i] == nums[i - 1]) continue;
        int l = i + 1, r = n - 1;
        while (l < r) {
            int sum = nums[i] + nums[l] + nums[r];
            if (sum == 0) {
                res.push_back({nums[i], nums[l], nums[r]});
                l++; r--;
                while (l < r && nums[l] == nums[l - 1]) l++;
                while (l < r && nums[r] == nums[r + 1]) r--;
            } else if (sum < 0) {
                l++;
            } else {
                r--;
            }
        }
    }
    return res;
}""",
            5
        ),
        (
            "Two Pointers & Sliding Window",
            "Trapping Rain Water",
            "Hard",
            "https://leetcode.com/problems/trapping-rain-water/",
            "https://www.geeksforgeeks.org/trapping-rain-water/",
            "Given n non-negative integers representing an elevation map where the width of each bar is 1, compute how much water it can trap after raining.",
            "Two-pointer optimal approach: Maintain left and right pointers, and track max_left and max_right heights. Move the pointer pointing to the smaller maximum inward, accumulating trapped water (max_side - height[ptr]).",
            "O(N)",
            "O(1)",
            """def trap(height: list[int]) -> int:
    if not height: return 0
    l, r = 0, len(height) - 1
    left_max, right_max = height[l], height[r]
    water = 0
    while l < r:
        if left_max < right_max:
            l += 1
            left_max = max(left_max, height[l])
            water += left_max - height[l]
        else:
            r -= 1
            right_max = max(right_max, height[r])
            water += right_max - height[r]
    return water""",
            """#include <vector>
#include <algorithm>
using namespace std;

int trap(vector<int>& height) {
    if (height.empty()) return 0;
    int l = 0, r = height.size() - 1;
    int leftMax = height[l], rightMax = height[r];
    int water = 0;
    while (l < r) {
        if (leftMax < rightMax) {
            l++;
            leftMax = max(leftMax, height[l]);
            water += leftMax - height[l];
        } else {
            r--;
            rightMax = max(rightMax, height[r]);
            water += rightMax - height[r];
        }
    }
    return water;
}""",
            6
        ),
        (
            "Two Pointers & Sliding Window",
            "Longest Substring Without Repeating Characters",
            "Medium",
            "https://leetcode.com/problems/longest-substring-without-repeating-characters/",
            "https://www.geeksforgeeks.org/length-of-the-longest-substring-without-repeating-characters/",
            "Given a string s, find the length of the longest substring without duplicate characters.",
            "Sliding Window with Hash Map: Expand window by incrementing right pointer. Store last seen index of each char. If char is already seen and its index >= left, shift left pointer to last_seen[char] + 1.",
            "O(N)",
            "O(min(N, Alphabet Size))",
            """def lengthOfLongestSubstring(s: str) -> int:
    char_map = {}
    left = max_len = 0
    for right, ch in enumerate(s):
        if ch in char_map and char_map[ch] >= left:
            left = char_map[ch] + 1
        char_map[ch] = right
        max_len = max(max_len, right - left + 1)
    return max_len""",
            """#include <string>
#include <unordered_map>
#include <algorithm>
using namespace std;

int lengthOfLongestSubstring(string s) {
    unordered_map<char, int> lastPos;
    int left = 0, maxLen = 0;
    for (int right = 0; right < s.length(); right++) {
        if (lastPos.count(s[right]) && lastPos[s[right]] >= left) {
            left = lastPos[s[right]] + 1;
        }
        lastPos[s[right]] = right;
        maxLen = max(maxLen, right - left + 1);
    }
    return maxLen;
}""",
            7
        ),

        # Topic 3: Binary Search
        (
            "Binary Search",
            "Search in Rotated Sorted Array",
            "Medium",
            "https://leetcode.com/problems/search-in-rotated-sorted-array/",
            "https://www.geeksforgeeks.org/search-an-element-in-a-sorted-and-pivoted-array/",
            "Given the array nums after the possible rotation and an integer target, return the index of target if it is in nums, or -1 if it is not in nums in O(log N) time.",
            "Modified Binary Search: Find mid. One half (either left to mid OR mid to right) is GUARANTEED to be normally sorted. Check if target falls in that sorted half's range. If so, discard other half; otherwise explore the other half.",
            "O(log N)",
            "O(1)",
            """def search(nums: list[int], target: int) -> int:
    l, r = 0, len(nums) - 1
    while l <= r:
        mid = (l + r) // 2
        if nums[mid] == target:
            return mid
        # Left half sorted
        if nums[l] <= nums[mid]:
            if nums[l] <= target < nums[mid]:
                r = mid - 1
            else:
                l = mid + 1
        # Right half sorted
        else:
            if nums[mid] < target <= nums[r]:
                l = mid + 1
            else:
                r = mid - 1
    return -1""",
            """#include <vector>
using namespace std;

int search(vector<int>& nums, int target) {
    int l = 0, r = nums.size() - 1;
    while (l <= r) {
        int mid = l + (r - l) / 2;
        if (nums[mid] == target) return mid;
        if (nums[l] <= nums[mid]) {
            if (nums[l] <= target && target < nums[mid]) r = mid - 1;
            else l = mid + 1;
        } else {
            if (nums[mid] < target && target <= nums[r]) l = mid + 1;
            else r = mid - 1;
        }
    }
    return -1;
}""",
            8
        ),

        # Topic 4: Linked List
        (
            "Linked List",
            "Reverse a Linked List",
            "Easy",
            "https://leetcode.com/problems/reverse-linked-list/",
            "https://www.geeksforgeeks.org/reverse-a-linked-list/",
            "Given the head of a singly linked list, reverse the list, and return the reversed list.",
            "Iterative 3-pointer method: Maintain prev = None, curr = head. Save curr.next, point curr.next = prev, advance prev = curr and curr = saved_next.",
            "O(N)",
            "O(1)",
            """class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def reverseList(head: ListNode) -> ListNode:
    prev = None
    curr = head
    while curr:
        nxt = curr.next
        curr.next = prev
        prev = curr
        curr = nxt
    return prev""",
            """struct ListNode {
    int val;
    ListNode *next;
    ListNode(int x) : val(x), next(nullptr) {}
};

ListNode* reverseList(ListNode* head) {
    ListNode *prev = nullptr, *curr = head;
    while (curr) {
        ListNode *nxt = curr->next;
        curr->next = prev;
        prev = curr;
        curr = nxt;
    }
    return prev;
}""",
            9
        ),
        (
            "Linked List",
            "LRU Cache",
            "Medium",
            "https://leetcode.com/problems/lru-cache/",
            "https://www.geeksforgeeks.org/lru-cache-implementation/",
            "Design a data structure that follows the constraints of a Least Recently Used (LRU) cache with O(1) time complexity for get and put operations.",
            "Combine a Hash Map (for O(1) key-to-node lookup) with a Doubly Linked List (for O(1) removal and insertion at head/tail). Use dummy head and tail nodes to simplify edge cases.",
            "O(1) for both operations",
            "O(Capacity)",
            """class Node:
    def __init__(self, key=0, val=0):
        self.key = key
        self.val = val
        self.prev = None
        self.next = None

class LRUCache:
    def __init__(self, capacity: int):
        self.cap = capacity
        self.cache = {}
        self.head, self.tail = Node(), Node()
        self.head.next = self.tail
        self.tail.prev = self.head

    def _remove(self, node):
        node.prev.next = node.next
        node.next.prev = node.prev

    def _add(self, node):
        node.next = self.head.next
        node.prev = self.head
        self.head.next.prev = node
        self.head.next = node

    def get(self, key: int) -> int:
        if key in self.cache:
            node = self.cache[key]
            self._remove(node)
            self._add(node)
            return node.val
        return -1

    def put(self, key: int, value: int) -> None:
        if key in self.cache:
            self._remove(self.cache[key])
        node = Node(key, value)
        self.cache[key] = node
        self._add(node)
        if len(self.cache) > self.cap:
            lru = self.tail.prev
            self._remove(lru)
            del self.cache[lru.key]""",
            """#include <unordered_map>
using namespace std;

struct Node {
    int key, val;
    Node *prev, *next;
    Node(int k=0, int v=0): key(k), val(v), prev(nullptr), next(nullptr) {}
};

class LRUCache {
    int cap;
    unordered_map<int, Node*> mp;
    Node *head, *tail;
    
    void removeNode(Node* node) {
        node->prev->next = node->next;
        node->next->prev = node->prev;
    }
    void addNode(Node* node) {
        node->next = head->next;
        node->prev = head;
        head->next->prev = node;
        head->next = node;
    }
public:
    LRUCache(int capacity) : cap(capacity) {
        head = new Node(); tail = new Node();
        head->next = tail; tail->prev = head;
    }
    int get(int key) {
        if (!mp.count(key)) return -1;
        Node* node = mp[key];
        removeNode(node); addNode(node);
        return node->val;
    }
    void put(int key, int value) {
        if (mp.count(key)) removeNode(mp[key]);
        Node* node = new Node(key, value);
        mp[key] = node;
        addNode(node);
        if (mp.size() > cap) {
            Node* lru = tail->prev;
            removeNode(lru);
            mp.erase(lru->key);
            delete lru;
        }
    }
};""",
            10
        ),

        # Topic 5: Trees & Graphs
        (
            "Trees & Graphs",
            "Lowest Common Ancestor of a Binary Tree",
            "Medium",
            "https://leetcode.com/problems/lowest-common-ancestor-of-a-binary-tree/",
            "https://www.geeksforgeeks.org/lowest-common-ancestor-binary-tree-set-1/",
            "Given a binary tree, find the lowest common ancestor (LCA) of two given nodes p and q.",
            "Recursive post-order traversal: If current node is None or matches p or q, return current node. Recursively search left and right subtrees. If both return non-null, current node is the LCA!",
            "O(N)",
            "O(Height of Tree)",
            """def lowestCommonAncestor(root, p, q):
    if not root or root == p or root == q:
        return root
    left = lowestCommonAncestor(root.left, p, q)
    right = lowestCommonAncestor(root.right, p, q)
    if left and right:
        return root
    return left or right""",
            """struct TreeNode {
    int val;
    TreeNode *left, *right;
    TreeNode(int x) : val(x), left(nullptr), right(nullptr) {}
};

TreeNode* lowestCommonAncestor(TreeNode* root, TreeNode* p, TreeNode* q) {
    if (!root || root == p || root == q) return root;
    TreeNode* left = lowestCommonAncestor(root->left, p, q);
    TreeNode* right = lowestCommonAncestor(root->right, p, q);
    if (left && right) return root;
    return left ? left : right;
}""",
            11
        ),
        (
            "Trees & Graphs",
            "Number of Islands",
            "Medium",
            "https://leetcode.com/problems/number-of-islands/",
            "https://www.geeksforgeeks.org/find-number-of-islands/",
            "Given an m x n 2D binary grid grid which represents a map of '1's (land) and '0's (water), return the number of islands.",
            "Iterate through all cells. When a '1' is encountered, increment island count and trigger a BFS or DFS to sink all connected land cells by marking them as '0'.",
            "O(M * N)",
            "O(M * N)",
            """def numIslands(grid: list[list[str]]) -> int:
    if not grid: return 0
    rows, cols = len(grid), len(grid[0])
    islands = 0

    def dfs(r, c):
        if r < 0 or c < 0 or r >= rows or c >= cols or grid[r][c] != '1':
            return
        grid[r][c] = '0'  # Mark visited
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            dfs(r + dr, c + dc)

    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == '1':
                islands += 1
                dfs(r, c)
    return islands""",
            """#include <vector>
using namespace std;

void dfs(vector<vector<char>>& grid, int r, int c) {
    int rows = grid.size(), cols = grid[0].size();
    if (r < 0 || c < 0 || r >= rows || c >= cols || grid[r][c] != '1') return;
    grid[r][c] = '0';
    dfs(grid, r + 1, c);
    dfs(grid, r - 1, c);
    dfs(grid, r, c + 1);
    dfs(grid, r, c - 1);
}

int numIslands(vector<vector<char>>& grid) {
    int count = 0;
    for (int r = 0; r < grid.size(); r++) {
        for (int c = 0; c < grid[0].size(); c++) {
            if (grid[r][c] == '1') {
                count++;
                dfs(grid, r, c);
            }
        }
    }
    return count;
}""",
            12
        ),

        # Topic 6: Dynamic Programming
        (
            "Dynamic Programming",
            "Coin Change",
            "Medium",
            "https://leetcode.com/problems/coin-change/",
            "https://www.geeksforgeeks.org/coin-change-dp-7/",
            "You are given an integer array coins representing coins of different denominations and an integer amount. Return the fewest number of coins that you need to make up that amount, or -1 if impossible.",
            "Bottom-Up DP: Let dp[i] be the minimum coins needed for amount i. Initialize dp[0] = 0 and all other dp[i] = infinity. For each amount from 1 to amount, and each coin: dp[i] = min(dp[i], 1 + dp[i - coin]).",
            "O(Amount * len(Coins))",
            "O(Amount)",
            """def coinChange(coins: list[int], amount: int) -> int:
    dp = [float('inf')] * (amount + 1)
    dp[0] = 0
    for i in range(1, amount + 1):
        for coin in coins:
            if i - coin >= 0:
                dp[i] = min(dp[i], 1 + dp[i - coin])
    return dp[amount] if dp[amount] != float('inf') else -1""",
            """#include <vector>
#include <algorithm>
using namespace std;

int coinChange(vector<int>& coins, int amount) {
    vector<int> dp(amount + 1, amount + 1);
    dp[0] = 0;
    for (int i = 1; i <= amount; i++) {
        for (int coin : coins) {
            if (i - coin >= 0) {
                dp[i] = min(dp[i], 1 + dp[i - coin]);
            }
        }
    }
    return dp[amount] > amount ? -1 : dp[amount];
}""",
            13
        ),
        (
            "Dynamic Programming",
            "Longest Increasing Subsequence (LIS)",
            "Medium",
            "https://leetcode.com/problems/longest-increasing-subsequence/",
            "https://www.geeksforgeeks.org/longest-increasing-subsequence-dp-3/",
            "Given an integer array nums, return the length of the longest strictly increasing subsequence in O(N log N) time.",
            "Patience Sorting with Binary Search: Maintain an array tails where tails[i] stores the smallest tail of all increasing subsequences of length i+1. For each number x, binary search its insertion position in tails.",
            "O(N log N)",
            "O(N)",
            """import bisect

def lengthOfLIS(nums: list[int]) -> int:
    tails = []
    for x in nums:
        idx = bisect.bisect_left(tails, x)
        if idx == len(tails):
            tails.append(x)
        else:
            tails[idx] = x
    return len(tails)""",
            """#include <vector>
#include <algorithm>
using namespace std;

int lengthOfLIS(vector<int>& nums) {
    vector<int> tails;
    for (int x : nums) {
        auto it = lower_bound(tails.begin(), tails.end(), x);
        if (it == tails.end()) {
            tails.push_back(x);
        } else {
            *it = x;
        }
    }
    return tails.size();
}""",
            14
        )
    ]

    for d in dsa_problems:
        cursor.execute("""
        INSERT INTO dsa_problems (topic, title, difficulty, leetcode_url, gfg_url, description, approach_notes, time_complexity, space_complexity, code_python, code_cpp, order_idx)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, d)

    conn.commit()
    conn.close()
    print("Database seeding completed successfully!")

if __name__ == "__main__":
    seed_database()
