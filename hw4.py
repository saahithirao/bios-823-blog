import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import streamlit as st
import altair as alt

st.title("Is there life after graduate school?")
st.markdown(""""This app performs visuzliazation of data from 
the survey of Earned Doctorates""")

st.sidebar.header("User Input")
selected_year = st.sidebar.selectbox('Year', list(reversed(range(2008,2017))))

@st.cache
def load_data(year):
    df = pd.read_excel("https://ncses.nsf.gov/pubs/nsf19301/assets/data/tables/sed17-sr-tab021.xlsx", header=3)
    dm = pd.read_excel("https://ncses.nsf.gov/pubs/nsf19301/assets/data/tables/sed17-sr-tab020.xlsx", header=3)
    df = df.rename(columns={'Ethnicity, race, and citizenship status':'Race'})
    dm = df.rename(columns={'Ethnicity, race, and citizenship status':'Race'})
    
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

    df_combine = pd.concat([df_female, df_male], ignore_index=True)

    year_df = df_combine[["Gender", "Race", year]]
    return year_df

phds = load_data(selected_year)

unique_gender = phds.Gender.unique()
select_gender = st.sidebar.multiselect('Gender', unique_gender, unique_gender)
df_selected = phds[(phds.Gender.isin(select_gender))]

st.dataframe(df_selected)


# def main():
#     page = st.sidebar.selectbox("Choose a page", ["Homepage", "Exploration"])
#     if page == "Homepage":
#         st.header("This is your data explorer.")
#         st.write("Please select a page on the left.")
#         st.write(df)
#     elif page == "Exploration":
#         st.title("Data Exploration")
#         x_axis = st.selectbox("Choose a variable for the x-axis", df.columns, index=3)
#         y_axis = st.selectbox("Choose a variable for the y-axis", df.columns, index=4)
#         visualize_data(df, x_axis, y_axis)

# @st.cache
# def load_data():
#     df = data.cars()
#     return df

# def visualize_data(df, x_axis, y_axis):
#     graph = alt.Chart(df).mark_circle(size=60).encode(
#         x=x_axis,
#         y=y_axis,
#         color='Origin',
#         tooltip=['Name', 'Origin', 'Horsepower', 'Miles_per_Gallon']
#     ).interactive()

#     st.write(graph)

# if __name__ == "__main__":
#     main()



# map_data = pd.DataFrame(
#     np.random.randn(1000, 2) / [50, 50] + [37.76, -122.4],
#     columns=['lat', 'lon'])

# st.map(map_data)