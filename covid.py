import pandas as pd
import numpy as np

def get_days_left(country, population):
    #Getting the data - cleaning
    df = pd.read_csv("https://covid.ourworldindata.org/data/owid-covid-data.csv")
    
    vacc_col = [vac for vac in df.columns if "vaccin" in vac]
    df = df[df["location"]== country][vacc_col]
    
    mask = np.all(np.isnan(df), axis=1) | np.all(df == 0, axis=1)
    df = df[~mask]
    
    #dealing with missing values
    df["new_vaccinations"] = df["new_vaccinations"].fillna(method = "ffill")
    
    #Setting up values
    not_vaccinated = population - df["total_vaccinations"].iloc[-1]
    seven_day_average = sum(df["new_vaccinations"].iloc[-7:]) / 7
    
    days_left = int((not_vaccinated / 2) / seven_day_average)
    return days_left

print(str(get_days_left("Hungary", 9600000))+" days until herd immunity.")