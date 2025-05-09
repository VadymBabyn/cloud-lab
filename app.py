from flask import Flask, render_template, request, redirect
import psycopg2
import os

app = Flask(__name__)

# Параметри для підключення до Render PostgreSQL
conn = psycopg2.connect(
    host=os.getenv("DB_HOST"),
    port=os.getenv("DB_PORT"),
    dbname=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD")
)

# Створення таблиці, якщо не існує
def create_table_if_not_exists():
    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS notes (
                id SERIAL PRIMARY KEY,
                title TEXT NOT NULL,
                content TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        conn.commit()

create_table_if_not_exists()

@app.route('/')
def index():
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM notes ORDER BY created_at DESC")
        notes = cur.fetchall()
    return render_template("index.html", notes=notes)

@app.route('/add', methods=['POST'])
def add_note():
    title = request.form['title']
    content = request.form['content']
    with conn.cursor() as cur:
        cur.execute("INSERT INTO notes (title, content) VALUES (%s, %s)", (title, content))
        conn.commit()
    return redirect('/')

@app.route('/delete/<int:note_id>')
def delete_note(note_id):
    with conn.cursor() as cur:
        cur.execute("DELETE FROM notes WHERE id = %s", (note_id,))
        conn.commit()
    return redirect('/')

@app.route('/edit/<int:note_id>', methods=['GET', 'POST'])
def edit_note(note_id):
    if request.method == 'POST':
        new_title = request.form['title']
        new_content = request.form['content']
        with conn.cursor() as cur:
            cur.execute("UPDATE notes SET title = %s, content = %s WHERE id = %s", (new_title, new_content, note_id))
            conn.commit()
        return redirect('/')
    else:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM notes WHERE id = %s", (note_id,))
            note = cur.fetchone()
        return render_template('edit.html', note=note)

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')
