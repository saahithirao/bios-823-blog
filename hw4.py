import altair as alt
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go 
import seaborn as sns
import streamlit as st

# create dashboard title and description
st.title("Visualizing Data of Doctorate Recipients")
st.markdown("""This dashboard visualizes data about doctorate recipients including: 
demographic information and field of study. 
Data was collected by the National Center for Science and Engineering Statistics (NCSES) and 
can be found here: https://ncses.nsf.gov/pubs/nsf19301/data.""")

# read data
df = pd.read_excel("https://ncses.nsf.gov/pubs/nsf19301/assets/data/tables/sed17-sr-tab021.xlsx", header=3)
dm = pd.read_excel("https://ncses.nsf.gov/pubs/nsf19301/assets/data/tables/sed17-sr-tab020.xlsx", header=3)
df = df.rename(columns={'Ethnicity, race, and citizenship status':'Race_Ethnicity'})
dm = dm.rename(columns={'Ethnicity, race, and citizenship status':'Race_Ethnicity'})

# transforming data of females to summarize and plot
df_female = (
    df.
    drop(df[df['Race_Ethnicity'].str.contains('citizen')].index.tolist()).
    drop(df[df['Race_Ethnicity'].str.contains('visa')].index.tolist()).
    drop(df[df['Race_Ethnicity'].str.contains('Not')].index.tolist()).
    reset_index().
    drop(columns = ['index'])
    )
df_female["Gender"] = "Female"
df_plot = df_female[df_female["Race_Ethnicity"] == "All doctorate recipients"]
df2 = (df_plot.drop(['Gender'], axis=1))
df_long = pd.melt(df2,id_vars=["Race_Ethnicity"],var_name='Year', value_name='phds')
df_long['Gender'] = ['Female']*10

# transforming data of males to summarize and plot
df_male = (
    dm.
    drop(df[df['Race_Ethnicity'].str.contains('citizen')].index.tolist()).
    drop(df[df['Race_Ethnicity'].str.contains('visa')].index.tolist()).
    drop(df[df['Race_Ethnicity'].str.contains('Not')].index.tolist()).
    reset_index().
    drop(columns = ['index'])
    )
df_male["Gender"] = "Male"
df_plot2 = df_male[df_male["Race_Ethnicity"] == "All doctorate recipients"]
df3 = (df_plot2.drop(['Gender'], axis=1))
df_long2 = pd.melt(df3,id_vars=['Race_Ethnicity'],var_name='Year', value_name='phds')
df_long2['Gender'] = ['Male']*10

# Combine data for table 
df_combine = pd.concat([df_female, df_male], ignore_index=True)
# Combine data for plot
df_combine_plot = pd.concat([df_long, df_long2], ignore_index=True)

@st.cache
def load_data(year):
    """
    stores data for each for faster retrieval 
    """
    year_df = df_combine[["Gender", "Race_Ethnicity", year]]
    return year_df

# Creating widget for selecting data by year, gender, and race (separately)
st.sidebar.header("User Input")
selected_year = st.sidebar.selectbox('Year', list(reversed(range(2008,2018))))
phds = load_data(selected_year)

unique_gender = phds.Gender.unique()
select_gender = st.sidebar.multiselect('Gender', unique_gender, unique_gender)

unique_race = phds.Race_Ethnicity.unique()
select_race = st.sidebar.multiselect('Race_Ethnicity', unique_race, unique_race)
df_selected = phds[(phds.Gender.isin(select_gender)) & (phds.Race_Ethnicity.isin(select_race))]

# calling data table 
st.subheader("Doctorate recipients by gender & race from 2008-2016")
st.write("On the sidebar select a year, gender, or race (including all) to display data by year, gender, and/or race")
st.table(df_selected)

# plotting figure
fig = px.line(df_combine_plot, 
                x='Year', y='phds', color='Gender', 
                labels = {
                    "phds": "Number of PhDs"
                })
fig.update_traces(mode='markers+lines')
st.subheader("Number of doctorate recipients by gender over time")
st.write("Hover over points to view data for that year")
st.write(fig)

# saggregate doctorate recipients across years
st.subheader("Summary of doctorate recipients across years by gender")
st.write("This table was created from data aggregated from 2008 to 2017 and follows from the figure above")
summary = pd.DataFrame({'Gender': ['Female','Male'],
            'Min': [df_long['phds'].min(), df_long2['phds'].min()],
            'Mean' : [df_long['phds'].mean(), df_long2['phds'].mean()], 
            'Median': [df_long['phds'].median(), df_long2['phds'].median()],
            'Max': [df_long['phds'].max(), df_long2['phds'].max()]})
st.dataframe(summary)

# visualize data by field of study
dat = pd.read_excel("https://ncses.nsf.gov/pubs/nsf19301/assets/data/tables/sed17-sr-tab054.xlsx", header=3)

# create data frame of all doctorate recipients by field of study
dat_all = dat.iloc[[0]]
dat_T = dat_all.T
dat_T = dat_T.rename(columns=dat_T.iloc[0]).reset_index()
dat_T = dat_T.iloc[1:]

# bar plot by field of study
fig2 = px.bar(dat_T, x='index', y='All doctorate recipients (number)c',  
             labels={'All doctorate recipients (number)c':'All Doctorates', 'index':'Field of Study'})
st.subheader("All doctorate recipients by field of study in 2017")
st.write("Hover over plot to view specific numbers")
st.write(fig2)

# extract gender information
to_plot = dat[dat['Characteristic'].str.contains('ale')]

# swap columns and rows
plot = to_plot.T
plot2 = (
            plot.
            rename(columns=plot.iloc[0]).
            drop(plot.index[0]).
            reset_index().
            drop(columns=['Female doctorate recipients (number)', 'Male doctorate recipients (number)'])
)

# create stacked bar plot of doctorates by field of study and gender
fig3 = go.Figure(
    data=[
        go.Bar(
            name="Male",
            x=plot2["index"],
            y=plot2["Male"],
            offsetgroup=1,
        ),
        go.Bar(
            name="Female",
            x=plot2["index"],
            y=plot2["Female"],
            offsetgroup=1,
            base=plot2["Male"],
            hovertext= [f'Count: {val}' for val in plot2["Female"]]
        )
    ],
    layout=go.Layout(yaxis_title="Percent")
)
st.subheader("Doctorate recipients by field of study and gender in 2017")
st.write("Hover over plot to view percentages by gender of a specific field of study")
st.write(fig3)
