import pandas as pd
import streamlit as st
import plotly.express as px

data=pd.read_csv('vehicles_us.csv')

st.header('Choose your car!')

price_range=st.slider("What is your price range", value=(1, 375000))

actual_range=list(range(price_range[0], price_range[1]+1))

high_year = st.checkbox('Only cars from 2019 or newer')

if high_year:
    filtered_data=data[data.price.isin(actual_range)]
    filtered_data=filtered_data[data.model_year>=2019]
else:
    filtered_data=data[data.price.isin(actual_range)]

st.write('Here are your options with a split by price and model year')

fig = px.scatter(filtered_data, x="price", y="model_year", title="Price vs Model Year")
st.plotly_chart(fig)

st.write('Distribution of odometer of filtered cars')
fig2 = px.histogram(filtered_data, x='odometer', title="Odometer Distribution")
st.plotly_chart(fig2)

st.write('Here is the list of recommended cars')
st.dataframe(filtered_data.sample(5)) 