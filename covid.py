import pandas as pd
import sqlite3
import numpy as np
import os

os.chdir(r"C:\Users\Áron\Desktop\herd-immunity")

url="https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/vaccinations/vaccinations.csv"


#building list of countires who are vaccinating
def get_countries():
    df = pd.read_csv(url)
    countries = df[ df["total_vaccinations"] > 0]["location"].unique().tolist()
    return countries
    
#NEEDS TO BE OPTIMIZED
def get_days_left(country):
    #Getting the data - cleaning
#    country = "Hungary"
    df = pd.read_csv(url)
    
    df = df[df["location"] == country]._get_numeric_data()
    
    mask = np.all(np.isnan(df), axis=1) | np.all(df == 0, axis=1)
    df = df[~mask]
    
    #dealing with missing values
    df= df.fillna(method = "ffill")
    
    #Setting up values - getting population from vaccination / 100 and sum(vaccinated)
    try:
        population = df["total_vaccinations"].iloc[-1] / (df["total_vaccinations_per_hundred"].iloc[-1] / 100)
        
        not_vaccinated = population - df["people_vaccinated"].iloc[-1]
        seven_day_average = sum(df["daily_vaccinations"].iloc[-14:]) / 14
        
        days_left = (not_vaccinated *0.6) / seven_day_average
        
        #this return format allows to be inserted into a dataframe
        return {'Country': country,
                'Days': days_left}
    except:
        return 0



#generating dataframe to return - getting every countries' immunity date
def build_list():
    l = []    
    countries = get_countries()
    for country in countries:
        l.append(get_days_left(country))
    
    return l




#Database things
def insert_database(df):
    #creating database
    conn = sqlite3.connect("covid.db")
    c = conn.cursor()
    
    #creating table
    c.execute('CREATE TABLE IF NOT EXISTS ImmunityDate  (Country text, Days number)')
    conn.commit()
    
    #sending df to db
    df.to_sql('ImmunityDate', conn, if_exists='replace', index = False)



if __name__ == '__main__':
    #putting it into a df
    days_left_df = pd.DataFrame(build_list()).dropna()
    days_left_df["Days"] = days_left_df["Days"].astype(int)
    

#saving it into disk
#days_left_df.to_csv("days_left_df.csv",index = False) #index needs to be false(unnamed:0 issue)







