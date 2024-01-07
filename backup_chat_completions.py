
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

circular_economy_varied_examples = """ 
               Example 1:
               Problem:
               Many companies face challenges in effectively managing resources, leading to increased environmental impact and higher production expenses. This inefficiency results in waste, excessive energy consumption, and a negative environmental footprint.
               
               Solution:
               Industrial symbiosis, exemplified by the "Sustainable Synergies" project in Aalborg, enables companies to lower production costs, minimize environmental impact, and foster innovation by exchanging surplus materials, water, energy, and resources. This approach enhances resource and energy efficiency, reduces waste management expenses, and generates new economic opportunities. Additionally, it significantly contributes to environmental sustainability by cutting energy consumption, materials usage, and CO2 emissions, benefiting both businesses and the environment.
               
               Example 2: 
               Problem:
               Traditional waste disposal methods for drink cans and bottles lead to environmental issues and resource depletion. Low recycling rates contribute to excessive energy consumption and the extraction of virgin materials like bauxite.
               
               Solution:
               The Danish deposit and return system for recycling drink cans and bottles, led by Dansk Retursystem, achieved a remarkable 93% return rate in 2021, recycling 1.9 billion containers. This circular system promotes energy efficiency by using 95% less energy to produce cans from recycled materials and reduces the need for extracting bauxite. Effective cooperation among producers, consumers, and the Danish Return System ensures a high return rate, serving as an inspiring model to boost recycling rates and support the circular economy, in line with the EU's 90% collection goal for plastic bottles by 2029.
               
               Example 3:
               Problem:
               Worn-out artificial turf poses an environmental challenge, with disposal through incineration leading to significant CO2 emissions and waste accumulation, contributing to environmental pollution.
               
               Solution:
               Re-Match offers a pioneering solution by utilizing patented technology to efficiently separate worn-out artificial turf into clean, reusable components such as rubber granules, sand, and plastic fibers. This process reduces CO2 emissions dramatically, saving 400 tonnes of CO2 per pitch compared to incineration, while also minimizing waste, equivalent to 1.4 million plastic bags or 250 tonnes of waste. Re-Match's sustainable approach emits less than 20 tonnes of CO2 per pitch during the separation process, effectively addressing the environmental concerns associated with artificial turf disposal.
               
               Example 4:
               The recycling of lithium-ion batteries, crucial in the electrification of transportation and the shift towards sustainable energy solutions, has been challenging, resulting in the export, landfill disposal, and burning of these valuable resources in the USA.
               
               Solution:
               Li-Cycle addresses the problem by aiming to recover critical materials from lithium-ion batteries and reintroduce them sustainably into the supply chain. Their innovative approach seeks to establish a closed-loop, circular economy for battery materials, ensuring that secondary materials from used batteries can be economically and sustainably reused and reformed into new batteries. This initiative not only reduces environmental impact but also promotes the responsible and efficient management of lithium-ion batteries, contributing to a more sustainable future.
               
               Example 5:
               Problem:
               Brands often struggle to implement effective product take-back programs in the context of a circular economy. This results in wasted resources, missed revenue opportunities, and difficulties in tracking and measuring the environmental impact of their efforts.
               
               Solution:
               numi.circular's numi.platform offers a solution by providing circular economy software that facilitates product take-back programs for brands. Customers can return used products to earn recovery points, and the platform automates the sorting and distribution of these products. Additionally, it tracks all takebacks and generates impact reports, allowing brands to measure their environmental initiatives. By offering pre-owned inventory for resale and incentivizing customers with discounts, numi.circular helps companies adopt more sustainable practices, close product lifecycles, reduce waste, and create new revenue streams, ultimately contributing to a more circular and eco-conscious business model.
               
               Example 6:
               Problem:
               Agricultural biomass waste poses environmental challenges, as it often goes unused and contributes to pollution and greenhouse gas emissions. Additionally, there is a need for sustainable materials in industries like agriculture, construction, and carbon offsetting.
               
               Solution:
               Zimbanjex addresses these issues by converting agricultural biomass waste into biochar through a pyrolysis process. This biochar serves multiple purposes, including organic soil regeneration, long-term carbon storage, and applications in industries like cement production and road construction. Furthermore, the startup offers carbon removal certificates, allowing companies to offset their emissions while supporting sustainable practices. Zimbanjex's innovative approach not only minimizes biomass waste but also provides eco-friendly solutions for various industries, promoting a circular and environmentally conscious economy.
               
               Example 7:
               Problem:
               The conventional transportation of bikes often involves single-use cardboard packaging, which generates a significant amount of waste and has limited durability. This unsustainable practice contributes to environmental pollution and resource depletion.
               
               Solution:
               Circular logistics, a German startup, addresses this problem by offering the BikeBox, a sustainable bike transport packaging made from durable polypropylene. This foldable box not only reduces to 1/8th of its size for easy storage but also promotes continuous reuse, eliminating the need for single-use cardboard packaging. Polypropylene's durability allows for multiple reuses, and it is 100% recyclable at the end of its lifecycle. The BikeBox is designed for easy assembly, similar to traditional cardboard boxes. Additionally, circular logistics handles the return of these boxes, creating a waste-minimizing, closed-loop system that aligns with circular economy principles and promotes sustainability in bike transportation.
               
               Example 8:
               Problem:
               The hotel industry often faces challenges related to disposing of old mattresses, leading to waste generation and environmental concerns. Conventional mattress disposal methods contribute to landfills and resource depletion.
               
               Solution:
               Austrian startup MATR offers a solution by providing "Mattress-as-a-Service" to hotels, allowing them to reduce their environmental impact. MATR collects mattresses at the end of their lifespan, disassembles them, and recycles most of the components, reintroducing them into the material loop. This approach ensures that MATR mattresses are not wasted but continuously returned to the material cycle, reducing waste and minimizing the CO2 footprint compared to conventional mattress disposal methods. MATR's innovative service aligns with circular economy principles and promotes sustainability in the hotel industry.
            """


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
    return response

def summary_eval(prob_eval_text, sol_eval_text, problem_text, solution_text):
    model = "gpt-4"
    system = f"""You are an unbiased expert on Circular Economy, helping a VC analyst sift through ideas with a discerning eye. Adopt a skeptical mindset when giving your overall feedback.

              The problem and solution pairs have been evaluated according to these questions:
              Questions about the problem statement:
              {problem_questions}

              Questions about the solution statement:
              {solution_questions}
              These are a variety of great circular economy ideas: {circular_economy_varied_examples}"""
    user = """Based on these evaluations, please generate an overall SWOT analysis and your recommendation of how this idea compares relative to varied circular economy ideas in your knowledge. Output in JSON in this format:{SWOT Analysis: 8-sentence-string with new lines between each item, Recommendation: 2-sentence-string} do not nest the JSON output. 

              Problem statement:""" + f"""\n\n {problem_text} \n\n Solution statement: \n\n {solution_text}" \n\n
              Problem evaluations: \n\n {prob_eval_text} \n\n Solution evaluations: \n\n {sol_eval_text}"""
    max_tokens = 1200
    temp = 1
    response = run_open_ai(model, system, user, max_tokens, 1, None, temp)
    return response


def get_problem_solution_eval_result(problem_text, solution_text):

    problem_prompt_answers = problem_eval(problem_text)
    solution_prompt_answers = solution_eval(problem_text, solution_text)
    summary = summary_eval(problem_prompt_answers, solution_prompt_answers, problem_text, solution_text)

    return json.loads(problem_prompt_answers), json.loads(solution_prompt_answers), json.loads(summary)
