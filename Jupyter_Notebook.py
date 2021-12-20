#!/usr/bin/env python
# coding: utf-8

# In[ ]:


get_ipython().system('pip install pandas')
get_ipython().system('pip install numpy')
get_ipython().system('pip install plotly')


# In[ ]:


#importing packages
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go 


# In[ ]:


#importing dataframes as csv
confirmed_cases_df = pd.read_csv('covid_confirmed_cases.csv')
confirmed_deaths_df = pd.read_csv('confirmed_deaths.csv')


# # Data Manipulation and Cleaning

# In[ ]:


#dropping columns that I don't need
confirmed_cases_df = confirmed_cases_df.drop(columns=['Lat', 'Long', 'Province/State'])
confirmed_deaths_df = confirmed_deaths_df.drop(columns=['Lat', 'Long', 'Province/State'])


# In[ ]:


#group data by Country
confirmed_cases_df = confirmed_cases_df.groupby(by='Country/Region').aggregate(np.sum).T
confirmed_cases_df.index.name = 'Date'
confirmed_cases_df = confirmed_cases_df.reset_index()
confirmed_deaths_df = confirmed_deaths_df.groupby(by='Country/Region').aggregate(np.sum).T
confirmed_deaths_df.index.name = 'Date'
confirmed_deaths_df = confirmed_deaths_df.reset_index()


# In[ ]:


#melting the data
confirmed_cases_melt_df = confirmed_cases_df.melt(id_vars='Date').copy()
confirmed_cases_melt_df.rename(columns={'value':'Confirmed'}, inplace=True)
confirmed_deaths_melt_df = confirmed_deaths_df.melt(id_vars='Date').copy()
confirmed_deaths_melt_df.rename(columns={'value':'Confirmed'}, inplace=True)


# In[ ]:


#formatting the date 
confirmed_cases_melt_df['Date'] = pd.to_datetime(confirmed_cases_melt_df['Date'])
confirmed_cases_melt_df['Date'] = confirmed_cases_melt_df['Date'].dt.strftime('%d/%m/%Y')
confirmed_deaths_melt_df['Date'] = pd.to_datetime(confirmed_deaths_melt_df['Date'])
confirmed_deaths_melt_df['Date'] = confirmed_deaths_melt_df['Date'].dt.strftime('%d/%m/%Y')


# In[ ]:


max_date = confirmed_cases_melt_df['Date'].max()
max_date


# In[ ]:


total_confirmed_df = confirmed_cases_melt_df[confirmed_cases_melt_df['Date'] == max_date]
total_confirmed = total_confirmed_df['Confirmed'].sum()
total_confirmed


# In[ ]:


total_death_df = confirmed_deaths_melt_df[confirmed_deaths_melt_df['Date'] == max_date]
total_death = total_death_df['Confirmed'].sum()
total_death


# In[ ]:


total_active = total_confirmed - total_death
total_active


# # Data Visualization

# In[ ]:


#create a new df
total_confirmed_df = confirmed_cases_melt_df[confirmed_cases_melt_df['Date'] == max_date]
total_confirmed_df


# In[ ]:


total_confirmed = total_confirmed_df['Confirmed'].sum()
total_confirmed


# In[ ]:


fig = px.bar(total_confirmed_df.sort_values('Confirmed', ascending=False).head(30)
             , x='Country/Region', y='Confirmed', text='Confirmed')
fig.show()


# In[ ]:


fig2 = px.scatter(confirmed_cases_melt_df, x='Date', y='Confirmed', color='Country/Region')
fig2.show()

#would only work when using the US spelling of colour 


# In[ ]:


fig3 = px.line(confirmed_cases_melt_df[confirmed_cases_melt_df['Country/Region'] == 'Ireland'], x='Date', y='Confirmed')
fig3.show()


# In[ ]:




