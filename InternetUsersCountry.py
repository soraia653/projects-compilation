import pandas as pd
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt
import altair as alt

clean_users = pd.read_csv("clean_users.csv")

st.set_page_config(layout="wide")

st.sidebar.title("How does this visualization work?")
st.sidebar.write("This visualization uses data extracted from Kaggle and aims at presenting it in the most informative and user-friendly way possible.")

st.sidebar.subheader("The Map")
st.sidebar.write("The map is a simple way of visualizing all the available countries in our dataset. More functionalities will be added later on.")

st.sidebar.subheader("The First Visualization")
st.sidebar.write("This visualization is quite flexible, allowing you to focus on the countries you wish to learn more about, but also choose which metric to use.")

st.sidebar.subheader("The Pie Chart")
st.sidebar.write("A simple pie chart showing the top 5 countries with the highest number of internet users.")

st.sidebar.write(":warning:For the visualizations I'm using the values in their logarithmic form, but the original values are available in the raw dataset.")

st.title('Internet Users Per Country')
users = pd.read_csv('clean_users.csv', index_col = 0)

users['population_log'] = np.log(users['population'])
users['internet_users_log'] = np.log(users['internet_users'])

with st.beta_expander('Do you wish to see the raw data?') :
    st.write(users)
    
st.subheader('Map')
st.map(users)

## Bar chart where I can select the country and metric I want to visualize.

c1, c2 = st.beta_columns(2)

c1.subheader('Visualization #1')
c1.markdown(':warning:''The chart will appear once you select your first country.')

country_list = c1.multiselect(
    'What country do you want to focus on?',
    (users['country']))

metric_list = c1.selectbox(
    'What metric do you want to focus on?',
    ('population_log', 'percentage', 'internet_users_log'))

st.write('You selected:', metric_list)

data = users[['country', 'internet_users_log', 'population_log','percentage']][users['country'].isin(country_list)]

chart = alt.Chart(data).mark_bar().encode(alt.X('country'), y=metric_list,
    color = alt.Color('country',
                      legend=alt.Legend(title="Selected countries"))).properties(
    width=600,
    height=400).configure_axis(
    grid=False
)

if len(country_list) > 0 :
    c1.altair_chart(chart)

## Pie chart of the Top 5 countries (per internet users)

c2.subheader('Visualization #2')
c2.markdown('Top 5 countries with the highest number of internet users.')
  
# Pie chart data

sorted_data = users.sort_values(by='internet_users_log', ascending=False)

labels = list(sorted_data['country'].head(5))
sizes = list(sorted_data['internet_users_log'].head(5))

explode = (0.1, 0, 0, 0, 0) # Stands out bigger portion

colors = ['xkcd:sky blue',
          'xkcd:light green',      #Colors
          'xkcd:coral',
          'xkcd:cream',
          'xkcd:tangerine']

fig1, ax1 = plt.subplots()

fig_color, fig_countries, fig_perc = ax1.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f', shadow=False, startangle=90)

for autotext in fig_perc:
    autotext.set_color('grey')

# Equal aspect ratio ensures that pie is drawn as a circle.
ax1.axis('equal')

c2.pyplot(fig1)
