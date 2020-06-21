


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.plotly as py
import plotly.graph_objs as go 
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
import cufflinks as cf
init_notebook_mode(connected=True)
cf.go_offline()
get_ipython().run_line_magic('matplotlib', 'inline')


# In[6]:


data = pd.read_csv("../Source/results.csv")


# In[7]:


def result(row):
      
    if row['home_score'] > row['away_score']:
        return row['home_team']
    elif row['home_score'] < row['away_score']:
        return row['away_team']
    else:
        return('Tie')


# In[8]:


data['results'] = data[['home_score','away_score','home_team','away_team']].apply(result,axis=1)
data.head(2)


# In[9]:


data['date'] = pd.to_datetime(data['date'])
time = data['date'].iloc[0]
time.year


# In[10]:


data['month'] = data['date'].apply(lambda time: time.month)
data['year']  = data['date'].apply(lambda time: time.year)


# In[11]:


data['month'] = data['month'].map({1:'Jan', 2:'Feb', 3:'Mar', 4:'Apr', 5:'May', 6:'Jun', 7:'Jul', 8:'Aug', 9:'Sep', 
                                 10:'Oct', 11:'Nov', 12:'Dec'})


# In[12]:


match_count = data['year'].value_counts()
match_count.head(2)


# In[13]:


plt.figure(figsize=(20,8))
sns.lineplot(match_count.index, match_count.values, color='red', lw=2)
plt.title('Number of international soccer games', fontsize=20)
plt.ylabel('No of matches', fontsize=12)
plt.xlabel('Year', fontsize=12)


# In[14]:


plt.figure(figsize=(20,8))
sns.countplot(x='results',data=data, order =data['results'].value_counts()[1:20].index)
plt.title('Top 20 Countries with most wins', fontsize=20)
plt.ylabel('No of wins', fontsize=12)
plt.xlabel('Country', fontsize=12)


# In[15]:


brazil = data[data['results']=='Brazil']['city'].value_counts()[:20]
plt.figure(figsize=(18,10))
sns.barplot(brazil.values,brazil.index,palette='autumn')
plt.title("Favourite grounds for Brazil when they win", fontsize=20)
plt.ylabel('City', fontsize=12)
plt.xlabel('No of times won', fontsize=12)


# In[16]:


tour = data['tournament'].value_counts()
data1 = dict(
      values = tour.values[:20],
      labels = tour.index[:20],
      domain = {"x": [0, .5]},
      hoverinfo = "label+percent+name",
      type =  "pie")
layout1 = dict(
        title =  "Top 20 most played Leagues",
            )
fig = go.Fi


# In[17]:


total_scores = data[['home_score','away_score','country','month','year']]
total_scores['total_score'] = total_scores['home_score'] + total_scores['away_score']
total_scores.head()


# In[18]:


plt.figure(figsize=(25,10))
dj = total_scores.pivot_table(index='month',columns='year',values='total_score')
sns.heatmap(dj,cmap='cividis_r',linecolor='white', lw = 0.2)
plt.title('Goals scored across each month and year', fontsize=20)
plt.ylabel('Years', fontsize=12)
plt.xlabel('Months', fontsize=12)


# In[26]:


country_grouped = total_scores.groupby('country').sum().sort_values('total_score',ascending=False)[:30]
ax = plt.figure(figsize=(15,14))
sns.barplot(x="total_score", y=country_grouped.index, data=country_grouped, color ='yellow', label="Total_score")
sns.barplot(x="home_score", y=country_grouped.index, data=country_grouped, color = 'green', label="Home_score")
ax.legend(ncol=2, loc="upper right", frameon=True)
plt.title("Total & Home goals scored in the country's History", fontsize=20)
plt.ylabel('Country', fontsize=12)
plt.xlabel('No of goals', fontsize=12)


# In[22]:


aaa= data['home_team'].value_counts()
bbb = data['away_team'].value_counts()
team_matches = pd.concat([aaa,bbb],axis=1)

team_matches.columns = ['home_matches','away_matches']
team_matches['total_matches'] = team_matches['home_matches'] + team_matches['away_matches']
team_matches_sort = team_matches.sort_values('total_matches',ascending=False)


# In[98]:


team_matches_sort.iplot(kind='scatter',title='Number of matches played', xTitle='Country', yTitle='No of matches',theme='pearl')


# In[94]:


total_teams = data[['country','year']]
# total_teams['total_teams'] = total_teams['country'].sum()
# total_teams.head()
tt=total_teams.groupby(['year','country']).sum()
# for i in tt.index:
#     print(i,tt.index[i])
#     print(tt.country[i].sum())
#     data.loc[data['year']==str(i),'country'].agg(['nunique'])
# tt.country
df = data.groupby('year')['country'].nunique()
country_count=[]
year = list(df.index)
for i in df:
    country_count.append(i)
print(year)


# In[97]:


df = pd.DataFrame(list(zip(year, country_count)), 
               columns =['year', 'country']) 
plt.figure(figsize=(20,8))
sns.lineplot(df.year, df.country, color='blue', lw=2)
plt.title('Number of international soccer teams', fontsize=20)
plt.ylabel('No of teams', fontsize=12)
plt.xlabel('Year', fontsize=12)


# In[ ]:




