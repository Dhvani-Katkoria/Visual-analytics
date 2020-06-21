


import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import seaborn as sns
import os
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')


# In[4]:


# rankings = pd.read_csv('/home/vidhikatkoria/Downloads/international-football-results-from-1872-to-2017/results.csv')

matches = pd.read_csv("../Source/results.csv")
matches =  matches.replace({'Germany DR': 'Germany', 'China': 'China PR'})
matches['date'] = pd.to_datetime(matches['date'])
matches.head()


# In[ ]:


matches = matches.merge(rankings,
                         left_on=['date', 'home_team'],
                         right_on=['rank_date', 'country_full'])
# matches.head()

matches = matches.merge(rankings, 
                        left_on=['date', 'away_team'], 
                        right_on=['rank_date', 'country_full'], 
                        suffixes=('_home', '_away'))
matches.head()


# In[6]:


import pandas as pd
import numpy as np

match= pd.read_csv('/home/vidhikatkoria/Downloads/international-football-results-from-1872-to-2017/results.csv')

#put date in correct format and set it as the index
date= pd.to_datetime(match.date.values)
match['date']=date
match.set_index('date', inplace=True)


#get the coloumn of results (wins, ties and losses)
win= np.where(match.home_score > match.away_score, 'win', None)
tie=np.where(match.home_score == match.away_score, 'tie', None)
loss= np.where(match.home_score < match.away_score, 'loss', None)

results=pd.DataFrame([win, tie, loss]).T
results
x=[value[value != None]  for value in results.values]
#x=np.array(x)
#x=x.tolist()
match['result']= x
match['result']=np.squeeze(match.result.tolist())

#get the number of goals
match['goals']= match.home_score + match.away_score


#home
home_teams=match.groupby(['home_team','result']).count()['city'].sort_values(ascending=False).reset_index().rename(columns={'city': 'count'})


home_matches=[]
for team in home_teams.home_team:
    tot_matches= home_teams[home_teams.home_team== team]['count'].sum()
    home_matches.append(tot_matches)
   
home_teams['home_matches']=home_matches
home_teams['pct_home_victory']= home_teams['count']/ home_teams['home_matches']


#away
away_teams=match.groupby(['away_team','result']).count()['city'].sort_values(ascending=False).reset_index().rename(columns={'city': 'count'})
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


#total percentage
winners_pct.sort_values(by='tot_pct_victory', ascending=False)
winners_pct=np.round(winners_pct*100, 2)
winners_pct['tot_count']= winners.tot_count
winners_pct['tot_matches']= winners.tot_matches


losers_pct=np.round(losers_pct*100, 2)
losers_pct['tot_count']= losers.tot_count
losers_pct['tot_matches']= losers.tot_matches


winners_pct.sort_values(by='tot_pct_victory', ascending=False)


# In[13]:


winnersp = winners_pct.sort_values(by='tot_pct_victory', ascending=False)
winners16 = winnersp.head(16)
winners16


# In[15]:


shuffled = winners16.sample(frac=1)
result = np.array_split(shuffled, 8) 
# for part in result:
#     print(part,"\n")


# In[52]:


labels=[]
vic_ratio=[]
for part in result:
    match = str(part.index[0])+" vs "+ str(part.index[1])
    labels.append(match)
    win_ratio = list((float(part.tot_pct_victory[0]),float(part.tot_pct_victory[1])))
    vic_ratio.append(win_ratio)
best16_labels = labels
print(best16_labels)


# In[53]:


quaterfinal=[]
quaterfinal_team =[]
quaterfinal_team_ratio =[]
for i in range(0,8,2):
    if (float(result[i].tot_pct_victory[0]) > float(result[i].tot_pct_victory[1])):
        if (float(result[i+1].tot_pct_victory[0]) > float(result[i+1].tot_pct_victory[1])):
            match = str(result[i].index[0])+" vs "+ str(result[i+1].index[0])
            win_ratio = list((float(result[i].tot_pct_victory[0]),float(result[i+1].tot_pct_victory[0])))
            quaterfinal_team.append(result[i].index[0])
            quaterfinal_team.append(result[i+1].index[0])
            quaterfinal_team_ratio.append((float(result[i].tot_pct_victory[0])))
            quaterfinal_team_ratio.append((float(result[i+1].tot_pct_victory[0])))
        else:
            match = str(result[i].index[0])+" vs "+ str(result[i+1].index[1])
            win_ratio = list((float(result[i].tot_pct_victory[0]),float(result[i+1].tot_pct_victory[1])))
            quaterfinal_team.append(result[i].index[0])
            quaterfinal_team.append(result[i+1].index[1])
            quaterfinal_team_ratio.append((float(result[i].tot_pct_victory[0])))
            quaterfinal_team_ratio.append((float(result[i+1].tot_pct_victory[1])))
    else:
        if (float(result[i+1].tot_pct_victory[0]) > float(result[i+1].tot_pct_victory[1])):
            match = str(result[i].index[1])+" vs "+ str(result[i+1].index[0])
            win_ratio = list((float(result[i].tot_pct_victory[1]),float(result[i+1].tot_pct_victory[0])))
            quaterfinal_team.append(result[i].index[1])
            quaterfinal_team.append(result[i+1].index[0])
            quaterfinal_team_ratio.append((float(result[i].tot_pct_victory[1])))
            quaterfinal_team_ratio.append((float(result[i+1].tot_pct_victory[0])))
        else:
            match = str(result[i].index[1])+" vs "+ str(result[i+1].index[1])
            win_ratio = list((float(result[i].tot_pct_victory[1]),float(result[i+1].tot_pct_victory[1])))
            quaterfinal_team.append(result[i].index[1])
            quaterfinal_team.append(result[i+1].index[1])
            quaterfinal_team_ratio.append((float(result[i].tot_pct_victory[1])))
            quaterfinal_team_ratio.append((float(result[i+1].tot_pct_victory[1])))
    quaterfinal.append(match)
    labels.append(match)
    vic_ratio.append(win_ratio)
