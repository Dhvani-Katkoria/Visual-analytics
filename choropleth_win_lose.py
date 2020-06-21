import pandas as pd
import numpy as np
import plotly as py
import plotly.graph_objs as go

df= pd.read_csv('results.csv')

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

#get the column of total number of goals
df['goals']= df.home_score + df.away_score

#home
home_teams=df.groupby(['home_team','result']).count()['city'].sort_values(ascending=False).reset_index().rename(columns={'city': 'count'})
home_matches=[]
print(home_teams)
for team in home_teams.home_team:
    tot_matches= home_teams[home_teams.home_team== team]['count'].sum()
    home_matches.append(tot_matches)
home_teams['home_matches']=home_matches
home_teams['pct_home_victory']= home_teams['count']/ home_teams['home_matches']

print(home_teams)

#away
away_teams=df.groupby(['away_team','result']).count()['city'].sort_values(ascending=False).reset_index().rename(columns={'city': 'count'})
away_teams.replace({'loss': 'win', 'win':'loss'}, inplace=True) #loss means victory for the away team
away_tot_matches=[]
for team in away_teams.away_team:
    tot_matches= away_teams[away_teams.away_team == team]['count'].sum()
    away_tot_matches.append(tot_matches)
away_teams['away_matches']= away_tot_matches
away_teams['pct_victory_away'] = away_teams['count']/away_teams['away_matches']


#adjusting terminology and index
home_teams.rename(columns={'result': 'home_results', 'count': 'home_count'}, inplace=True)
home_teams.set_index('home_team', inplace=True)
away_teams.rename(columns={'result': 'away_results', 'count': 'away_count'}, inplace=True)
away_teams.set_index('away_team', inplace=True)

#defining winners and loosers
home_winners= home_teams[home_teams.home_results=='win']
away_winners= away_teams[away_teams.away_results=='win']
home_losers= home_teams[home_teams.home_results=='loss']
away_losers= away_teams[away_teams.away_results=='loss']

#merging datasets
winners=pd.merge(home_winners, away_winners, left_index=True, right_index=True, how='inner')
losers=pd.merge(home_losers, away_losers, left_index=True, right_index=True, how='inner')
losers.rename(columns={'pct_home_victory': 'pct_home_defeats', 'pct_victory_away': 'pct_away_defeats'}, inplace=True)
winners['tot_count']= winners.home_count + winners.away_count
winners['tot_matches']= winners.home_matches + winners.away_matches
winners['tot_pct_victory']= winners.tot_count/winners.tot_matches
winners= winners[winners.tot_matches >= 100] #getting only clubs who have played at least 100 matches
winners_pct= winners[['pct_home_victory', 'pct_victory_away', 'tot_pct_victory']]
losers['tot_count']= losers.home_count + losers.away_count
losers['tot_matches']= losers.home_matches + losers.away_matches
losers['tot_pct_defeats']= losers.tot_count/losers.tot_matches
losers= losers[losers.tot_matches >= 100] #getting only clubs who have played at least 100 matches
losers_pct= losers[['pct_home_defeats', 'pct_away_defeats', 'tot_pct_defeats']]

# Constants
img_width = 1600
img_height = 900
scale_factor = 0.5

# Add image
layout= go.Layout(images= [dict(
    source='https://images-na.ssl-images-amazon.com/images/I/41mFbk10Q-L._AC_SY700_.jpg',
    xref= "x",
    yref= "y",
    x= 0,
    y= 0,
    sizex= 500,
    sizey= 500,
    sizing= "stretch",
    opacity= .5,
    layer= "below")])
map = go.Figure()

