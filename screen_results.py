import streamlit as st
from problem_solution_eval import get_problem_solution_eval_result
import backup_chat_completions
import pandas as pd

###############################################################################
# Helper Functions
###############################################################################

# Changes session state back to input page
def backpage(): 
    st.session_state.page       = 0
    st.session_state.api_key    = None
    st.session_state.tavily_key = None

# Adds this idea to a short list of ideas that the VC can export
def add_to_shortlist(unique_query_name):
    # If its already in the output, then don't add it again
    if st.session_state.dataframe[unique_query_name]["shortlist"]:
        st.toast("Already in shortlist!")
        return

    # Otherwise, add it
    results = st.session_state.dataframe[unique_query_name]
    st.session_state.dataframe[unique_query_name]["shortlist"] = True
    
    eval_prob_text = "".join([h_t[0].replace('\n', ' ') + "\n" + 
                            h_t[1].replace('\n', ' ') + "\n"
                            for h_t in results["eval_problem"]])
    eval_soln_text = "".join([h_t[0].replace('\n', ' ') + "\n" + 
                            h_t[1].replace('\n', ' ') + "\n"
                            for h_t in results["eval_solution"]])
    eval_summ_text = "".join([h_t[0].replace('\n', ' ') + "\n" + 
                            h_t[1].replace('\n', ' ') + "\n"
                            for h_t in results["eval_summary"]])
    if unique_query_name in st.session_state.show_solution_keys.keys():
        if not st.session_state.show_solution_keys[unique_query_name]:        
            eval_summ_text = "".join([h_t[1].replace('\n', ' ')
                                    for h_t in results["eval_summary"]])

    new_row = pd.DataFrame({
        "Problem": [results["problem"].replace('\n', ' ')], 
        "Solution": [results["solution"].replace('\n', ' ')], 
        "Problem Evaluation": [eval_prob_text],
        "Solution Evaluation": [eval_soln_text],
        "Summary": [eval_summ_text]})

    st.session_state.shortlist = pd.concat([st.session_state.shortlist, new_row], axis = 0)

@st.cache_data
def convert_df(df):
    return df.to_csv(index = False).encode('utf-8')

# If the Gen AI results have not been calculated yet for a given problem-solution
# pair, then calculate the results.
def update_responses(unique_query_name):
    # First check if we've already calculate these before
    if len(st.session_state.dataframe[unique_query_name]["eval_problem"]) > 0:
        return

    # Create temp problem file
    p = open("problem.txt", "wb")
    p_t = st.session_state.dataframe[unique_query_name]['problem'] + "\n"
    p.write(p_t.encode('utf-8'))
    p.close()

    # Create temp problem file
    ps = open("solution.txt", "wb")
    ps_t = ("Problem: " + st.session_state.dataframe[unique_query_name]['problem'] + "\n\n" +
            "Solution: " + st.session_state.dataframe[unique_query_name]['solution'] + "\n")
    ps.write(ps_t.encode('utf-8'))
    ps.close()

    if (st.session_state.tavily_key is None) or (st.session_state.tavily_key == ""):
        try:
            # Backup Chat completion GenAI
            st.session_state.show_solution_keys[unique_query_name] = True
            eval_problem_dict, eval_solution_dict, eval_summary_dict = backup_chat_completions.get_problem_solution_eval_result(
                st.session_state.dataframe[unique_query_name]['problem'],
                st.session_state.dataframe[unique_query_name]['solution'])

            eval_problem  = [(k, eval_problem_dict[k])  for k in sorted(list(eval_problem_dict.keys() ))]
            eval_solution = [(k, eval_solution_dict[k]) for k in sorted(list(eval_solution_dict.keys()))]
            eval_summary  = [('SWOT Analysis', eval_summary_dict['SWOT Analysis']), 
                            ('Recommendation', eval_summary_dict['Recommendation'])]

            st.session_state.dataframe[unique_query_name]["eval_problem"]  = eval_problem
            st.session_state.dataframe[unique_query_name]["eval_solution"] = eval_solution
            st.session_state.dataframe[unique_query_name]["eval_summary"]  = eval_summary

        except Exception as e:
            st.button('Restart Session with New Data and Key', on_click = backpage)
            if "AuthenticationError" in str(e) or "Incorrect API key provided" in str(e):
                st.error("The provided Open AI key is not valid. Please restart the session with a valid Open AI key.")
            st.error(e)

        except:
                st.warning("Sorry, we're having difficulty connecting to Open AI right now. Please try this query again in a few moments. You can click on any other query in the meantime!")

    else:
        try:
            # Get Gen AI Responses
            st.session_state.show_solution_keys[unique_query_name] = False
            eval_problem, eval_solution, eval_summary = get_problem_solution_eval_result(
                "./problem.txt", "./solution.txt")

            st.session_state.dataframe[unique_query_name]["eval_problem"]  = eval_problem
            st.session_state.dataframe[unique_query_name]["eval_solution"] = eval_solution
            st.session_state.dataframe[unique_query_name]["eval_summary"]  = eval_summary

            st.toast("Calculated using the new Open AI Assistants (experimental)!")

        except Exception as e:
            try:
                # Backup Chat completion GenAI
                st.session_state.show_solution_keys[unique_query_name] = True
                eval_problem_dict, eval_solution_dict, eval_summary_dict = backup_chat_completions.get_problem_solution_eval_result(
                    st.session_state.dataframe[unique_query_name]['problem'],
                    st.session_state.dataframe[unique_query_name]['solution'])

                eval_problem  = [(k, eval_problem_dict[k])  for k in sorted(list(eval_problem_dict.keys() ))]
                eval_solution = [(k, eval_solution_dict[k]) for k in sorted(list(eval_solution_dict.keys()))]
                eval_summary  = [('SWOT Analysis', eval_summary_dict['SWOT Analysis']), 
                                ('Recommendation', eval_summary_dict['Recommendation'])]

                st.session_state.dataframe[unique_query_name]["eval_problem"]  = eval_problem
                st.session_state.dataframe[unique_query_name]["eval_solution"] = eval_solution
                st.session_state.dataframe[unique_query_name]["eval_summary"]  = eval_summary

            except Exception as e:
                st.button('Restart Session with New Data and Keys', on_click = backpage)
                if "AuthenticationError" in str(e) or "Incorrect API key provided" in str(e):
                    st.error("Either the provided Open AI or Tavily key is not valid. Please restart the session with valid Open AI and Tavily keys.")
                st.error(e)

        except:
            st.warning("Sorry, we're having difficulty connecting to Open AI right now. Please try this query again in a few moments. You can click on any other query in the meantime!")

