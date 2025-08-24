import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.figure_factory as ff

import preprocessing, helper
from helper import most_successful, top_athlete_per_country

# Load data
data = pd.read_csv("athlete_events.csv")
data_region = pd.read_csv("noc_regions.csv")

# Preprocess
data = preprocessing.preprocessor(data, data_region)
st.sidebar.title("Olympic Analysis")
st.sidebar.image("https://cdn.britannica.com/01/23901-050-33507FA4/flag-Olympic-Games.jpg")

# Sidebar Menu
user_menu = st.sidebar.radio(
    'Select an option',
    ('Medal Tally', 'Overall Analysis', 'Country-wise Analysis', 'Athlete-wise Analysis')
)

# Medal Tally
if user_menu == 'Medal Tally':
    st.sidebar.header('Medal Tally')
    year , country = helper.country_year_list(data)
    selected_year= st.sidebar.selectbox("Select Year", year )
    selected_country= st.sidebar.selectbox("Select Country", country)
    medal_tally = helper.fetch_medal_tally(data,selected_year,selected_country)
    if selected_year == "Overall" and selected_country == "Overall":
        st.title("Overall Tally")

    if selected_year != "Overall" and selected_country == "Overall":
        st.title("Medal Tally in " + str(selected_year) + " Olympics")

    if selected_year == "Overall" and selected_country != "Overall":
        st.title(selected_country + " Overall Performance")
    if selected_year != "Overall" and selected_country != "Overall":
            st.title("Performance of " + selected_country + " in " + str(selected_year) + " Olympics")
    st.table(medal_tally)

# Overall Analysis
if user_menu == "Overall Analysis":
    editions = len(data["Year"].unique()) - 1
    cities = len(data["City"].unique())
    sports = len(data["Sport"].unique())
    events = len(data["Event"].unique())
    athletes = len(data["Name"].unique())
    countries = len(data["region"].unique())

    st.title("Top Statistics")
    col1 , col2, col3 = st.columns(3)
    with col1:
        st.header("Editions")
        st.title(editions)
    with col2:
        st.header("Cities")
        st.title(cities)
    with col3:
        st.header("Sports")
        st.title(sports)
    col1, col2, col3 = st.columns(3)
    with col1:
        st.header("Events")
        st.title(events)
    with col2:
        st.header("Nations")
        st.title(countries)
    with col3:
        st.header("Athletes")
        st.title(athletes)

    nations_over_time = helper.nations_over_time(data)
    fig1 = px.line(nations_over_time, x="Year", y="count", markers=True)
    st.title("Total Nations participated over the Years")
    st.plotly_chart(fig1)

    events_over_time = helper.events_over_time(data)
    fig2 = px.line(events_over_time, x="Year", y="count", markers=True)
    st.title("Total Events over the Years")
    st.plotly_chart(fig2)

    athlete_over_time = helper.athlete_over_time(data)
    fig3 = px.line(athlete_over_time, x="Year", y="count", markers=True)
    st.title("Total Athletes participated over the Years")
    st.plotly_chart(fig3)

    st.title("Events over time in each Sport")
    fig , ax = plt.subplots(figsize= (20,15))
    x= data.drop_duplicates(["Year", "Event", "Sport"])
    ax = sns.heatmap(x.pivot_table(index ='Sport',columns='Year',values = 'Event',aggfunc = "count")
                     .fillna(0)
                     .astype(int),annot = True)
    st.pyplot(fig)

    st.title("Most Successful Athletes")
    sport_list = data['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0, "Overall")
    selected_sport = st.selectbox("Select Sport", sport_list)

    most_successful_df = most_successful(data,selected_sport)
    st.table(most_successful_df)

# Country-wise Analysis
if user_menu == 'Country-wise Analysis':
    st.sidebar.title("Country-wise Analysis")
    country_list = data['region'].dropna().unique().tolist()
    country_list.sort()
    selected_country = st.sidebar.selectbox("Select a Country", country_list)
    country_df= helper.yearwise_medal_tally(data,selected_country)
    st.title(selected_country + " Medal Tally over the Years")
    fig4 = px.line(country_df, x="Year", y="Medal", markers=True)
    st.plotly_chart(fig4)

    country_sport_heatmap = helper.country_sport_heatmap(data,selected_country)
    st.title(selected_country + " Medal Tally per Sports over Years")
    fig , ax = plt.subplots(figsize= (20,15))
    ax= sns.heatmap(country_sport_heatmap.pivot_table(index='Sport', columns='Year', values='Medal', aggfunc='count').fillna(0).astype(int),
        annot=True)
    st.pyplot(fig)

    top_athlete_per_country = helper.top_athlete_per_country(data,selected_country)
    st.title("Top 10 Athletes for " + selected_country )
    st.table(top_athlete_per_country)

# Athlete-wise Analysis

if user_menu == "Athlete-wise Analysis":
    athlete_df = data.drop_duplicates(subset=["Name", 'region'])
    x1 = athlete_df["Age"].dropna()
    x2 = athlete_df[athlete_df["Medal"] == 'Gold']["Age"].dropna()
    x3 = athlete_df[athlete_df["Medal"] == 'Silver']["Age"].dropna()
    x4 = athlete_df[athlete_df["Medal"] == 'Bronze']["Age"].dropna()
    st.title("Distribution of Age wrt Medal")

    fig1=ff.create_distplot([x1, x2, x3, x4], ["Overall Distribution", "Gold", "Silver", "Bronze"], show_hist=False,show_rug=False)
    fig1.update_layout(autosize=False,width=1000,height=600,xaxis_title = "Age of Athletes",yaxis_title = "Density")
    st.plotly_chart(fig1)

    sports_list_top20= data['Sport'].value_counts().reset_index()['Sport'].head(20).to_list()

    x = []
    name = []
    for sport in sports_list_top20:
        temp_df = athlete_df[athlete_df["Sport"] == sport]
        x.append(temp_df[temp_df["Medal"] == 'Gold']['Age'].dropna())
        name.append(sport)
    st.title("Distribution of Age wrt Top Sports(Gold Medalist)")
    fig2 = ff.create_distplot(x, name, show_hist=False, show_rug=False)
    fig2.update_layout(autosize=False, width=1000, height=600,xaxis_title = "Age of Athletes",yaxis_title = "Density")
    st.plotly_chart(fig2)

    st.title("Height vs Weight")
    sports_list=data["Sport"].unique().tolist()
    sports_list.sort()
    sports_list.insert(0,"Overall")

    selected_sport= st.selectbox("Select a Sport",sports_list)
    temp_df= helper.height_vs_weight(data,selected_sport)
    fig , ax = plt.subplots(figsize= (20,15))
    ax= sns.scatterplot(temp_df, x="Weight", y="Height", hue=temp_df["Medal"], style=temp_df["Sex"],s=90)
    st.pyplot(fig)

    male_df = athlete_df[athlete_df["Sex"] == "M"].groupby("Year")["Name"].count().reset_index()
    female_df = athlete_df[athlete_df["Sex"] == "F"].groupby("Year")["Name"].count().reset_index()
    participation = male_df.merge(female_df, on='Year', how='left')
    participation.fillna(0, inplace=True)
    participation= participation.rename(columns={"Name_x": "Male", "Name_y": "Female"}).astype(int)
    st.title("Male vs Female Participation Over the Years")
    fig = px.line(
        participation,
        x="Year",
        y=["Male", "Female"],
        labels={"value": "Number of Athletes", "Year": "Olympic Year", "variable": "Gender"},
        markers=True,

    )
    st.plotly_chart(fig)






