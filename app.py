from flask import Flask, g, render_template
import sqlite3

app = Flask(__name__)

conn = sqlite3.connect('bank.db')
cur = conn.cursor()

cur.execute('''CREATE TABLE IF NOT EXISTS test (
id INTEGER PRIMARY KEY AUTOINCREMENT,
first_name TEXT,
last_name TEXT
);''')
conn.close()


def get_db():
    if not hasattr(g, 'db'):
        g.db = sqlite3.connect('bank.db')
    return g.db


@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'db'):
        g.db.close()


@app.route('/test')
def test():
    people = []
    c = get_db().cursor()
    for row in c.execute('SELECT * FROM test;'):
        people.append({
            'id': row[0],
            'first_name': row[1],
            'last_name': row[2]

        })
    return render_template('test.html', people=people)
