from flask import Flask, request, url_for, flash, redirect
from flask.templating import render_template
import sqlite3
app = Flask(__name__)
app.config['SECRET_KEY'] = "Rosie is a pricess"

# retrieve data 
def get_db_connection():
    conn = sqlite3.connect('database.db')
    # 设置数据的解析方法，可以像字典一样访问每一列数据
    conn.row_factory = sqlite3.Row
    return conn

# retrieve specific post
def get_post(post_id):
    conn = get_db_connection()
    post = conn.execute('SELECT * FROM posts WHERE id = ?',
                        (post_id,)).fetchone()
    conn.close()
    return post

@app.route('/')
def index():
    # use previous function to retrieve link
    conn = get_db_connection()

    # search for all data, put them into posts
    posts = conn.execute('SELECT * FROM posts').fetchall()
    conn.close()

    # hand the retrieved posts to index.html
    return render_template('index.html', posts=posts)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/posts/<int:post_id>')
def post(post_id):
    post = get_post(post_id)
    return render_template('post.html', post=post)

@app.route('/posts/new', methods=('GET', 'POST'))
def new():
    # if method is get: go to new.html
    # if method is post: save to the database and go to index.html
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is empty!')
        elif not content:
            flash('Content is empty!')
        else:
            conn = get_db_connection()
            conn.execute('INSERT INTO posts (title, content) VALUES (?, ?)',
                        (title, content))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))
    return render_template('new.html') 

@app.route('/posts/<int:id>/edit', methods = ('GET', 'POST'))
def edit(id):
    post = get_post(id)

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is required!')
        else:
            conn = get_db_connection()
            conn.execute('UPDATE posts SET title = ?, content = ?'
                        ' WHERE id = ?',
                        (title, content, id))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))

    return render_template('edit.html', post=post)


@app.route('/posts/<int:id>/delete', methods=('POST',))
def delete(id):
    post = get_post(id)
    conn = get_db_connection()
    conn.execute('DELETE FROM posts WHERE id = ?', (id, ))
    conn.commit()
    conn.close()
    flash(' "{}" delete successfully!'.format(post['title']))
    return redirect(url_for('index'))