# Add surface trace
map.add_trace(
    go.Choropleth(
        name="Winner",
        locations = winners_pct.index.values,
        locationmode='country names',
        colorscale =  [[0,'red'], [0.33, 'brown'], [0.66, 'yellow'], [1.0, 'green']],
        colorbar_title =  'Winning % of Teams',
        colorbar_ticksuffix = '%',
        z=winners_pct['tot_pct_victory']*100
    )
)
map.add_trace(
    go.Choropleth(
        name="Loser",
        locations = losers_pct.index.values,
        locationmode='country names',
        colorscale =  [[0,'green'], [0.33, 'yellow'], [0.66, 'brown'], [1.0, 'red']],
        colorbar_title = 'Losing % of Teams',
        colorbar_ticksuffix = '%',
        visible=False,
        z=losers_pct['tot_pct_defeats']*100
    )
)
map.add_trace(
    go.Choropleth(
        name="Winner",
        locations = home_winners.index.values,
        locationmode='country names',
        colorscale =  [[0,'red'], [0.33, 'brown'], [0.66, 'yellow'], [1.0, 'green']],
        colorbar_title = 'Winning % of Home Teams',
        colorbar_ticksuffix = '%',
        visible=False,
        z=home_winners['pct_home_victory']*100
    )
)
map.add_trace(
    go.Choropleth(
        name="Loser",
        locations = home_losers.index.values,
        locationmode='country names',
        colorscale =  [[0,'green'], [0.33, 'yellow'], [0.66, 'brown'], [1.0, 'red']],
        colorbar_title = 'Losing % of Home Teams',
        colorbar_ticksuffix = '%',
        visible=False,
        z=home_losers['pct_home_victory']*100
    )
)
map.add_trace(
    go.Choropleth(
        name="Winner",
        locations = away_winners.index.values,
        locationmode='country names',
        colorscale =  [[0,'red'], [0.33, 'brown'], [0.66, 'yellow'], [1.0, 'green']],
        colorbar_title = 'Winning % of Away Teams',
        colorbar_ticksuffix = '%',
        visible=False,
        z=away_winners['pct_victory_away']*100
    )
)
map.add_trace(
    go.Choropleth(
        name="Loser",
        locations = away_losers.index.values,
        locationmode='country names',
        colorscale =  [[0,'green'], [0.33, 'yellow'], [0.66, 'brown'], [1.0, 'red']],
        colorbar_title = 'Losing % of Away Teams',
        colorbar_ticksuffix = '%',
        visible=False,
        z=away_losers['pct_victory_away']*100
    )
)

map.update_layout(
    title_text='WINNERS AND LOSERS',
    #annotation
    annotations=[
        go.layout.Annotation(text="Value :", showarrow=False,
                             x=0, y=1.05, yref="paper", align="left")
    ],
    # Add dropdown
    updatemenus=[
        go.layout.Updatemenu(
            buttons=list([
                dict(
                    args=[{"visible": [True, False, False, False, False, False]}],
                    label="Teams Winning Percentage",
                    method="restyle"
                ),
                dict(
                    args=[{"visible": [False, True, False, False, False, False]}],
                    label="Teams Losing Percentage",
                    method="restyle"
                ),
                dict(
                    args=[{"visible": [False, False, True, False, False, False]}],
                    label="Home Teams Winning Percentage",
                    method="restyle"
                ),
                dict(
                    args=[{"visible": [False, False, False, True, False, False]}],
                    label="Home Teams Losing Percentage",
                    method="restyle"
                ),
                dict(
                    args=[{"visible": [False, False, False, False, True, False]}],
                    label="Away Teams Winning Percentage",
                    method="restyle"
                ),
                dict(
                    args=[{"visible": [False, False, False, False, False, True]}],
                    label="Away Teams Losing Percentage",
                    method="restyle"
                )
            ]),
            direction="down",
            pad={"r": 10, "t": 10},
            showactive=True,
            x=0.06,
            xanchor="left",
            y=1.085,
            yanchor="top"
        ),
    ],
    geo=dict(
        showframe=False,
        showcoastlines=False,
        showlakes=True,
        lakecolor='#69d4ff',
        showocean=True,
        oceancolor='#69d4ff',
        projection_type='orthographic'#equirectangle
    )
)
map.update_layout(template="plotly_dark")

py.offline.plot(map)