# Prints HTML code for the results screen 
def update_screen(screen, results, show_keys):
    html_code = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            .main-container {
                display: flex;
                flex-direction: column;
                align-items: stretch;
                width: 100%;
            }

            .box {
                flex: 1;
                background-color: #f1f2f6;
                padding: 10px;
                margin-right: 10px;
            }

            .container {
                display: flex;
                justify-content: space-between;
                margin-bottom: 10px;
            }
        </style>
        <title>Gray Boxes</title>
    </head>
    <body>
        <div class="main-container">
            <div class="container">
                <div class="box">
                    <p><b>Problem:</b> """ + results["problem"].replace('\n', ' ') + """</p>
                    <p><b>Solution:</b> """ + results["solution"].replace('\n', ' ') + """</p>
                </div>
            </div>
            <div class="container">
                <div class="box">
                    <h4>Problem Evaluation</h4>""" + "".join([
                    "<h6>" + h_t[0].replace('\n', ' ') + "</h6>" + 
                    "<p><i>" + h_t[1].replace('\n', ' ') + "</i></p>" 
                    for h_t in results["eval_problem"]]
                    if len(results["eval_problem"]) > 0
                    else ["<p><i>Loading...</i></p>"]) + """
                </div>
                <div class="box">
                    <h4>Summary</h4>""" + "".join([
                    "<h6>" + h_t[0].replace('\n', ' ') + "</h6>" + 
                    "<p><i>" + h_t[1].replace('\n', ' ') + "</i></p>" 
                    if show_keys
                    else "<p><i>" + h_t[1].replace('\n', ' ') + "</i></p>"
                    for h_t in results["eval_summary"]]
                    if len(results["eval_summary"]) > 0
                    else ["<p><i>Loading...</i></p>"]) + """
                </div>
                <div class="box">
                    <h4>Solution Evaluation</h4>""" + "".join([
                    "<h6>" + h_t[0].replace('\n', ' ') + "</h6>" + 
                    "<p><i>" + h_t[1].replace('\n', ' ') + "</i></p>" 
                    for h_t in results["eval_solution"]]
                    if len(results["eval_solution"]) > 0
                    else ["<p><i>Loading...</i></p>"]) + """
                </div>
            </div>
        </div>
    </body>
    </html>
    """

    screen.markdown(html_code, unsafe_allow_html=True)

###############################################################################
# Print Screen with Results
###############################################################################

# Prints the results on the screen for the provided data. Allows the users to 
# return to the input page to input different data.
def show_results_screen():
    # Side Bar (only appears if run with multiple queries)
    unique_query_name = list(st.session_state.dataframe.keys())[0]
    if (len(st.session_state.dataframe.keys()) > 1):
        unique_query_name = st.sidebar.radio("Idea Label", st.session_state.dataframe.keys())
    main_content = st

    # Title
    main_content.title("SustAInable VC Synergy")
    with st.spinner('Loading ...'):
        update_responses(unique_query_name)

    # Unless there was an error updating the responses...
    if len(st.session_state.dataframe[unique_query_name]["eval_problem"]) > 0:

        # Action buttons
        col1, col2, col3 = main_content.columns(3)
        with col1:
            st.button('Restart Session with New Data', on_click = backpage)
        with col2:
            if st.button('Add to Shortlist'):
                add_to_shortlist(unique_query_name)
        with col3:
            csv = convert_df(st.session_state.shortlist)
            st.download_button('Download Shortlist', data = csv, file_name = "Shortlist.csv",
                            mime = 'text/csv')

        # Main Screen
        update_screen(main_content, st.session_state.dataframe[unique_query_name],
                    st.session_state.show_solution_keys[unique_query_name])

    # Disclaimer
    main_content.markdown("*Disclaimer: Generative AI can make mistakes. Consider checking important information.*")
    main_content.markdown("*Created by Team sustAInable (Shwetha Krishnamurthy, Jacob Ryan, and Mason Yu) for the 2024 D^3 EarthAI Hackathon.*")

