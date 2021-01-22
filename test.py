from flask import Flask, render_template
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
        
        days_left = int((not_vaccinated / 2) / seven_day_average)
        return str(days_left) + " days until herd immunity."
    
    except:
        print("Country does not provide enough data.")
        



data=[
    {
        'country':'Hungary',
        'days': get_days_left("Hungary"),

    }]

app = Flask(__name__)
@app.route('/')


def index():
    return render_template('index.html', data=data)


if __name__ == '__main__':
    app.run()