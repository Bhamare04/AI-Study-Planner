from flask import Flask, render_template, request
import sqlite3

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

if __name__ == '__main__':
    app.run(debug=True)