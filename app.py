from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# Create a database or connect to it
def init_db():
    conn = sqlite3.connect('items.db')  # SQLite database file
    c = conn.cursor()
    c.execute('''
    CREATE TABLE IF NOT EXISTS items (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL
    )''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    conn = sqlite3.connect('items.db')
    c = conn.cursor()
    c.execute('SELECT * FROM items')
    items = c.fetchall()
    conn.close()
    return render_template('index.html', items=items)

@app.route('/add', methods=['POST'])
def add_item():
    item_name = request.form['item_name']
    if item_name:
        conn = sqlite3.connect('items.db')
        c = conn.cursor()
        c.execute('INSERT INTO items (name) VALUES (?)', (item_name,))
        conn.commit()
        conn.close()
    return redirect('/')

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
