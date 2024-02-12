import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide",initial_sidebar_state="collapsed")
st.sidebar.title("Filters",anchor=False)
#----------------------------------------------------------------------------------------------------
#CSS

with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>",unsafe_allow_html = True)

#----------------------------------------------------------------------------------------------------

df = pd.read_csv("supermarket_sales.csv", sep=";", decimal=",")
df["Date"] = pd.to_datetime(df["Date"])
df=df.sort_values("Date")
#----------------------------------------------------------------------------------------------------
#Tratamento dos dados

df["Month"] = df["Date"].dt.month
df["Year"] = df["Date"].dt.year
df["Day"] = df["Date"].dt.day

def determinar_mes(valor):
    meses = {
        1:'Jan',
        2:'Fev',
        3:'Mar',
        4:'Apr',
        5:'May',
        6:'Jun',
        7:'Jul',
        8:'Aug',
        9:'Set',
        10:'Out',
        11:'Nov',
        12:'Dez'
    }
    return meses.get(valor)


df["Month"] = df["Month"].apply(determinar_mes)
#----------------------------------------------------------------------------------------------------
#filters

year = st.sidebar.selectbox("Year",df["Year"].unique())
month = st.sidebar.selectbox("Month", df["Month"].unique())
#----------------------------------------------------------------------------------------------------
#dataframe filtered

df_filtered = df.query('Year == @year & Month == @month')
#----------------------------------------------------------------------------------------------------
#Page layout
st.title(f'Sales Analysis {month} - {year}',anchor=False)
col1, col2 = st.columns(2)
col3, col4, col5 = st.columns(3)


#----------------------------------------------------------------------------------------------------
#Graphics

#Daily Sales

fig_date = px.bar(df_filtered.groupby(['Day','City'])[["Total"]].sum().reset_index(),
        x="Day", y="Total", color="City", title="Daily Sales",
        color_discrete_sequence=['#023e8a','#0a9396','#0077b6'])
fig_date.update_scenes(overwrite=False)
fig_date.update_yaxes(showgrid=False)
col1.plotly_chart(fig_date, use_container_width=True)

fig_prod = px.bar(df_filtered, 
        x="Date", y="Product line", 
        color="City", title="Product Line",
        orientation="h",
        color_discrete_sequence=['#16db65','#058c42','#04471c'])
fig_prod.update_xaxes(showgrid=False)

col2.plotly_chart(fig_prod, use_container_width=True)

#----------------------------------------------------------------------------------------------------
city_total = df_filtered.groupby("City")[["Total"]].sum().reset_index()
fig_city = px.pie(city_total, names="City", values="Total",color_discrete_sequence=['#00509d'],
                   title="City Sales")
fig_city.update_yaxes(showgrid=False)
col3.plotly_chart(fig_city, use_container_width=True)
#----------------------------------------------------------------------------------------------------
fig_kinddf = df_filtered.groupby("Payment")[["Total"]].sum().reset_index()
fig_kinddf = fig_kinddf.sort_values(by="Total")
fig_kind = px.bar(fig_kinddf, x="Total", y="Payment",
                   title="Per Payment",orientation="h",color_discrete_sequence=['#0e7c7b'])
fig_kind.update_xaxes(showgrid=False)
col4.plotly_chart(fig_kind, use_container_width=True)


city_total = df_filtered.groupby("City")[["Rating"]].mean().reset_index()
fig_rating = px.bar(df_filtered, y="Rating", x="City",color_discrete_sequence=['#0d47a1'],
                   title="Rating")
fig_rating.update_yaxes(showgrid=False)
col5.plotly_chart(fig_rating, use_container_width=True)
#----------------------------------------------------------------------------------------------------

# border= """
#     <style>
#     [data-testid="stFullScreenFrame"]
#     {
#     background-color: black;
#     border-radius: 15px;
#     }
#     </style>
# """


border2= """
    <style>
    [class="main-svg"]
    {
    border-radius: 15px 15px;
    }
    </style>
"""


border3= """
    <style>
    [data-testid="element-container"]
    {
    background-color: black;
    border-radius: 15px 15px;
    }
    </style>
"""


st.markdown(border2,unsafe_allow_html=True)

# st.markdown(border,unsafe_allow_html=True)

st.markdown(border3,unsafe_allow_html=True)

#----------------------------------------------------------------------------------------------------