import os
import utils
from openai import OpenAI
from tavily import TavilyClient


def create_problem_evaluation_assistant(problem_file_path):
    # Initialize clients with API keys
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    tavily_client = TavilyClient(api_key=os.environ["TAVILY_API_KEY"])

    # Knowledge about the circular economy and its criteria
    circular_economy_knowledge = "Deep Dive into Circular Economy\nIntroduction\nThe circular economy represents a systemic shift from traditional linear economic models (make, use, dispose) to an eco-friendly approach that emphasizes the reuse, repair, refurbishment, and recycling of materials and products. This transformation is crucial in addressing environmental challenges, such as resource depletion and climate change.\n\nPrinciples of Circular Economy\n1. Design Out Waste and Pollution\nFocus on designing products that minimize waste and pollution from the outset.\nImplement sustainable manufacturing processes.\n2. Keep Products and Materials in Use\nPromote the reuse, repair, and refurbishment of products.\nEmphasize durability and modularity in product design.\n3. Regenerate Natural Systems\nEncourage the use of renewable resources.\nImplement practices that restore and revitalize natural ecosystems.\nChallenges in Circular Economy\n1. Economic and Market Challenges\nThe transition to a circular economy requires changes in market structures and business models.\nConvincing stakeholders and consumers to adopt circular practices can be difficult.\n2. Technological and Infrastructural Barriers\nDeveloping and adopting technologies for recycling and refurbishing is costly and complex.\nThere is a need for infrastructure to support circular economy practices, like widespread collection and recycling systems.\n3. Regulatory and Policy Frameworks\nThe lack of supportive regulatory frameworks can hinder the growth of circular economy initiatives.\nPolicies need to incentivize sustainable practices and penalize linear, wasteful approaches.\nImpactful Solutions in Circular Economy\n1. Sustainable Product Design\nDesign products that are easy to disassemble for repair or recycling.\nUse environmentally friendly materials.\n2. Business Model Innovation\nAdopt models like product-as-a-service, where businesses retain ownership of products and customers pay for the service.\nImplement sharing platforms to maximize the use of products.\n3. Industrial Symbiosis\nEncourage different industries to work together, where waste from one industry becomes the input for another.\nFoster collaborations that lead to innovative uses of waste materials.\n4. Consumer Engagement and Education\nEducate consumers about the benefits of circular economy products and practices.\nEngage consumers in sustainability through incentives and awareness campaigns.\n5. Technology and Innovation\nInvest in technology that facilitates recycling and the efficient use of resources.\nInnovate in areas like biodegradable materials and renewable energy sources.\nConclusion\nThe circular economy presents a transformative approach to sustainability, focusing on a regenerative and restorative model. While there are challenges, the potential for innovation and environmental impact is substantial. Embracing circular economy principles can lead to a more sustainable and economically viable future."

    with open(problem_file_path, 'rb') as f:
        problem_text = f.read()

    assistant_prompt_instruction = f""""You are an unbiased expert on Circular Economy,
    helping a VC analyst sift through ideas with a discerning eye. Adopt a skeptical
    mindset when analyzing the idea. Here's your knowledge: {circular_economy_knowledge}
    Here is a problem solution pair that you received from a young startup:
    {problem_text}\n
    The startup is trying to solve the given problem.
    You need to evaluate the problem given in the file.
    You need to do some market research and understand if the problem being addressed has any impact on the climate.
    You need to search the web whenever the document doesn't have enough information.
    You need to give answers in 1 or maximum 2 sentences.
    """
    # file = client.files.create(
    #     file=open(
    #             problem_file_path,
    #             "rb"
    #         ),
    #         purpose="assistants",
    # )

    # Create an assistant
    assistant = client.beta.assistants.create(
        instructions=assistant_prompt_instruction,
        model="gpt-4-1106-preview",
        tools=[
            {
            "type": "function",
            "function": {
                "name": "tavily_search",
                "description": "Get information on recent events from the web.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {"type": "string", "description": "The search query to use. For example: 'Latest news on Nvidia stock performance'"},
                    },
                    "required": ["query"]
                }
            }
        }],
        # file_ids=[file.id],
    )

    return assistant, client, tavily_client

def get_problem_prompt_answers(problem_file_path):
    assistant, client, tavily_client = create_problem_evaluation_assistant(problem_file_path)

    prompt_list = [
    # "Does the problem being addressed has any impact on the climate?",
    "What is the scale of the problem? (people, volume, money, etc)",
    # "Who faces this problem predominantly?",
    # "Who else is solving this problem?",
    "Has this problem been solved elsewhere?"
    ]

    prompt_answer_dict_list = utils.get_eval_answers(prompt_list, assistant, client, tavily_client)

    return prompt_answer_dict_list
