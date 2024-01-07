import streamlit as st
from problem_solution_eval import get_problem_solution_eval_result

###############################################################################
# Helper Functions
###############################################################################

# Changes session state back to input page
def backpage(): st.session_state.page = 0

# If the Gen AI results have not been calculated yet for a given problem-solution
# pair, then calculate the results.
def update_responses(unique_query_name):
    # First check if we've already calculate these before
    # if not st.session_state.dataframe[unique_query_name]["eval_problem"]:
    #     return # TODO: fix

    # Create temp problem file
    p = open("problem.txt", "w")
    p.write(st.session_state.dataframe[unique_query_name]['problem'])
    p.close()

    # Create temp problem file
    ps = open("solution.txt", "w")
    ps.write("Problem: " + st.session_state.dataframe[unique_query_name]['problem'] + "\n\n")
    ps.write("Solution: " + st.session_state.dataframe[unique_query_name]['solution'])
    ps.close()

    # Get Gen AI Responses
    # eval_problem, eval_solution, eval_summary = get_problem_solution_eval_result(
    #     "problem.txt", "solution.txt")

    # TODO: delete these temp files later

    # edits this: st.session_state.dataframe 
    # TODO: this needs to be written (find the history row in data, see if it has gen AI answers yet, and if it does not, then create them)

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
                    <p><b>Problem:</b> """ + results["problem"] + """</p>
                    <p><b>Solution:</b> """ + results["solution"] + """</p>
                </div>
            </div>
            <div class="container">
                <div class="box">
                    <h4>Problem Evaluation</h4>""" + "".join([
                    "<h6>" + h_t[0] + "</h6>" + "<p><i>" + h_t[1] + "</i></p>" 
                    for h_t in results["eval_problem"]]
                    if len(results["eval_problem"]) > 0
                    else ["<p><i>Loading...</i></p>"]) + """
                </div>
                <div class="box">
                    <h4>Solution Evaluation</h4>""" + "".join([
                    "<h6>" + h_t[0] + "</h6>" + "<p><i>" + h_t[1] + "</i></p>" 
                    for h_t in results["eval_solution"]]
                    if len(results["eval_solution"]) > 0
                    else ["<p><i>Loading...</i></p>"]) + """
                </div>
                <div class="box">
                    <h4>Summary</h4>""" + "".join([
                    "<h6>" + h_t[0] + "</h6>" + "<p><i>" + h_t[1] + "</i></p>" 
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
    # TODO: still need to get the more information/chat/decision buttons working
            # <div class="container">
            #     <div class="box">
            #         <center>
            #             <p>Chat [[TODO: make button]]</p>
            #         </center>
            #     </div>
            #     <div class="box">
            #         <center>
            #             <p>Decision [[TODO: make button]]</p>
            #         </center>
            #     </div>
            # </div>

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

    # Disclaimer (TODO: should customize disclaimer)
    main_content.markdown("*Disclaimer: Generative AI can make mistakes. Consider checking important information.*")
    main_content.markdown("*Created by Team sustAInable (Shwetha Krishnamurthy, Jacob Ryan, and Mason Yu) for the 2024 D^3 EarthAI Hackathon.*")

    # Other action buttons
    st.button('Upload Different CSV or Problem-Solution Pair', on_click = backpage) # TODO: make sure that 
    # TODO: consider adding an "export" buttom

