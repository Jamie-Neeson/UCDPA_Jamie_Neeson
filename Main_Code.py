get_ipython().system('pip install pandas')
get_ipython().system('pip install numpy')
get_ipython().system('pip install plotly')
get_ipython().system('pip install matplotlib')

#importing packages
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go 
import matplotlib.pyplot as plt

#importing dataframes as csv
confirmed_cases_df = pd.read_csv('covid_confirmed_cases.csv')
confirmed_deaths_df = pd.read_csv('confirmed_deaths.csv')

#Data Manipulation and Cleaning

#dropping columns that I don't need
confirmed_cases_df = confirmed_cases_df.drop(columns=['Lat', 'Long', 'Province/State'])
confirmed_deaths_df = confirmed_deaths_df.drop(columns=['Lat', 'Long', 'Province/State'])
confirmed_deaths_df.head()

#group data by Country
confirmed_cases_df = confirmed_cases_df.groupby(by='Country/Region').aggregate(np.sum).T
confirmed_cases_df.index.name = 'Date'
confirmed_cases_df = confirmed_cases_df.reset_index()
confirmed_deaths_df = confirmed_deaths_df.groupby(by='Country/Region').aggregate(np.sum).T
confirmed_deaths_df.index.name = 'Date'
confirmed_deaths_df = confirmed_deaths_df.reset_index()
confirmed_cases_df.head()

#melting the data
confirmed_cases_melt_df = confirmed_cases_df.melt(id_vars='Date').copy()
confirmed_cases_melt_df.rename(columns={'value':'Confirmed'}, inplace=True)
confirmed_deaths_melt_df = confirmed_deaths_df.melt(id_vars='Date').copy()
confirmed_deaths_melt_df.rename(columns={'value':'Confirmed'}, inplace=True)
confirmed_cases_melt_df.head()

#formatting the date 
confirmed_cases_melt_df['Date'] = pd.to_datetime(confirmed_cases_melt_df['Date'])
confirmed_cases_melt_df['Date'] = confirmed_cases_melt_df['Date'].dt.strftime('%d/%m/%Y')
confirmed_deaths_melt_df['Date'] = pd.to_datetime(confirmed_deaths_melt_df['Date'])
confirmed_deaths_melt_df['Date'] = confirmed_deaths_melt_df['Date'].dt.strftime('%d/%m/%Y')

max_date = confirmed_cases_melt_df['Date'].max()
max_date

total_confirmed_df = confirmed_cases_melt_df[confirmed_cases_melt_df['Date'] == max_date]
total_confirmed = total_confirmed_df['Confirmed'].sum()
total_confirmed

total_death_df = confirmed_deaths_melt_df[confirmed_deaths_melt_df['Date'] == max_date]
total_death = total_death_df['Confirmed'].sum()
total_death

total_active = total_confirmed - total_death
total_active

#Data Visualization
total_confirmed_df = confirmed_cases_melt_df[confirmed_cases_melt_df['Date'] == max_date]
total_confirmed_df

total_confirmed = total_confirmed_df['Confirmed'].sum()
total_confirmed

#5 visualizations
fig = px.bar(total_confirmed_df.sort_values('Confirmed', ascending=False).head(30)
             , x='Country/Region', y='Confirmed', text='Confirmed', title='Total COVID 19 cases, all countries')
fig.show()

fig2 = px.scatter(confirmed_deaths_melt_df, x='Date', y='Confirmed', color='Country/Region', 
                  title='Increase in COVID 19 deaths by date, all countries')
fig2.show()

fig3 = px.line(confirmed_cases_melt_df[confirmed_cases_melt_df['Country/Region'] == 'Ireland'], 
               x='Date', y='Confirmed', title='Increase in COVID 19 cases by date, individual country')
fig3.show()

#same data visualized using matplotlib, comparing with fig3, plotly is a much better option 
plt.scatter(x='Country/Region', y='Confirmed', data=confirmed_cases_melt_df, s=10)
plt.show()

fig4 = px.choropleth(total_confirmed_df, 
                     locations='Country/Region', locationmode='country names',
                     color_continuous_scale='Rainbow',
                     color=total_confirmed_df['Confirmed'], height=500, title='World map of all COVID 19 cases')                                                                     
fig4.show()

fig5 = px.scatter(total_confirmed_df, x='Confirmed', y='Confirmed', color=total_confirmed_df['Country/Region'],
                  size='Confirmed', log_x=True, height=500, title='Total COVID 19 cases, all countries')
fig5.show()
