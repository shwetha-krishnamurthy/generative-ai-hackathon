import streamlit as st
import pandas as pd

def nextpage(): st.session_state.page = 1

def show_input_screen():
    st.title("Input to VC Evaluator (by sustAInable)")
    st.write("Upload your CSV file of your problem-solution pairs. Alternatively, analyze one idea")
    
    content_source = st.radio("Choose input method:", ["CSV upload", "Manual entry"])

    with st.form(key='user_input_form'):
        if content_source == "CSV upload":
            uploaded_file = st.file_uploader("Upload CSV File", type=["csv"])
            
        else: # Manual Entry
            problem_statement = st.text_input("Enter the Problem")
            solution_statement = st.text_input("Enter the Solution")

        if "api_key" not in st.session_state:
            st.session_state.api_key = st.text_input("Enter OpenAI API Key:", type='password')
            
        submitted = st.form_submit_button('Submit', on_click = nextpage)
        
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