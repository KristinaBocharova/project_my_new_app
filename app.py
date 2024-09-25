import pandas as pd
import streamlit as st
import plotly.express as px

# Load data 
data = pd.read_csv('vehicles_us.csv')

# Data preprocessing
data['price'] = pd.to_numeric(data['price'], errors='coerce')
data['model_year'] = pd.to_numeric(data['model_year'], errors='coerce')
data['odometer'] = pd.to_numeric(data['odometer'], errors='coerce')

# Fill missing values
def fill_model_year_with_median(group):
    median = group.median()  
    return group.fillna(median)  

data['model_year'] = data.groupby('model')['model_year'].transform(fill_model_year_with_median)

data['odometer'] = data['odometer'].fillna(data.groupby('model_year')['odometer'].transform('mean'))
data['odometer'] = data['odometer'].fillna(data['odometer'].mean())

# Streamlit interface
st.header('Choose your car!')

price_range=st.slider("What is your price range", value=(1, 375000))

actual_range=list(range(price_range[0], price_range[1]+1))

high_year = st.checkbox('Only cars from 2019 or newer')

# Filter data 
if high_year:
    filtered_data = data[(data['price'].isin(actual_range)) & (data['model_year'] >= 2019)]
else:
    filtered_data=data[data.price.isin(actual_range)]


# Scatter plot with a split by price and model_year
st.write('Here are your options with a split by price and model year:')
fig = px.scatter(filtered_data, x="price", y="model_year", title="Price vs Model Year")
st.plotly_chart(fig)

# Conclusion from the scatter plot with a split by price and model_year
st.write('Conclusion about the depandancy of price from model_year:')
st.write('1) Most of the cars on this scatter plot are priced below $80,000')

# Histogram showing distribution of cars by odometer 
st.write('Distribution of odometer of filtered cars:')
fig2 = px.histogram(filtered_data, x='odometer', title="Odometer Distribution")
st.plotly_chart(fig2)

# Conclusion from the histogram with a distribution by odometer
st.write('Conclusion about the distribution of car by odometer:')
st.write('1) Most of the cars have odometer ranging from 10,000 to 30,000 miles.')
st.write('2) The highest bar corresponds to a mileage of about 20,000 miles, which means that this is the most common mileage among the sampled vehicles.')
st.write('3) There are a few cars with over 50,000 miles, but they represent a small percentage of the total.')




    
    