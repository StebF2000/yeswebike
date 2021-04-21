from flask import Flask,render_template
import sqlite3
app = Flask(__name__)
import os
import sys
'''connection = sqlite3.connect('database.db')


with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

cur.execute("INSERT INTO posts (title, content) VALUES (?, ?)",
            ('First Post', 'Content for the first post')
            )

cur.execute("INSERT INTO posts (title, content) VALUES (?, ?)",
            ('Second Post', 'Content for the second post')
            )

connection.commit()
connection.close()'''

@app.route('/')
def dashboard():
    #print(os.listdir('dashboard/pages'),file=sys.stderr)
    return render_template('pages/dashboard.html')

@app.route('/docs')
def docs():
    #print(os.listdir('dashboard/pages'),file=sys.stderr)
    return render_template('docs/documentation.html')