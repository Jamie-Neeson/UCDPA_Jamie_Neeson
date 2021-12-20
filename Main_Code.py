#importing packages
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

#importing dataframe as csv
confirmed_df = pd.read_csv('covid_confirmed_cases.csv')
confirmed_df


# # Data Manipulation and Cleaning
confirmed_df = confirmed_df.drop(columns=['Lat', 'Long', 'Province/State'])
confirmed_df.head()

confirmed_df = confirmed_df.groupby(by='Country/Region').aggregate(np.sum).T
confirmed_df

confirmed_df.index.name = 'Date'
confirmed_df = confirmed_df.reset_index()
confirmed_df.tail()

confirmed_melt_df = confirmed_df.melt(id_vars='Date').copy()
confirmed_melt_df

confirmed_melt_df.rename(columns={'value':'Confirmed'}, inplace=True)
confirmed_melt_df

max_date = confirmed_melt_df['Date'].max()
max_date

confirmed_melt_df['Date'] = pd.to_datetime(confirmed_melt_df['Date'])
confirmed_melt_df.head()

confirmed_melt_df['Date'] = confirmed_melt_df['Date'].dt.strftime('%d/%m/%Y')
max_date = confirmed_melt_df['Date'].max()
max_date

#Data Visualization

#create a new df for total confirmed cases
total_confirmed_df = confirmed_melt_df[confirmed_melt_df['Date'] == max_date]
total_confirmed_df

total_confirmed = total_confirmed_df['Confirmed'].sum()
total_confirmed


fig = px.bar(total_confirmed_df.sort_values('Confirmed', ascending=False).head(30)
             , x='Country/Region', y='Confirmed', text='Confirmed')
fig.show()

fig2 = px.scatter(confirmed_melt_df, x='Date', y='Confirmed', color='Country/Region')
fig2.show()

fig3 = px.line(confirmed_melt_df[confirmed_melt_df['Country/Region'] == 'Ireland'], x='Date', y='Confirmed')
fig3.show()