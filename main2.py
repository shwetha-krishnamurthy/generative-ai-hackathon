import streamlit as st
from screen_results import show_results_screen 
from keywords import process_dataframe

# NOTE: run using `streamlit run main.py`
# Changes session state to results page
def nextpage(): 
    st.session_state.page = 1
    print("******** increment page")
    if st.session_state.content_source == "CSV upload" and st.session_state.uploaded_file is not None:
        try:
            # Try reading with default UTF-8 encoding
            st.session_state.dataframe = pd.read_csv(st.session_state.uploaded_file)
            print("******** xxxDF:")
            print(st.session_state.dataframe)
            st.write("CSV file successfully loaded.")
        except UnicodeDecodeError:
            st.session_state.dataframe = pd.read_csv(st.session_state.uploaded_file, encoding='ISO-8859-1')
            print("******** xxxDF:")
            print(st.session_state.dataframe)
            st.write("CSV file successfully loaded.")
        except Exception as e:
            st.write("An error occurred while reading the CSV file.")
            st.write(e)

    elif st.session_state.content_source == "Manual entry":
        st.session_state.dataframe = pd.DataFrame({
            'Problem': [problem_statement],
            'Solution': [solution_statement]
        })

# Configure multi-page streamlit
st.set_page_config(layout = "wide")
if "page" not in st.session_state:
    st.session_state.page      = 0
if "dataframe" not in st.session_state:
    st.session_state.dataframe = None
if "api_key" not in st.session_state:
    st.session_state.api_key   = None
if "uploaded_file" not in st.session_state:
    st.session_state.uploaded_file   = None
if "dataframe" not in st.session_state:
    st.session_state.dataframe   = None

# Get user input
if st.session_state.page == 0:
    # Title
    st.title("Input to VC Evaluator (by sustAInable)")
    st.write("Upload your CSV file of your problem-solution pairs. Alternatively, analyze one idea")
    
    st.session_state.content_source = st.radio("Choose input method:", ["CSV upload", "Manual entry"])

    with st.form(key='user_input_form'):
        # CSV Upload
        if st.session_state.content_source == "CSV upload":
            st.session_state.uploaded_file = st.file_uploader("Upload CSV File", type=["csv"])
            
        # Manual Entry
        else: 
            problem_statement = st.text_input("Enter the Problem")
            solution_statement = st.text_input("Enter the Solution")

        # API Key
        # if "api_key" not in st.session_state:
        st.session_state.api_key = st.text_input("Enter OpenAI API Key:", type='password')

        # Submission button
        submitted = st.form_submit_button('Submit', on_click = nextpage)

# Show results
if st.session_state.page == 1:
    print("******** API:")
    print(st.session_state.api_key)
    print("******** DF:")
    print(st.session_state.dataframe)
    data = process_dataframe(st.session_state.dataframe)
    # del st.session_state.dataframe
    show_results_screen(data)