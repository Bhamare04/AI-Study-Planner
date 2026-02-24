from flask import Flask, render_template, request
import sqlite3
from datetime import datetime

app = Flask(__name__)

# DATABASE INIT
def init_db():
    conn = sqlite3.connect('planner.db')
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS subjects (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        difficulty TEXT,
        exam_date TEXT,
        study_hours INTEGER
    )
    ''')

    conn.commit()
    conn.close()

init_db()

@app.route('/', methods=['GET', 'POST'])
def home():

    if request.method == 'POST':
        name = request.form['name']
        difficulty = request.form['difficulty']
        exam_date = request.form['exam_date']
        study_hours = request.form['study_hours']

        conn = sqlite3.connect('planner.db')
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO subjects (name, difficulty, exam_date, study_hours) VALUES (?, ?, ?, ?)",
            (name, difficulty, exam_date, study_hours)
        )

        conn.commit()
        conn.close()

    # Fetch all subjects
    conn = sqlite3.connect('planner.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM subjects")
    subjects = cursor.fetchall()
    conn.close()

    return render_template('index.html', subjects=subjects)

@app.route('/plan')
@app.route('/plan')
def plan():

    conn = sqlite3.connect('planner.db')
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM subjects")
    subjects = cursor.fetchall()

    for r in subjects:
        print(r)
        
    conn.close()

    from datetime import datetime

    # ---- Difficulty Score ----
    def difficulty_score(diff):
        if diff == "Hard":
            return 3
        elif diff == "Medium":
            return 2
        else:
            return 1

    # ---- Exam Urgency Score ----
    def urgency_score(date_str):
        exam_date = datetime.strptime(date_str, "%Y-%m-%d")
        days_left = (exam_date - datetime.now()).days

        if days_left <= 3:
            return 3
        elif days_left <= 7:
            return 2
        else:
            return 1

    # ---- FINAL PRIORITY SORT ----
    subjects_sorted = sorted(
        subjects,
        key=lambda s: difficulty_score(s[2]) + urgency_score(s[3]),
        reverse=True
    )

    # 🔥 TODAY'S PLAN (Top 3 Subjects)
    today_plan = subjects_sorted[:3]

    return render_template(
        'plan.html',
        subjects=subjects_sorted,
        today_plan=today_plan
    )
if __name__ == '__main__':
    app.run(debug=True)