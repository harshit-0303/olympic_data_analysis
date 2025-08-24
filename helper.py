import pandas as pd
import numpy as np


def medal_tally(data):
    # Remove duplicates to avoid counting same medals multiple times
    medal_tally = data.drop_duplicates(
        subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Medal', 'Event']
    )

    # Group by NOC and sum medals
    medal_tally = (
        medal_tally.groupby("region")
        .sum()[["Bronze", "Gold", "Silver"]]
        .sort_values("Gold", ascending=False)
        .reset_index()
    )

    # Add Total column
    medal_tally["Total"] = (
        medal_tally["Gold"] + medal_tally["Silver"] + medal_tally["Bronze"]
    )

    # Convert to int
    medal_tally["Gold"] = medal_tally["Gold"].astype(int)
    medal_tally["Silver"] = medal_tally["Silver"].astype(int)
    medal_tally["Bronze"] = medal_tally["Bronze"].astype(int)
    medal_tally["Total"] = medal_tally["Total"].astype(int)

    return medal_tally

def country_year_list(data):
    year = data['Year'].unique().tolist()
    year.sort()
    year.insert(0, "Overall")

    country = np.unique(data['region'].dropna().values).tolist()
    country.sort()
    country.insert(0, "Overall")

    return year, country


def fetch_medal_tally(data, year, country):
    # Remove duplicate medals
    medal_df = data.drop_duplicates(
        subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Medal', 'Event']
    )

    # Filtering logic
    if year == "Overall" and country == "Overall":
        temp_df = medal_df
    elif year != "Overall" and country == "Overall":
        temp_df = medal_df[medal_df["Year"] == int(year)]
    elif year == "Overall" and country != "Overall":
        temp_df = medal_df[medal_df["region"] == country]
    else:
        temp_df = medal_df[(medal_df["region"] == country) & (medal_df["Year"] == int(year))]

    # Grouping logic
    if country == "Overall":
        x = (
            temp_df.groupby("region")
            .sum()[["Gold", "Silver", "Bronze"]]
            .sort_values("Gold", ascending=False)
            .reset_index()
        )
    else:
        x = (
            temp_df.groupby("Year")
            .sum()[["Gold", "Silver", "Bronze"]]
            .sort_values("Year")
            .reset_index()
        )

    # Add total column
    x["Total"] = x["Gold"] + x["Silver"] + x["Bronze"]

    # Convert to int (avoids float medals like 2.0)
    x[["Gold", "Silver", "Bronze", "Total"]] = x[["Gold", "Silver", "Bronze", "Total"]].astype(int)

    return x

def nations_over_time(data):
    nations_over_time = (
        data.drop_duplicates(['Year', 'region'])['Year']
        .value_counts()
        .reset_index()
        .sort_values("Year")
    )
    return nations_over_time

def events_over_time(data):
    event_over_year= (data.drop_duplicates(["Year","Event"])['Year']
                      .value_counts()
                      .reset_index()
                      .sort_values("Year"))
    return event_over_year

def athlete_over_time(data):
    event_over_year= (data.drop_duplicates(["Year","Name"])['Year']
                      .value_counts()
                      .reset_index()
                      .sort_values("Year"))
    return event_over_year

def most_successful(data,sport):
    temp_df = data.dropna(subset = ["Medal"])
    if sport != "Overall" :
        temp_df = temp_df[temp_df["Sport"] == sport]
    x= temp_df["Name"].value_counts().reset_index().merge(data[["Name","region","Sport"]], on= "Name").drop_duplicates().head(15)
    x.rename(columns={"count" : "Total_medals"}, inplace = True)
    return x

def yearwise_medal_tally(data, country):
    temp_df = data.dropna(subset=["Medal"])
    temp_df = temp_df.drop_duplicates(["Event", "Year", "City", "Sport", "Event", "Medal", "region"])
    temp_df = temp_df[temp_df["region"] == country]



    final_df = temp_df.groupby("Year")["Medal"].count().reset_index()
    return final_df

def country_sport_heatmap(data,country):
    temp_df = data.dropna(subset=["Medal"])
    temp_df = temp_df.drop_duplicates(["Event", "Year", "City", "Sport", "Event", "Medal", "region"])
    new_df= temp_df[temp_df['region'] == country]

    return new_df

def top_athlete_per_country(data,country):
    temp_df = data.dropna(subset=['Medal'])
    temp_df = temp_df[temp_df['region'] == country]
    x = (temp_df['Name'].value_counts().reset_index().rename(columns={'count': 'Medals'}).head(10))
    x = x.merge(data[['Name', 'Sport']], on='Name', how='left')
    x = x.drop_duplicates(subset='Name')

    return x

def height_vs_weight(data,sport):
    athlete_df= data.drop_duplicates(subset=['Name','region'])
    if sport != "Overall" :
        temp_df = athlete_df[athlete_df["Sport"] == sport]
        return temp_df
    else :
        return athlete_df




