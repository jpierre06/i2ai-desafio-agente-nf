import streamlit as st
from core.data_loader import load_dataframes_from_folders

data = load_dataframes_from_folders()
items = data["items"]

st.dataframe(items)