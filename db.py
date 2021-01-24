import sqlite3
import pandas as pd
import os
os.chdir(r"C:\Users\Áron\Desktop\herd-immunity")

#creating database
conn = sqlite3.connect("covid.db")
c = conn.cursor()

#creating table
c.execute('CREATE TABLE IF NOT EXISTS ImmunityDate  (Country text, Days number)')
conn.commit()


#reading in df
df = pd.read_csv("days_left_df.csv")

#sending df to db
df.to_sql('ImmunityDate', conn, if_exists='replace', index = False)


#querying date
c.execute('''SELECT * FROM ImmunityDate''')

#printing stuff in db - if you're running this loop df_res will be empty,
#as the query "has been emptied by fetch" -that's why one uses spyder to be able to execute
#code partially
for row in c.fetchall():
    print (row)

#putting it into a db - just to check
df_res = pd.DataFrame(c.fetchall(), columns=['Country','Days'])
