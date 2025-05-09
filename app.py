from flask import Flask, render_template, request, redirect
import psycopg2
import os

app = Flask(__name__)

# Параметри для підключення до Render PostgreSQL (через змінні середовища)
conn = psycopg2.connect(
    host=os.getenv("DB_HOST"),
    port=os.getenv("DB_PORT"),
    dbname=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD")
)

@app.route('/')
def index():
    cur = conn.cursor()
    cur.execute("SELECT * FROM notes ORDER BY created_at DESC")
    notes = cur.fetchall()
    return render_template("index.html", notes=notes)

@app.route('/add', methods=['POST'])
def add_note():
    title = request.form['title']
    content = request.form['content']
    cur = conn.cursor()
    cur.execute("INSERT INTO notes (title, content) VALUES (%s, %s)", (title, content))
    conn.commit()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')
