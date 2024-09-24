import pandas as pd
import streamlit as st
import plotly.express as px

data=pd.read_csv('vehicles_us.csv')

data['price'] = pd.to_numeric(data['price'], errors='coerce')
data['model_year'] = pd.to_numeric(data['model_year'], errors='coerce')
data['odometer'] = pd.to_numeric(data['odometer'], errors='coerce')

def fill_model_year_with_median(group):
    median = group.median()  
    return group.fillna(median)  

data['model_year'] = data.groupby('model')['model_year'].transform(fill_model_year_with_median)

data['odometer'] = data['odometer'].fillna(data.groupby('model_year')['odometer'].transform('mean'))

st.header('Choose your car!')

price_range=st.slider("What is your price range", value=(1, 375000))

actual_range=list(range(price_range[0], price_range[1]+1))

high_year = st.checkbox('Only cars from 2019 or newer')

if high_year:
    filtered_data = data[(data['price'].isin(actual_range)) & (data['model_year'] >= 2019)]
else:
    filtered_data=data[data.price.isin(actual_range)]


if filtered_data.empty:
    st.write("No cars match your criteria.")
else:
    st.write('Here are your options with a split by price and model year')
    fig = px.scatter(filtered_data, x="price", y="model_year", title="Price vs Model Year")
    st.plotly_chart(fig)

    st.write('Distribution of odometer of filtered cars')
    fig2 = px.histogram(filtered_data, x='odometer', title="Odometer Distribution")
    st.plotly_chart(fig2)

    
    st.write('Here is the list of recommended cars')
    st.dataframe(filtered_data.sample(5))