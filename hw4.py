import altair as alt
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import plotly.express as px 
import seaborn as sns
import streamlit as st

st.title("Is there life after graduate school?")
st.markdown("""This dashboard visualizes data about doctorate recipients including: 
demographic information, field of study, and postgraduation plans. 
Data was collected the National Center for Science and Engineering Statistics (NCSES) and 
datasets can be found here: https://ncses.nsf.gov/pubs/nsf19301/data.""")


df = pd.read_excel("https://ncses.nsf.gov/pubs/nsf19301/assets/data/tables/sed17-sr-tab021.xlsx", header=3)
dm = pd.read_excel("https://ncses.nsf.gov/pubs/nsf19301/assets/data/tables/sed17-sr-tab020.xlsx", header=3)
df = df.rename(columns={'Ethnicity, race, and citizenship status':'Race'})
dm = dm.rename(columns={'Ethnicity, race, and citizenship status':'Race'})

df_female = (
    df.
    drop(df[df['Race'].str.contains('citizen')].index.tolist()).
    drop(df[df['Race'].str.contains('visa')].index.tolist()).
    drop(df[df['Race'].str.contains('Hispanic')].index.tolist()).
    drop(df[df['Race'].str.contains('Ethnicity')].index.tolist()).
    reset_index().
    drop(columns = ['index'])
)
df_female["Gender"] = "Female"
df_plot = df_female[df_female["Race"] == "All doctorate recipients"]
df2 = (df_plot.drop(['Gender'], axis=1))
df_long = pd.melt(df2,id_vars=['Race'],var_name='Year', value_name='phds')
df_long['Gender'] = ['Female']*10

df_male = (
    dm.
    drop(dm[dm['Race'].str.contains('citizen')].index.tolist()).
    drop(dm[dm['Race'].str.contains('visa')].index.tolist()).
    drop(dm[dm['Race'].str.contains('Hispanic')].index.tolist()).
    drop(dm[dm['Race'].str.contains('Ethnicity')].index.tolist()).
    reset_index().
    drop(columns = ['index'])
)
df_male["Gender"] = "Male"
df_plot2 = df_male[df_male["Race"] == "All doctorate recipients"]
df3 = (df_plot2.drop(['Gender'], axis=1))
df_long2 = pd.melt(df3,id_vars=['Race'],var_name='Year', value_name='phds')
df_long2['Gender'] = ['Male']*10

df_combine = pd.concat([df_female, df_male], ignore_index=True)
df_combine_plot = pd.concat([df_long, df_long2], ignore_index=True)

@st.cache
def load_data(year):
    """
    stores data for each for faster retrieval 
    """
    year_df = df_combine[["Gender", "Race", year]]
    return year_df

# Creating widget for selecting data by year and gender (separately)
st.sidebar.header("User Input")
selected_year = st.sidebar.selectbox('Year', list(reversed(range(2008,2017))))
phds = load_data(selected_year)
unique_gender = phds.Gender.unique()
select_gender = st.sidebar.multiselect('Gender', unique_gender, unique_gender)
df_selected = phds[(phds.Gender.isin(select_gender))]

# calling data table 
st.subheader("Doctorate recipients by gender & race from 2008-2016")
st.write("Select a year on the sidebar to display data for that year and select to view data by gender")
st.dataframe(df_selected)

# plotting figure
fig = px.line(df_combine_plot, 
                x='Year', y='phds', color='Gender', 
                labels = {
                    "phds": "Number of PhDs"
                })
fig.update_traces(mode='markers+lines')
st.subheader("Number of doctorate recipients by gender over time")
st.write(fig)
