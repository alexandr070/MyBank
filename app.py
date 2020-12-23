from flask import Flask, g, render_template, request, redirect
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


# noinspection PyUnusedLocal
@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'db'):
        g.db.close()


@app.route('/test')
def test():
    people = []
    q = request.args.get('q', default='', type=str)
    c = get_db().cursor()
    qs = '{}%'.format(q)
    for row in c.execute(
            '''SELECT *, first_name||' '||last_name AS full_name
            FROM test 
            WHERE (first_name LIKE ?) OR (last_name LIKE ?);''',
            (qs, qs)):
        people.append({
            'id': row[0],
            'first_name': row[1],
            'last_name': row[2],
            'full_name': row[3]
        })
    return render_template('test.html', people=people, q=q)


@app.route('/test/add', methods=['POST'])
def test_add():
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    c = get_db().cursor()
    c.execute('INSERT INTO test (first_name, last_name) VALUES (?,?)', (first_name, last_name))
    get_db().commit()
    return redirect('/test')
