import pandas as pd
import sqlite3
import numpy as np
import os

os.chdir(r"C:\Users\Áron\Desktop\covid\herd-immunity")

url="https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/vaccinations/vaccinations.csv"


#building list of countires who are vaccinating
def get_countries():
    df = pd.read_csv(url)
    countries = df[ df["total_vaccinations"] > 0]["location"].unique().tolist()
    return countries
    
#NEEDS TO BE OPTIMIZED
def get_days_left(country):
    #Getting the data - cleaning
#    country = "United Kingdom"
    df = pd.read_csv(url)
    
    last_updated = df[df["location"] == country]["date"].iloc[-1]
    df = df[df["location"] == country]._get_numeric_data()
    
    mask = np.all(np.isnan(df), axis=1) | np.all(df == 0, axis=1)
    df = df[~mask]
    
    #dealing with missing values
    df= df.fillna(method = "ffill")
    
    #Setting up values - getting population from vaccination / 100 and sum(vaccinated)
    try:
        population = df["total_vaccinations"].iloc[-1] / (df["total_vaccinations_per_hundred"].iloc[-1] / 100)
        daily_average = sum(df["daily_vaccinations"].iloc[-14:]) / 14
        
        not_vaccinated_fd = population - df["people_vaccinated"].iloc[-1]
        not_vaccinated_sd = population - df["people_fully_vaccinated"].iloc[-1]
        
        base_day_fd = df["people_vaccinated"].iloc[-8]
        base_day_sd = df["people_fully_vaccinated"].iloc[-8]
        
        average_first_dose = (sum(df["people_vaccinated"].iloc[-7:] - base_day_fd) / 7)
        average_second_dose = (sum(df["people_fully_vaccinated"].iloc[-7:] - base_day_sd) / 7)

        days_left_first_dose = (not_vaccinated_fd *0.7) / average_first_dose
        days_left_second_dose = (not_vaccinated_sd *0.7) / average_second_dose
        
        
        
        
        
        #this return format allows to be inserted into a dataframe
        return {'Country': country,
                'FDDays' : days_left_first_dose,
                'SDDays' : days_left_second_dose,
                'DailyAvg': daily_average,
                'Updated' : last_updated}
    except:
        return 0



#generating dataframe to return - getting every countries' immunity date
def build_list():  
    l = []    
    countries = get_countries()
    for country in countries:
        l.append(get_days_left(country))
    
    return l
  

def build_df():
    res = build_list()
    days_left_df = pd.DataFrame()
    for row in res:
        if row != 0:
            days_left_df = days_left_df.append(row, ignore_index = True)
    return days_left_df


#Database things
def insert_database(df):
    #creating database
    conn = sqlite3.connect("covid.db")
    c = conn.cursor()
    
    #creating table
    c.execute('CREATE TABLE IF NOT EXISTS ImmunityDate  (Country text,FDDays number, SDDays number, DailyAvg number, Updated text)')
    conn.commit()
    
    #sending df to db
    df.to_sql('ImmunityDate', conn, if_exists='replace', index = False)



a = pd.DataFrame(build_list())

if __name__ == '__main__':
    #putting it into a df
    days_left_df = build_df().dropna().reset_index(drop=True)
    
    #filtering infinte values
    df_filter = days_left_df.isin([np.nan, np.inf, -np.inf]) 
    days_left_df = days_left_df[~df_filter].dropna()
    
    
    days_left_df["FDDays"] = days_left_df["FDDays"].astype(int)
    days_left_df["SDDays"] = days_left_df["SDDays"].astype(int)
    days_left_df["DailyAvg"] = days_left_df["DailyAvg"].astype(int)
    insert_database(days_left_df)
    





