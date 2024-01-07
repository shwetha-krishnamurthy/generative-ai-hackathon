import os
import json
from query import run_open_ai

os.environ['OPENAI_API_KEY'] = "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"


problem_questions = ["Question 1: Does the problem being addressed has any impact on the climate?",
              "Question 2: What is the scale of the problem? (people, volume, money, etc)",
              "Question 3: Who faces this problem predominantly?",
              "Question 4: Who else is solving this problem?",
              "Question 5: Has this problem been solved elsewhere?"]

solution_questions = ["Question 1: Does the solution address the problem directly? Answer yes or no",
              "Question 2: How feasible is the solution?",
              "Question 3: How unique is this solution? Use web search to support your claims",
              "Question 4: What are the risks in implementing this solution?",
              "Question 5: What are the potential challenges in implementing this solution?",
              "Question 6: What additional data does this solution need to help your evaluation further?"]

# TODO be able to read the md file. otherwise, hardcode the VC knowledge into prompt
# with open("generative-ai-hackathon/CircularEconomyResearch.md", "r", encoding="utf-8") as file:
#     circular_economy_knowledge = file.read()


def problem_eval(problem_text):
    model = "gpt-4"
    # TODO add the circular economy knowledge to system prompt correctly on Streamlit
    system = "You are an unbiased expert on Circular Economy, helping a VC analyst sift through ideas with a discerning eye. Adopt a skeptical mindset when analyzing the idea. Here's your knowledge: \n\n" # + circular_economy_knowledge
    user = f"""Here are a list of questions you must answer about the below problem statement. Please answer each in 3 sentences in JSON format with the question label as the key, with the evaluation as the value.
              Questions:
              {problem_questions}

              Problem statement: \n\n {problem_text}"""
    max_tokens = 2000
    temp = 1
    response = run_open_ai(model, system, user, max_tokens, 1, None, temp)
    print(response)
    return response

def solution_eval(problem_text, solution_text):
    model = "gpt-4"
    system = "You are an unbiased expert on Circular Economy, helping a VC analyst sift through ideas with a discerning eye. Adopt a skeptical mindset when analyzing the idea. Here's your knowledge: \n\n" # + circular_economy_knowledge
    user = f"""Here are a list of questions you must answer about the below problem - solution pair. Please answer each in 3 sentences in JSON format with the question label as the key, with the evaluation as the value.
              Questions:
              {solution_questions}

              Problem statement: \n\n {problem_text} \n\n Solution statement: \n\n" + {solution_text}"""
    max_tokens = 2500
    temp = 1
    response = run_open_ai(model, system, user, max_tokens, 1, None, temp)
    print(response)
    return response

def summary_eval(prob_eval_text, sol_eval_text):
    model = "gpt-3.5-turbo"
    system = f"""You are an unbiased expert on Circular Economy, helping a VC analyst sift through ideas with a discerning eye. Adopt a skeptical mindset when giving your overall feedback.

              The problem and solution pairs have been evaluated according to these questions:
              Questions about the problem statement:
              {problem_questions}

              Questions about the solution statement:
              {solution_questions}
              Here's your knowledge: \n\n" + circular_economy_knowledge"""
    user = f"""Based on these evaluations, please generate an overall SWOT analysis. Then, recommend shortlisting this idea or not with 2 sentence reasoning. Output as a JSON file with the key: SWOT analysis and recommendation.

              Problem evaluations:
              {prob_eval_text}

              Solution evaluations:
              {sol_eval_text}"""
    max_tokens = 1200
    temp = 1
    response = run_open_ai(model, system, user, max_tokens, 1, None, temp)
    print(response)
    return response


def get_problem_solution_eval_result(problem_text, solution_text):

    problem_prompt_answers = problem_eval(problem_text)
    solution_prompt_answers = solution_eval(problem_text, solution_text)
    summary = summary_eval(problem_prompt_answers, solution_prompt_answers)

    print(problem_prompt_answers)
    print(solution_prompt_answers)
    print(summary)

    return json.loads(problem_prompt_answers), json.loads(solution_prompt_answers), json.loads(summary)

# if __name__ == '__main__':
#     prob_evaluation = problem_eval("The construction industry is indubitably one of the significant contributors to global waste, contributing approximately 1.3 billion tons of waste annually, exerting significant pressure on our landfills and natural resources. Traditional construction methods entail single-use designs that require frequent demolitions, leading to resource depletion and wastage.")
#     sol_evaluation = solution_eval("The construction industry is indubitably one of the significant contributors to global waste, contributing approximately 1.3 billion tons of waste annually, exerting significant pressure on our landfills and natural resources. Traditional construction methods entail single-use designs that require frequent demolitions, leading to resource depletion and wastage. ", 
#                   "Herein, we propose an innovative approach to mitigate this problem: Modular Construction. This method embraces recycling and reuse, taking a significant stride towards a circular economy.   Modular construction involves utilizing engineered components in a manufacturing facility that are later assembled on-site. These components are designed for easy disassembling, enabling them to be reused in diverse projects, thus significantly reducing waste and conserving resources.  Not only does this method decrease construction waste by up to 90%, but it also decreases construction time by 30-50%, optimizing both environmental and financial efficiency. This reduction in time corresponds to substantial financial savings for businesses. Moreover, the modular approach allows greater flexibility, adapting to changing needs over time.  We believe, by adopting modular construction, the industry can transit from a 'take, make and dispose' model to a more sustainable 'reduce, reuse, and recycle' model, driving the industry towards a more circular and sustainable future. The feasibility of this concept is already being proven in markets around the globe, indicating its potential for scalability and real-world application.")
#     summary_eval(prob_evaluation, sol_evaluation)