print(quaterfinal_team)
print(quaterfinal_team_ratio)


# In[57]:


semifinal_team=[]
semifinal_win_ratio = []

for i in range(0,8,2):
    if (quaterfinal_team_ratio[i] > quaterfinal_team_ratio[i+1]):
        semifinal_team.append(quaterfinal_team[i])
        semifinal_win_ratio.append(quaterfinal_team_ratio[i])
    else:
        semifinal_team.append(quaterfinal_team[i+1])
        semifinal_win_ratio.append(quaterfinal_team_ratio[i+1])

match = str(semifinal_team[0])+" vs "+ str(semifinal_team[1])
win_ratio = list((float(semifinal_win_ratio[0]),float(semifinal_win_ratio[1]))) 
labels.append(match)
vic_ratio.append(win_ratio)
match = str(semifinal_team[2])+" vs "+ str(semifinal_team[3])
win_ratio = list((float(semifinal_win_ratio[2]),float(semifinal_win_ratio[3]))) 
labels.append(match)
vic_ratio.append(win_ratio)
print(labels)
print(vic_ratio)


# In[58]:


final_team=[]
final_win_ratio=[]
for i in range(0,4,2):
    if (semifinal_win_ratio[i] > semifinal_win_ratio[i+1]):
        final_team.append(semifinal_team[i])
        final_win_ratio.append(semifinal_win_ratio[i])
    else:
        final_team.append(semifinal_team[i+1])
        final_win_ratio.append(semifinal_win_ratio[i+1])

match = str(final_team[0])+" vs "+ str(final_team[1])
win_ratio = list((float(final_win_ratio[0]),float(final_win_ratio[1]))) 
labels.append(match)
vic_ratio.append(win_ratio)
print(labels)
print(vic_ratio)


# In[74]:


import networkx as nx
import pydot
from networkx.drawing.nx_pydot import graphviz_layout

node_sizes = pd.DataFrame(vic_ratio)
scale_factor = 0.3 # for visualization
G = nx.balanced_tree(2, 3)
pos = graphviz_layout(G, prog='twopi')
centre = pd.DataFrame(pos).mean(axis=1).mean()

plt.figure(figsize=(10, 10))
ax = plt.subplot(1,1,1)
# add circles 
circle_positions = [(220, 'black'), (170, 'blue'), (100, 'red'), (60, 'yellow')]
[ax.add_artist(plt.Circle((centre, centre), 
                          cp, color='Yellow', 
                          alpha=0.2)) for cp, c in circle_positions]

# draw first the graph
nx.draw(G, pos, 
        node_color=node_sizes.diff(axis=1)[1].abs().pow(scale_factor), 
        node_size=node_sizes.diff(axis=1)[1].abs().pow(scale_factor)*1000, 
        alpha=1, 
        cmap='Greens',
        edge_color='black',
        width=10,
        with_labels=False)

# draw the custom node labels
shifted_pos = {k:[(v[0]-centre)*0.9+centre,(v[1]-centre)*0.9+centre] for k,v in pos.items()}
nx.draw_networkx_labels(G, 
                        pos=shifted_pos, 
                        bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="black", lw=.5, alpha=1),
                        labels=dict(zip(reversed(range(len(labels))), labels)))

texts = ((10, 'Best 16', 'black'), (70, 'Quarter-\nfinal', 'blue'), (130, 'Semifinal', 'red'), (190, 'Final', 'yellow'))
[plt.text(p, centre+20, t, 
          fontsize=12, color='grey', 
          va='center', ha='center') for p,t,c in texts]
plt.axis('equal')
plt.title('Prediction based on history victory ratio', fontsize=20)
plt.show()


# In[ ]:




