from flask import Flask, render_template
import pandas as pd
from pandas import DataFrame
import os
import pangviz
app = Flask(__name__)

@app.route('/')
def hello_world():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    attacks = pd.read_csv(dir_path+'\\attacks.csv')
    countries = attacks.loc[:, ['Country']]
    keys = countries['Country'].str.strip()
    df = DataFrame(keys) #convert series to dataframe
    grouped = df.groupby('Country').size() #get count per country

    # convert groupby object back to a dataframe by creating 2 series and joining them:
    s1 = pd.Series(grouped.index.values)
    s2 = pd.Series(grouped.values)
    df2 = pd.DataFrame({'Country': s1, 'Incidents': s2})

    df2 = df2[df2['Incidents']>=5]
    dt = pangviz.ToGvizDataTable(df2)
    return render_template('index.html',mapdata=dt.encode()) #Pass geo data as a json string

if __name__ == '__main__':
    app.run()
