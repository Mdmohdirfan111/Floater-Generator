import streamlit as st
import pandas as pd
# ... [rest of your code with st.input() instead of input()]

st.title("🎯 Floater Generator")
file = st.file_uploader("Upload input file")
month = st.selectbox("Select month", list(calendar.month_name[1:]))
# ... [adapt all input() calls to Streamlit]
