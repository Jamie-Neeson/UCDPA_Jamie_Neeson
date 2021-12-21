#!/usr/bin/env python
# coding: utf-8

# In[1]:


get_ipython().system('pip install pandas')
get_ipython().system('pip install numpy')
get_ipython().system('pip install plotly')
get_ipython().system('pip install matplotlib')


# In[2]:


#importing packages
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go 
import matplotlib.pyplot as plt


# In[3]:


#importing dataframes as csv
confirmed_cases_df = pd.read_csv('covid_confirmed_cases.csv')
confirmed_deaths_df = pd.read_csv('confirmed_deaths.csv')


# # Data Manipulation and Cleaning

# In[4]:


#dropping columns that I don't need
confirmed_cases_df = confirmed_cases_df.drop(columns=['Lat', 'Long', 'Province/State'])
confirmed_deaths_df = confirmed_deaths_df.drop(columns=['Lat', 'Long', 'Province/State'])
confirmed_deaths_df.head()


# In[5]:


#group data by Country
confirmed_cases_df = confirmed_cases_df.groupby(by='Country/Region').aggregate(np.sum).T
confirmed_cases_df.index.name = 'Date'
confirmed_cases_df = confirmed_cases_df.reset_index()
confirmed_deaths_df = confirmed_deaths_df.groupby(by='Country/Region').aggregate(np.sum).T
confirmed_deaths_df.index.name = 'Date'
confirmed_deaths_df = confirmed_deaths_df.reset_index()
confirmed_cases_df.head()


# In[6]:


#melting the data
confirmed_cases_melt_df = confirmed_cases_df.melt(id_vars='Date').copy()
confirmed_cases_melt_df.rename(columns={'value':'Confirmed'}, inplace=True)
confirmed_deaths_melt_df = confirmed_deaths_df.melt(id_vars='Date').copy()
confirmed_deaths_melt_df.rename(columns={'value':'Confirmed'}, inplace=True)
confirmed_cases_melt_df.head()


# In[7]:


#formatting the date 
confirmed_cases_melt_df['Date'] = pd.to_datetime(confirmed_cases_melt_df['Date'])
confirmed_cases_melt_df['Date'] = confirmed_cases_melt_df['Date'].dt.strftime('%d/%m/%Y')
confirmed_deaths_melt_df['Date'] = pd.to_datetime(confirmed_deaths_melt_df['Date'])
confirmed_deaths_melt_df['Date'] = confirmed_deaths_melt_df['Date'].dt.strftime('%d/%m/%Y')


# In[8]:


max_date = confirmed_cases_melt_df['Date'].max()
max_date


# In[9]:


total_confirmed_df = confirmed_cases_melt_df[confirmed_cases_melt_df['Date'] == max_date]
total_confirmed = total_confirmed_df['Confirmed'].sum()
total_confirmed


# In[10]:


total_death_df = confirmed_deaths_melt_df[confirmed_deaths_melt_df['Date'] == max_date]
total_death = total_death_df['Confirmed'].sum()
total_death


# In[11]:


total_active = total_confirmed - total_death
total_active


# # Data Visualization

# In[12]:


#create a new df
total_confirmed_df = confirmed_cases_melt_df[confirmed_cases_melt_df['Date'] == max_date]
total_confirmed_df


# In[13]:


total_confirmed = total_confirmed_df['Confirmed'].sum()
total_confirmed


# In[14]:


fig = px.bar(total_confirmed_df.sort_values('Confirmed', ascending=False).head(30)
             , x='Country/Region', y='Confirmed', text='Confirmed')
fig.show()


# In[15]:


fig2 = px.scatter(confirmed_deaths_melt_df, x='Date', y='Confirmed', color='Country/Region')
fig2.show()

#would only work when using the US spelling of colour 
#scatter graph shows the total confirm dealths


# In[16]:


fig3 = px.line(confirmed_cases_melt_df[confirmed_cases_melt_df['Country/Region'] == 'Ireland'], x='Date', y='Confirmed')
fig3.show()


# In[17]:


plt.scatter(x='Country/Region', y='Confirmed', data=confirmed_cases_melt_df, s=10)


# In[18]:


fig4 = px.choropleth(total_confirmed_df, 
                     locations='Country/Region', locationmode='country names',
                     color_continuous_scale='Rainbow',
                     color=total_confirmed_df['Confirmed'], height=500)                                                                     
fig4.show()


# In[19]:


fig5 = px.scatter(total_confirmed_df, x='Confirmed', y='Confirmed', color=total_confirmed_df['Country/Region'],
                  size='Confirmed', log_x=True, height=500)
fig5.show()

