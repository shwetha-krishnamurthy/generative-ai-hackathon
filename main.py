import streamlit as st
from screen_input import show_input_screen
from screen_results import show_results_screen 
import pandas as pd

# NOTE: run using `streamlit run main.py`

# Configure multi-page streamlit
st.set_page_config(layout = "wide")
if "page" not in st.session_state:
    st.session_state.page = 0
if "dataframe" not in st.session_state:
    st.session_state.dataframe = None
if "api_key" not in st.session_state:
    st.session_state.api_key = None
if "show_solution_keys" not in st.session_state:
    st.session_state.show_solution_keys = {}
if "shortlist" not in st.session_state:
    st.session_state.shortlist = pd.DataFrame()

# Get user input
if st.session_state.page == 0:
    show_input_screen()

# Show results
if st.session_state.page == 1:
    show_results_screen()
