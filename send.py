from flask import Flask, g, render_template
import sqlite3
import os
os.chdir(r"C:\Users\Áron\Desktop\covid\herd-immunity")

#connecting to db
def connect_db():
    return sqlite3.connect('covid.db')


app = Flask(__name__)

#getting the data from the db
@app.route('/')
def get_data(name=None):
    g.db = connect_db()
    cur = g.db.execute('SELECT * FROM ImmunityDate')
    data = []
    for row in cur.fetchall():  
        data.append(row)
    g.db.close()
    return render_template('index.html', data=data)

#running
def main():
    app.run(debug=False)

if __name__ == '__main__':
    main()