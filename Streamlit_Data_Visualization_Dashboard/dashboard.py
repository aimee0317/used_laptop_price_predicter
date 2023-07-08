import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.title("Used Laptop Price Analysis")
st.sidebar.title("Used Laptop Price Analysis")
st.sidebar.markdown(
    "This is an interactive dashboard to analyze used laptop price data. 💻")

data_url = ('/Users/amelia/Desktop/desktop/used_laptop_price_predicter/Streamlit_Data_Visualization_Dashboard/Cleaned_Laptop_data.csv')


# only rerun the function if the code changed or will reuse cached data
@st.cache_data(persist=True)
def load_data():
    data = pd.read_csv(data_url)
    return data


data = load_data()

st.write(data)

st.sidebar.subheader("Show some random laptop")
random_laptop = st.sidebar.radio(
    'Sentiment', ('positive', 'neutral', 'negative'))

st.sidebar.markdown('### Price distribution')
select = st.sidebar.selectbox(
    'Visualization type', ['Histogram', 'Violin Plot'], key='1')

if not st.sidebar.checkbox('Hide', True):
    st.markdown("### Used Laptop Price Distribution")
    if select == 'Histogram':
        fig = px.histogram(data, x="latest_price")
        st.plotly_chart(fig)
    else:
        fig = px.violin(data, y="latest_price")
        st.plotly_chart(fig)
