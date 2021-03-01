from flask import Flask, g, render_template
import sqlite3
import os
from flask import request
os.chdir(r"C:\Users\Áron\Desktop\covid\herd-immunity")

#connecting to db
def connect_db():
    return sqlite3.connect('covid.db')


app = Flask(__name__)

phones = ["iphone", "android", "blackberry"]

#getting the data from the db
@app.route('/')
def get_data(name=None):
    
    #get user data
    agent = request.headers.get('User-Agent')
    
    g.db = connect_db()
    cur = g.db.execute('SELECT * FROM ImmunityDate WHERE FDDays < 5000 AND SDDays < 5000 AND FDDays < SDDays')
    data = []
    for row in cur.fetchall():  
        data.append(row)
    g.db.close()
    
    #send user to mobile site if on phone
    if any(phone in agent.lower() for phone in phones):
        return render_template("mobile-view.html", data = data)
    return render_template('index.html', data=data)

#running
def main():
    app.run(debug=False)

if __name__ == '__main__':
    main()