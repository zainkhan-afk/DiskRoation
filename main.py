import requests
import pandas as pd
import streamlit as st

st.title("TITLE")

text = st.text_input(label="Enter your question:")

if text:
    st.write("TEST TEST TEST")