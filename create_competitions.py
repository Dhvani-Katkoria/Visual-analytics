import pandas as pd
import numpy as np
import plotly as py
import plotly.graph_objs as go
from collections import Counter

df= pd.read_csv('/Users/daggubatisirichandana/PycharmProjects/MLTechniques/Datavis/A4/results.csv')

#put date in correct format and set it as the index
date= pd.to_datetime(df.date.values)
df['date']=date
df.set_index('date', inplace=True)

#get the column of results (wins, ties and losses)
win= np.where(df.home_score > df.away_score, 'win', None)
tie=np.where(df.home_score == df.away_score, 'tie', None)
loss= np.where(df.home_score < df.away_score, 'loss', None)
results=pd.DataFrame([win, tie, loss]).T    #transpose
df['result']= [value[value != None]  for value in results.values]
df['result']=np.squeeze(df.result.tolist())

#Get list of unique pairs
unique_team=df.groupby(['home_team','away_team']).count().index.values
temp = Counter(frozenset(ele) for ele in unique_team)
unique_team=[list(ele) for ele in list(temp)]
#Calculate values for the frequently playing teams
games = pd.DataFrame(columns =['team', 'rival', 'win', 'tie', 'loss', 'difference', 'total', 'metric'])
for i,j in unique_team:
    t1=df[df.home_team == i][df[df.home_team == i].away_team == j]
    t2=df[df.home_team == j][df[df.home_team == j].away_team == i]
    frame=pd.concat([t1,t2])
    print(frame)
    win=frame[frame.result == 'win'].shape[0]
    tie=frame[frame.result == 'tie'].shape[0]
    loss=frame[frame.result == 'loss'].shape[0]
    total=win+tie+loss
    diff=win-loss
    metric=diff/total
    # Append rows in Empty Dataframe by adding dictionaries
    games = games.append({'team':i, 'rival':j, 'win':win, 'tie':tie, 'loss':loss, 'difference':diff, 'total':total, 'metric':metric}, ignore_index=True)

games.to_csv('competitions.csv')

