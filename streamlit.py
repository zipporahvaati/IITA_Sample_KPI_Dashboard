
import streamlit as st
import pandas as pd

st.title("Streamlit Test Dashboard App")

df=pd.read_csv("data/agriculture_dataset.csv")

st.write("Data loaded:")
st.write(df.head())