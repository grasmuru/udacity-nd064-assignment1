import sqlite3
import logging
import logging.config
from flask import Flask, jsonify, json, render_template, request, url_for, redirect, flash
from werkzeug.exceptions import abort
from os import path

x = 0
# Function to get a database connection.
# This function connects to database with the name `database.db`
def get_db_connection():
    connection = sqlite3.connect('database.db')
    connection.row_factory = sqlite3.Row
    global x
    x=x+1
    return connection

# Function to get a post using its ID
def get_post(post_id):
    connection = get_db_connection()
    post = connection.execute('SELECT * FROM posts WHERE id = ?',
                        (post_id,)).fetchone()
    connection.close()
    global x
    x=x-1
    return post

# Define the Flask application
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your secret key'

# Define the main route of the web application 
@app.route('/')
def index():
    connection = get_db_connection()
    posts = connection.execute('SELECT * FROM posts').fetchall()
    connection.close()
    global x
    x=x-1
    return render_template('index.html', posts=posts)

# Define how each individual article is rendered 
# If the post ID is not found a 404 page is shown
@app.route('/<int:post_id>')
def post(post_id):
    post = get_post(post_id)
    if post is None:
      logger.debug('Non existant article returned')
      return render_template('404.html'), 404
    else:
      logger.debug('Article returned '+post['title'])
      return render_template('post.html', post=post)

# Define the About Us page
@app.route('/about')
def about():
    logger.debug('About us page retrieved')
    return render_template('about.html')

# Define the post creation functionality 
@app.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is required!')
        else:
            connection = get_db_connection()
            connection.execute('INSERT INTO posts (title, content) VALUES (?, ?)',
                         (title, content))
            connection.commit()
            connection.close()
            logger.debug('Created an article called '+title)
            global x
            x=x-1
            return redirect(url_for('index'))

    return render_template('create.html')

# Define the post creation functionality 	
@app.route('/healthz')
def healthz():
    return 'result: OK - healthy';

# Define the post creation functionality  {"db_connection_count": 1, "post_count": 7}
@app.route('/metrics')
def metrics():
    connection = get_db_connection()
    posts = len(connection.execute('SELECT * FROM posts').fetchall())
    connection.close()
    global x
    x=x-1
    data = {}
    data['post_count'] = posts
    data['db_connection_count'] = x
    return json.dumps(data)	
	
# start the application on port 3111
if __name__ == "__main__":
   log_file_path = path.join(path.dirname(path.abspath(__file__)), 'logging.conf')
   logging.config.fileConfig(log_file_path)
   logger = logging.getLogger()
   app.run(host='0.0.0.0', port='3111')
