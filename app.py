from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# Create or connect to the database
def init_db():
    conn = sqlite3.connect('items.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL
        )''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            item_id INTEGER NOT NULL,
            content TEXT NOT NULL,
            FOREIGN KEY (item_id) REFERENCES items (id) ON DELETE CASCADE
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

@app.route('/item/<int:item_id>', methods=['GET', 'POST'])
def item_page(item_id):
    conn = sqlite3.connect('items.db')
    c = conn.cursor()

    # Fetch the item
    c.execute('SELECT * FROM items WHERE id = ?', (item_id,))
    item = c.fetchone()
    if not item:
        return "Item not found", 404

    # Fetch the posts for this item
    c.execute('SELECT * FROM posts WHERE item_id = ?', (item_id,))
    posts = c.fetchall()

    # Add a new post if POST request
    if request.method == 'POST':
        post_content = request.form['post_content']
        if post_content:
            c.execute('INSERT INTO posts (item_id, content) VALUES (?, ?)', (item_id, post_content))
            conn.commit()
            # Redirect back to the item page to show the new post
            return redirect(f'/item/{item_id}')

    conn.close()
    return render_template('item_page.html', item=item, posts=posts)

# Route to delete an item
@app.route('/item/<int:item_id>/delete', methods=['POST'])
def delete_item(item_id):
    conn = sqlite3.connect('items.db')
    c = conn.cursor()
    c.execute('DELETE FROM items WHERE id = ?', (item_id,))
    conn.commit()
    conn.close()
    return redirect('/')

# Route to delete a post
@app.route('/post/<int:post_id>/delete', methods=['POST'])
def delete_post(post_id):
    conn = sqlite3.connect('items.db')
    c = conn.cursor()
    c.execute('DELETE FROM posts WHERE id = ?', (post_id,))
    conn.commit()
    conn.close()
    # Redirect to the item's page after deleting the post
    return redirect(request.referrer)

# Route to add an item
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
    init_db()  # Initialize the database
    app.run(debug=True)
