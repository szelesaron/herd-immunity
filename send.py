from flask import Flask, render_template
import sqlite3
import os
import pandas as pd
os.chdir(r"C:\Users\Áron\Desktop\herd-immunity")

#this can be used to check the content of the database
def import_database():
    conn = sqlite3.connect("covid.db")
    c = conn.cursor()
    c.execute('''SELECT * FROM ImmunityDate''')
    
    #putting it into a df - just to check
    df_res = pd.DataFrame(c.fetchall(), columns=['Country','Days'])
    return df_res


data = import_database()

app = Flask(__name__)
@app.route('/')


def index():
    return render_template('index.html', data=data)


if __name__ == '__main__':
    app.run()