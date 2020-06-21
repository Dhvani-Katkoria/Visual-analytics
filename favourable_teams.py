import pandas as pd
import numpy as np
import plotly as py
import plotly.graph_objs as go
from collections import Counter

df= pd.read_csv('/Users/daggubatisirichandana/PycharmProjects/MLTechniques/Datavis/A4/competitions.csv')
# Get unique elements in multiple columns
Allteams = (df['team'].append(df['rival'])).unique()
print("Country Names:\n")
print(Allteams,"\n\n")
countryselected=input("Enter country name in captilized format : ")
t1=df[df.team == countryselected][['rival','metric','win','tie','loss']].rename(columns={'rival': 'country'})
t2=df[df.rival == countryselected][['team','metric','win','tie','loss']].rename(columns={'team': 'country'})
teams=pd.concat([t1,t2])
print(teams[teams.country == 'England'])
teams['text']= pd.Series(['']*teams.shape[0],index=teams.index.values).astype(str).str.cat(teams.win.astype(str), sep=' Win: ').str.cat(teams.tie.astype(str), sep=' Tie: ').str.cat(teams.loss.astype(str), sep=' Lose:')


data = dict (
    type = 'choropleth',
    locations = teams['country'],
    locationmode='country names',
    colorscale =  [[0, 'red'],[0.5, 'white'],[1, 'green']],
    colorbar_title = 'Favourability',
    colorbar_ticksuffix = '%',
    text = teams['text'],
    z= teams['metric'])

map = go.Figure(data=[data])
map.update_layout(
    title_text='Matches Favourability with '+countryselected,
    geo=dict(
        showframe=False,
        showcoastlines=False,
        showlakes=True,
        lakecolor='#69d4ff',
        showocean=True,
        landcolor='black',
        oceancolor='#69d4ff',
        projection_type='equirectangular'
    )
)
py.offline.plot(map)

