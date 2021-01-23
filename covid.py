import pandas as pd
import numpy as np


def get_days_left(country):
    #Getting the data - cleaning
    #country = "Malta"
    
    df = pd.read_csv("https://covid.ourworldindata.org/data/owid-covid-data.csv")
    
    vacc_col = [vac for vac in df.columns if "vaccin" in vac]
    df = df[df["location"]== country][vacc_col]
    
    mask = np.all(np.isnan(df), axis=1) | np.all(df == 0, axis=1)
    df = df[~mask]
    
    #dealing with missing values
    df= df.fillna(method = "ffill")
    df= df.fillna(method = "bfill")
    
    #Setting up values - getting population from vaccination / 100 and sum(vaccinated)
    try:
        population = df["total_vaccinations"].iloc[-1] / (df["total_vaccinations_per_hundred"].iloc[-1] / 100)
        
        not_vaccinated = population - df["total_vaccinations"].iloc[-1]
        seven_day_average = sum(df["new_vaccinations"].iloc[-14:]) / 14
        
        days_left = (not_vaccinated / 2) / seven_day_average
        return days_left
    
    except:
        print("Country does not provide enough data.")
        
#get_days_left("Malta")


#returning dataframe -saving it into csv file
data = {'Country': ['Hungary','Austria'],
        'Days': [get_days_left("Hungary"), get_days_left("Austria")]
    }
days_left_df = pd.DataFrame(data, columns= ['Country', 'Days'])
days_left_df.to_csv("days_left_df.csv",index = False) #index needs to be false(unnamed:0 issue)


