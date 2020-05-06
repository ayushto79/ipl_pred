#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np


# #### Matches dataset

# In[2]:


matches = pd.read_excel(r"C:\Users\LAPTOP\Desktop\Ayush_Project\matches.xlsx")


# In[4]:


matches.head()


# Dropping rows where match result is unknown since it is a draw

# In[5]:


matches = matches.dropna(subset = ['winner'])


# Changing name of teams
# 1) Pune Warriors -> Rising Pune Supergiants (RPS)
# 2) Delhi Capitals -> Delhi Daredevils (DD)

# In[6]:


matches.replace(['Mumbai Indians','Kolkata Knight Riders','Royal Challengers Bangalore','Deccan Chargers','Chennai Super Kings','Rajasthan Royals','Delhi Daredevils','Gujarat Lions','Kings XI Punjab','Sunrisers Hyderabad','Rising Pune Supergiants','Rising Pune Supergiant','Kochi Tuskers Kerala','Pune Warriors','Delhi Capitals'],['MI','KKR','RCB','DC','CSK','RR','DD','GL','KXIP','SRH','RPS','RPS','KTK','RPS','DD'],inplace=True)


# In[7]:


matches.head()


# Inserting Venue to Dubai for missing values

# In[8]:


matches['city'].fillna('Dubai',inplace = True)


# In[9]:


matches = matches.drop(['dl_applied','umpire1','umpire2','umpire3','result','player_of_match','venue'],axis=1)


# In[10]:


matches.head()


# In[11]:


matches['date'] = pd.to_datetime(matches.date, format='%y-%m-%d')


# In[12]:


matches = matches.sort_values(by = 'date')


# In[13]:


matches.head()


# #### Deliveries dataset

# In[41]:


deliveries = pd.read_csv(r"C:\Users\LAPTOP\Desktop\Ayush_Project\deliveries.csv")


# In[42]:


deliveries.head()


# Inserting 0 where player wasn't dismissed and 1 where player was dismissed

# In[43]:


deliveries["player_dismissed"] = deliveries["player_dismissed"].fillna(0)


# In[44]:


deliveries["player_dismissed"] = deliveries["player_dismissed"].where(deliveries["player_dismissed"] == 0, 1)


# Batting statistics

# In[45]:


del1 = deliveries.groupby(['match_id','batting_team'])['total_runs'].sum().reset_index()


# In[46]:


del1= del1.pivot(index='match_id',columns='batting_team',values='total_runs').reset_index().fillna(0)


# In[47]:


del1.head()


# In[48]:


data_bat = matches.merge(del1,how ='left', left_on='id', right_on = 'match_id').drop(columns=['season'])


# In[49]:


data_bat.head()


# In[50]:


data_bat['DD'] = data_bat['Delhi Capitals'] + data_bat['Delhi Daredevils']
data_bat['RPS'] = data_bat['Rising Pune Supergiant'] + data_bat['Rising Pune Supergiants'] + data_bat['Pune Warriors']
data_bat = data_bat.drop(columns=['Delhi Capitals','Delhi Daredevils','Rising Pune Supergiant','Rising Pune Supergiants','Pune Warriors'])


# In[51]:


data_bat = data_bat.rename(columns = {'Mumbai Indians':'MI','Kolkata Knight Riders':'KKR','Royal Challengers Bangalore':'RCB','Deccan Chargers':'DC','Chennai Super Kings':'CSK','Rajasthan Royals':'RR','Gujarat Lions':'GL','Kings XI Punjab':'KXIP','Sunrisers Hyderabad':'SRH','Kochi Tuskers Kerala':'KTK'})


# In[52]:


data_bat.head()


# In[53]:


data_bat['team1_bat'] = 0
data_bat['team2_bat'] = 0


# In[54]:


for i in range(len(data_bat)):
    data_bat['team1_bat'][i] =   data_bat[data_bat['team1'][i]][i]
    data_bat['team2_bat'][i] =   data_bat[data_bat['team2'][i]][i]


# In[55]:


data_bat.head()


# In[56]:


data_bat = data_bat.drop(columns=['CSK','MI','RCB','KTK','RPS','KKR','KXIP','SRH','DC','DD','GL','RR'])


# In[57]:


data_bat


# Bowling statistics

# In[58]:


del2 = deliveries.groupby(['match_id','bowling_team'])['player_dismissed'].sum().reset_index()


# In[59]:


del2= del2.pivot(index='match_id',columns='bowling_team',values='player_dismissed').reset_index().fillna(0)


# In[60]:


del2


# In[61]:


del2['DD'] = del2['Delhi Capitals'] + del2['Delhi Daredevils']
del2['RPS'] = del2['Rising Pune Supergiant'] + del2['Rising Pune Supergiants'] + del2['Pune Warriors']
del2 = del2.drop(columns=['Delhi Capitals','Delhi Daredevils','Rising Pune Supergiant','Rising Pune Supergiants','Pune Warriors'])


# In[62]:


del2 = del2.rename(columns = {'Mumbai Indians':'MI','Kolkata Knight Riders':'KKR','Royal Challengers Bangalore':'RCB','Deccan Chargers':'DC','Chennai Super Kings':'CSK','Rajasthan Royals':'RR','Gujarat Lions':'GL','Kings XI Punjab':'KXIP','Sunrisers Hyderabad':'SRH','Kochi Tuskers Kerala':'KTK'})


# In[63]:


del2


# In[70]:


data_final = data_bat.merge(del2,how ='left', left_on='id', right_on = 'match_id').drop(columns=['id','match_id_x'])


# In[71]:


data_final


# team_bowl implies number of wickets taken by that particular team in the match

# In[72]:


data_final['team1_bowl'] = 0
data_final['team2_bowl'] = 0


# In[73]:


for i in range(len(data_final)):
    data_final['team1_bowl'][i] =   data_final[data_final['team1'][i]][i]
    data_final['team2_bowl'][i] =   data_final[data_final['team2'][i]][i]


# In[75]:


data_final.head()


# In[76]:


data_final = data_final.drop(columns=['CSK','MI','RCB','KTK','RPS','KKR','KXIP','SRH','DC','DD','GL','RR'])


# In[77]:


data_final


# In[ ]:




