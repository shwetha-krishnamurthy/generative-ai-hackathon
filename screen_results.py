import streamlit as st
from problem_solution_eval import get_problem_solution_eval_result
import backup_chat_completions
import os

###############################################################################
# Helper Functions
###############################################################################

# Changes session state back to input page
def backpage(): st.session_state.page = 0

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

    try: 
        # Get Gen AI Responses
        eval_problem, eval_solution, eval_summary = get_problem_solution_eval_result(
            "./problem.txt", "./solution.txt") # TODO: should take API key as a param
        
    except Exception as e:
        # print(e)
        # raise

        # Backup Chat completion GenAI
        eval_problem, eval_solution, eval_summary = backup_chat_completions.get_problem_solution_eval_result(
            st.session_state.dataframe[unique_query_name]['problem'],
            st.session_state.dataframe[unique_query_name]['solution'])

    st.session_state.dataframe[unique_query_name]["eval_problem"]  = eval_problem
    st.session_state.dataframe[unique_query_name]["eval_solution"] = eval_solution
    st.session_state.dataframe[unique_query_name]["eval_summary"]  = eval_summary

    # Delete temp file
    os.remove("problem.txt")
    os.remove("solution.txt")

# Prints HTML code for the results screen 
def update_screen(screen, results):
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
                    <h4>Solution Evaluation</h4>""" + "".join([
                    "<h6>" + h_t[0].replace('\n', ' ') + "</h6>" + 
                    "<p><i>" + h_t[1].replace('\n', ' ') + "</i></p>" 
                    for h_t in results["eval_solution"]]
                    if len(results["eval_solution"]) > 0
                    else ["<p><i>Loading...</i></p>"]) + """
                </div>
                <div class="box">
                    <h4>Summary</h4>""" + "".join([
                    "<p><i>" + h_t[1].replace('\n', ' ') + "</i></p>" 
                    for h_t in results["eval_summary"]]
                    if len(results["eval_summary"]) > 0
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
        unique_query_name = st.sidebar.radio("Queries", st.session_state.dataframe.keys())
    main_content = st

    # Main Screen
    main_content.title("VC Evaluator (by sustAInable): " + unique_query_name)
    update_responses(unique_query_name)
    update_screen(main_content, st.session_state.dataframe[unique_query_name])

    # Disclaimer
    main_content.markdown("*Disclaimer: Generative AI can make mistakes. Consider checking important information.*")
    main_content.markdown("*Created by Team sustAInable (Shwetha Krishnamurthy, Jacob Ryan, and Mason Yu) for the 2024 D^3 EarthAI Hackathon.*")

    # Other action buttons
    st.button('Upload Different CSV or Problem-Solution Pair', on_click = backpage)

