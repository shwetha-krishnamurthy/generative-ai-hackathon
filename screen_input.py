import os
import streamlit as st
import pandas as pd
from io import StringIO
from keywords import process_dataframe

###############################################################################
# Helper Function
###############################################################################

# Changes session state to results page
def nextpage(): st.session_state.page = 1

###############################################################################
# Print Input Screen
###############################################################################

# Asks user for a problem-solution pair or a CSV of pairs. Also ask for an API 
# key unless one was previously provided.
def show_input_screen():
    # Title
    st.title("SustAInable VC Synergy")
    st.write("Upload your CSV file of your problem-solution pairs. Alternatively, analyze one idea")
    
    content_source = st.radio("Choose input method:", ["CSV upload", "Manual entry"])

    with st.form(key = 'user_input_form', clear_on_submit = False):
        # CSV Upload
        if content_source == "CSV upload":
            uploaded_file = st.file_uploader("Upload CSV File", type=["csv"])
            
        # Manual Entry
        else: 
            problem_statement = st.text_input("Enter the Problem")
            solution_statement = st.text_input("Enter the Solution")

        # API Key
        st.session_state.api_key = st.text_input("Enter OpenAI API Key (required):", type='password')
        st.session_state.tavily_key = st.text_input("Enter Tavily API Key (optional; if you would like to scrape the web using Open AI Assistants):", type='password')

        os.environ['OPENAI_API_KEY'] = st.session_state.api_key
        os.environ["TAVILY_API_KEY"] = st.session_state.tavily_key

        # Submission button
        submitted = st.form_submit_button('Upload')
        
    # Store inputs
    if submitted and (st.session_state.api_key is None or st.session_state.api_key == ""):
        st.error("Please include an OpenAI API Key.")

    elif submitted:
        if content_source == "CSV upload" and uploaded_file is not None:
            try:
                stringio = StringIO(uploaded_file.getvalue().decode("utf-8", errors="replace"))
                string_data = stringio.read()
                st.session_state.dataframe = process_dataframe(pd.read_csv(StringIO(string_data)))
                
                st.warning('CSV file successfully loaded! Please click "Process Results", which take a few moments to process. Please do not leave or click elsewhere on this screen while it is loading.')

                # Move to next page
                st.button('Process Results', on_click = nextpage)    
            except Exception as e:
                st.write("An error occurred while reading the CSV file.")
                st.error(e)

        elif content_source == "Manual entry":
            st.session_state.dataframe = process_dataframe(pd.DataFrame({
                'problem': [problem_statement],
                'solution': [solution_statement]}))
            st.success('Input successfully loaded!')
            st.warning('Please click "Process Results", which take a few moments to process. Please do not leave or click elsewhere on this screen while it is loading.')

            # Move to next page
            st.button('Process Results', on_click = nextpage)    

if __name__ == "__main__":
    show_input_screen()
