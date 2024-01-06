import streamlit as st
import pandas as pd

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
    st.title("Input to VC Evaluator (by sustAInable)")
    st.write("Upload your CSV file of your problem-solution pairs. Alternatively, analyze one idea")
    
    content_source = st.radio("Choose input method:", ["CSV upload", "Manual entry"])

    with st.form(key='user_input_form'):
        # CSV Upload
        if content_source == "CSV upload":
            uploaded_file = st.file_uploader("Upload CSV File", type=["csv"])
            
        # Manual Entry
        else: 
            problem_statement = st.text_input("Enter the Problem")
            solution_statement = st.text_input("Enter the Solution")

        # API Key
        if "api_key" not in st.session_state:
            st.session_state.api_key = st.text_input("Enter OpenAI API Key:", type='password')

        # Submission button
        submitted = st.form_submit_button('Submit', on_click = nextpage)
        
    # Store inputs
    if submitted:
        if content_source == "CSV upload" and uploaded_file is not None:
            try:
                # Try reading with default UTF-8 encoding
                st.session_state.dataframe = pd.read_csv(uploaded_file)
                st.write("CSV file successfully loaded.")
            except UnicodeDecodeError:
                st.session_state.dataframe = pd.read_csv(uploaded_file, encoding='ISO-8859-1')
                st.write("CSV file successfully loaded.")
            except Exception as e:
                st.write("An error occurred while reading the CSV file.")
                st.write(e)

        elif content_source == "Manual entry":
            st.session_state.dataframe = pd.DataFrame({
                'Problem': [problem_statement],
                'Solution': [solution_statement]
            })

if __name__ == "__main__":
    input_screen()
