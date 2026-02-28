"""
SmartStudent AI – RAG Knowledge Base
Static curated documents about student life, study strategies, and budgeting.
These documents are embedded at startup and used to ground LLM answers.
"""

DOCUMENTS = [
    # ─── Study Strategies ───────────────────────────────────────────────────
    {
        "id": "study_001",
        "topic": "study",
        "title": "Pomodoro Technique",
        "content": (
            "The Pomodoro Technique is a time management method that breaks work into 25-minute "
            "focused sessions called 'pomodoros', followed by a 5-minute break. After 4 pomodoros, "
            "take a longer 15-30 minute break. This technique reduces mental fatigue, improves focus, "
            "and prevents burnout. Ideal for students with multiple subjects to study."
        ),
    },
    {
        "id": "study_002",
        "topic": "study",
        "title": "Spaced Repetition",
        "content": (
            "Spaced repetition is a learning technique where you review material at increasing "
            "intervals over time. Instead of cramming the night before, review notes after 1 day, "
            "then 3 days, then 1 week, then 2 weeks. Apps like Anki implement this automatically. "
            "Scientifically proven to increase long-term retention by up to 200%."
        ),
    },
    {
        "id": "study_003",
        "topic": "study",
        "title": "Active Recall",
        "content": (
            "Active recall is the practice of actively retrieving information from memory instead of "
            "passively re-reading notes. Close your textbook and try to write down everything you "
            "remember. Use flashcards, practice tests, and self-quizzing. Studies show active recall "
            "is 50-70% more effective than passive review for exam preparation."
        ),
    },
    {
        "id": "study_004",
        "topic": "study",
        "title": "The Feynman Technique",
        "content": (
            "The Feynman Technique: 1) Choose a concept to study. 2) Explain it in simple terms as "
            "if teaching a 12-year-old. 3) Identify gaps in your explanation and go back to the "
            "source material. 4) Simplify further and use analogies. This forces deep understanding "
            "rather than surface memorisation. Great for complex subjects like mathematics and physics."
        ),
    },
    {
        "id": "study_005",
        "topic": "study",
        "title": "Exam Preparation Timeline",
        "content": (
            "Optimal exam preparation: Start 3-4 weeks before the exam. Week 1: Review all material "
            "and create summary notes. Week 2: Practice problems and past papers. Week 3: Focus on "
            "weak areas identified from practice. Week 4 (last week): Light review and rest. "
            "Never sacrifice sleep before an exam — sleep consolidates memory. Aim for 7-8 hours."
        ),
    },
    {
        "id": "study_006",
        "topic": "study",
        "title": "Study Environment Optimisation",
        "content": (
            "An optimal study environment: Use a dedicated study space separate from leisure areas. "
            "Keep your phone in another room or use apps like Forest to block distractions. "
            "Maintain room temperature between 20-22°C. Use ambient noise or lo-fi music if silence "
            "is distracting. Good lighting reduces eye strain. Keep water nearby — dehydration "
            "reduces cognitive performance by 10-15%."
        ),
    },
    {
        "id": "study_007",
        "topic": "study",
        "title": "Mind Mapping for Complex Subjects",
        "content": (
            "Mind maps are visual diagrams that connect ideas around a central concept. "
            "Start with the main topic in the centre, then branch out to subtopics. "
            "Use colours and images to enhance memory. Mind maps are especially useful for "
            "essay-based subjects, connecting disparate concepts, and getting an overview before "
            "deep-diving into a topic. Tools: XMind, MindMeister, or just pen and paper."
        ),
    },
    {
        "id": "study_008",
        "topic": "study",
        "title": "Group Study Strategies",
        "content": (
            "Effective group study: Limit group size to 3-5 students. Assign roles — one person "
            "explains, others question. Use the 'teaching' method: each member teaches one topic "
            "to the rest. Schedule group sessions after individual study so you first form your "
            "own understanding. Avoid purely social sessions disguised as study. Set a clear agenda "
            "and time limit for each session."
        ),
    },
    # ─── Budget & Finance ────────────────────────────────────────────────────
    {
        "id": "budget_001",
        "topic": "budget",
        "title": "50/30/20 Budget Rule for Students",
        "content": (
            "The 50/30/20 rule adapted for students: 50% of income on needs (rent, food, transport, "
            "tuition), 30% on wants (entertainment, dining out, clothing), 20% on savings and debt "
            "repayment. As a student with limited income, aim for 60/20/20 — keeping needs at 60% "
            "and reducing wants to 20%. Even saving 10% per month builds financial resilience."
        ),
    },
    {
        "id": "budget_002",
        "topic": "budget",
        "title": "Reducing Food Costs",
        "content": (
            "Students spend 20-30% of their budget on food. Meal prepping on Sundays can cut food "
            "costs by 40%. Cook in bulk — rice, pasta, lentils, eggs are cheap and nutritious. "
            "Use student discounts at supermarkets. Apps like Too Good To Go offer restaurant meals "
            "at 70% discount. Bring lunch to campus instead of buying. Limit coffee shop visits — "
            "a daily $5 coffee costs $1,825 per year."
        ),
    },
    {
        "id": "budget_003",
        "topic": "budget",
        "title": "Subscription Audit",
        "content": (
            "The average person unknowingly pays for 3-5 unused subscriptions. Audit your subscriptions "
            "monthly. Check bank statements for recurring charges. Cancel anything unused for 30+ days. "
            "Share plans where allowed — Netflix, Spotify family plans split across 4-6 people cost "
            "under $3/month each. Use student discounts: Spotify, Apple Music, Adobe, and many SaaS "
            "tools offer 40-60% student discounts with a university email."
        ),
    },
    {
        "id": "budget_004",
        "topic": "budget",
        "title": "Emergency Fund for Students",
        "content": (
            "Even students need an emergency fund of $500-$1,000. This covers unexpected expenses like "
            "laptop repairs, medical bills, or travel emergencies without going into debt. Build it "
            "gradually — save $25-$50 per month. Keep it in a separate high-yield savings account "
            "to avoid spending temptation. An emergency fund eliminates the need for high-interest "
            "credit card debt in a crisis."
        ),
    },
    {
        "id": "budget_005",
        "topic": "budget",
        "title": "Student Discount Resources",
        "content": (
            "Maximise student discounts: UNiDAYS and Student Beans offer hundreds of verified student "
            "discounts. Amazon Prime Student is 50% cheaper. Microsoft 365 and Adobe Creative Cloud "
            "offer 60% discounts. Cinemas, museums, and public transport typically offer 20-50% off "
            "with a valid student ID. Always ask before paying — many businesses offer unlisted "
            "student discounts. International Student Identity Card (ISIC) unlocks 42,000+ discounts globally."
        ),
    },
    {
        "id": "budget_006",
        "topic": "budget",
        "title": "Side Income for Students",
        "content": (
            "Students can earn extra income without sacrificing grades: Tutoring peers or school "
            "students ($15-$50/hour). Freelancing on Fiverr or Upwork (design, writing, coding). "
            "Campus jobs (library, cafeteria) often have flexible hours aligned with study schedules. "
            "Selling notes on Stuvia or Nexus. Participating in paid research studies at your university. "
            "Limit work to 15-20 hours/week to avoid academic impact."
        ),
    },
    {
        "id": "budget_007",
        "topic": "budget",
        "title": "Avoiding Lifestyle Inflation",
        "content": (
            "Lifestyle inflation occurs when spending increases as income increases. As a student "
            "who gets a part-time job, resist upgrading your lifestyle immediately. Maintain the "
            "same spending habits and save or invest the extra income. The habits you build as a "
            "student — cooking at home, using public transport, avoiding impulse purchases — "
            "form the financial foundation for your entire adult life."
        ),
    },
    # ─── Mental Health & Wellbeing ───────────────────────────────────────────
    {
        "id": "wellbeing_001",
        "topic": "wellbeing",
        "title": "Managing Academic Stress",
        "content": (
            "Academic stress affects 70%+ of university students. Management strategies: "
            "Break large tasks into small, achievable steps. Use a physical planner to externalise "
            "worries from your mind. Exercise for 30 minutes at least 3 times per week — proven to "
            "reduce cortisol by 26%. Practice box breathing (4 seconds in, 4 hold, 4 out, 4 hold) "
            "for immediate anxiety relief. Talk to a counsellor — most universities offer free services."
        ),
    },
    {
        "id": "wellbeing_002",
        "topic": "wellbeing",
        "title": "Sleep and Academic Performance",
        "content": (
            "Sleep is the most under-rated study tool. During sleep, the brain consolidates memories "
            "and clears metabolic waste. Students who sleep 7-9 hours perform 20-30% better on exams "
            "than those who sleep less. Tips: Maintain a consistent sleep schedule (±30 min). "
            "Avoid screens 1 hour before bed. Keep your room dark and cool. "
            "A 20-minute nap between 1-3pm can restore alertness without disrupting night sleep."
        ),
    },
    {
        "id": "wellbeing_003",
        "topic": "wellbeing",
        "title": "Avoiding Procrastination",
        "content": (
            "Procrastination is driven by emotional avoidance, not laziness. Techniques to overcome it: "
            "The 2-minute rule — if a task takes under 2 minutes, do it now. "
            "Implementation intentions — 'I will study at 6pm in the library on Monday'. "
            "Reduce decision friction — lay out your study materials the night before. "
            "The 'just start' method — commit only to working for 5 minutes. Often, starting is the hardest part. "
            "Identify your peak energy hours and schedule deep work then."
        ),
    },
    # ─── Time Management ─────────────────────────────────────────────────────
    {
        "id": "time_001",
        "topic": "time_management",
        "title": "Time Blocking Method",
        "content": (
            "Time blocking involves scheduling specific tasks into specific time slots in your calendar. "
            "Unlike a to-do list, time blocking forces you to decide WHEN you will do each task. "
            "Block time for: deep work (exams, essays), shallow work (emails, admin), personal tasks, "
            "and recovery. Leave 20% of each day as buffer for the unexpected. "
            "Review and adjust your time blocks every Sunday for the coming week."
        ),
    },
    {
        "id": "time_002",
        "topic": "time_management",
        "title": "Eisenhower Matrix for Prioritisation",
        "content": (
            "The Eisenhower Matrix categorises tasks by urgency and importance: "
            "Q1 Urgent + Important (exams tomorrow, crises) — Do immediately. "
            "Q2 Not Urgent + Important (long-term study, health, projects) — Schedule. "
            "Q3 Urgent + Not Important (some meetings, others' requests) — Delegate or minimise. "
            "Q4 Not Urgent + Not Important (social media, TV) — Eliminate. "
            "Students should spend most time in Q2 to prevent Q1 crises."
        ),
    },
]


def get_all_documents() -> list:
    """Return all knowledge base documents."""
    return DOCUMENTS


def get_documents_by_topic(topic: str) -> list:
    """Return documents filtered by topic."""
    return [d for d in DOCUMENTS if d["topic"] == topic]
