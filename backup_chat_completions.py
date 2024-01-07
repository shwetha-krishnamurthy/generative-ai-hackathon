
import json
from query import run_open_ai

# VC Problem evaluation questions & Solutions
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

# Knowledge about the circular economy and its criteria
circular_economy_knowledge = "Deep Dive into Circular Economy\nIntroduction\nThe circular economy represents a systemic shift from traditional linear economic models (make, use, dispose) to an eco-friendly approach that emphasizes the reuse, repair, refurbishment, and recycling of materials and products. This transformation is crucial in addressing environmental challenges, such as resource depletion and climate change.\n\nPrinciples of Circular Economy\n1. Design Out Waste and Pollution\nFocus on designing products that minimize waste and pollution from the outset.\nImplement sustainable manufacturing processes.\n2. Keep Products and Materials in Use\nPromote the reuse, repair, and refurbishment of products.\nEmphasize durability and modularity in product design.\n3. Regenerate Natural Systems\nEncourage the use of renewable resources.\nImplement practices that restore and revitalize natural ecosystems.\nChallenges in Circular Economy\n1. Economic and Market Challenges\nThe transition to a circular economy requires changes in market structures and business models.\nConvincing stakeholders and consumers to adopt circular practices can be difficult.\n2. Technological and Infrastructural Barriers\nDeveloping and adopting technologies for recycling and refurbishing is costly and complex.\nThere is a need for infrastructure to support circular economy practices, like widespread collection and recycling systems.\n3. Regulatory and Policy Frameworks\nThe lack of supportive regulatory frameworks can hinder the growth of circular economy initiatives.\nPolicies need to incentivize sustainable practices and penalize linear, wasteful approaches.\nImpactful Solutions in Circular Economy\n1. Sustainable Product Design\nDesign products that are easy to disassemble for repair or recycling.\nUse environmentally friendly materials.\n2. Business Model Innovation\nAdopt models like product-as-a-service, where businesses retain ownership of products and customers pay for the service.\nImplement sharing platforms to maximize the use of products.\n3. Industrial Symbiosis\nEncourage different industries to work together, where waste from one industry becomes the input for another.\nFoster collaborations that lead to innovative uses of waste materials.\n4. Consumer Engagement and Education\nEducate consumers about the benefits of circular economy products and practices.\nEngage consumers in sustainability through incentives and awareness campaigns.\n5. Technology and Innovation\nInvest in technology that facilitates recycling and the efficient use of resources.\nInnovate in areas like biodegradable materials and renewable energy sources.\nConclusion\nThe circular economy presents a transformative approach to sustainability, focusing on a regenerative and restorative model. While there are challenges, the potential for innovation and environmental impact is substantial. Embracing circular economy principles can lead to a more sustainable and economically viable future."



def problem_eval(problem_text):
    model = "gpt-4"
    system = "You are an unbiased expert on Circular Economy, helping a VC analyst sift through ideas with a discerning eye. Adopt a skeptical mindset when analyzing the idea. Here's your knowledge: \n\n" + circular_economy_knowledge
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
    system = "You are an unbiased expert on Circular Economy, helping a VC analyst sift through ideas with a discerning eye. Adopt a skeptical mindset when analyzing the idea. Here's your knowledge: \n\n" + circular_economy_knowledge
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
    user = """Based on these evaluations, please generate an overall SWOT analysis and whether to shortlist this idea or not. Output as valid JSON object in this format:{SWOT Analysis: 8-sentence-string with new lines between each item, Recommendation: 2-sentence-string} do not nest the JSON output. 

              Problem evaluations:""" + prob_eval_text + "Solution evaluations: " + sol_eval_text
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