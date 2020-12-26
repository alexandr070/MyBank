from flask import Flask, g, render_template, request, redirect, flash
import sqlite3
from country_list import countries_for_language

app = Flask(__name__)
app.secret_key = '2003'

conn = sqlite3.connect('bank.db')
cur = conn.cursor()

cur.execute('''CREATE TABLE IF NOT EXISTS test (
id INTEGER PRIMARY KEY AUTOINCREMENT,
first_name TEXT,
last_name TEXT,
country TEXT
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


def get_countries():
    c = countries_for_language('ru')
    return [country[1] for country in c]


@app.route('/test')
def test():
    people = []
    q = request.args.get('q', default='', type=str)
    c = get_db().cursor()
    qs = '{}%'.format(q)
    for row in c.execute(
            '''SELECT id,first_name,last_name, first_name||' '||last_name AS full_name,country
            FROM test 
            WHERE (first_name LIKE ?) OR (last_name LIKE ?);''',
            (qs, qs)):
        people.append({
            'id': row[0],
            'first_name': row[1],
            'last_name': row[2],
            'full_name': row[3],
            'country': row[4]
        })
    return render_template('test.html', people=people, q=q, countries=get_countries())


@app.route('/test/add', methods=['POST'])
def test_add():
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    country = request.form['country']
    valid = True
    if len(first_name.strip()) == 0:
        flash('Имя не может быть пустым')
        valid = False

    if len(last_name.strip()) == 0:
        flash('Фамилия не может быть пустой')
        valid = False

    if country not in get_countries():
        flash('Неверная страна')
        valid = False

    if valid:
        c = get_db().cursor()
        c.execute('INSERT INTO test (first_name, last_name,country) VALUES (?,?,?)', (first_name, last_name, country))
        get_db().commit()
    return redirect('/test')


@app.route('/test/delete/<int:user_id>', methods=['POST'])
def test_delete(user_id):
    c = get_db().cursor()
    c.execute('DELETE FROM test WHERE id=?;', (user_id,))
    get_db().commit()
    return redirect('/test')
