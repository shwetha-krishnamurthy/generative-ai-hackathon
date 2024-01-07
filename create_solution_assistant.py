import os
import utils
from openai import OpenAI
from tavily import TavilyClient

os.environ['OPENAI_API_KEY'] = "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"
os.environ["TAVILY_API_KEY"] = "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"

def create_solution_evaluation_assistant(solution_file_path):
    # Initialize clients with API keys
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    tavily_client = TavilyClient(api_key=os.environ["TAVILY_API_KEY"])

    assistant_prompt_instruction = """You a VC analyst specializing in sustainability investing.
    You need to evaluate the solution to a problem given in the file.
    You need to search the internet to evaluate it.
    You can say you need more information if you don't find enough information.
    You need to answers in 1 or max 2 sentences.
    You need to see if the solution adheres to the following principles of circular economy: 
        1. Design Out Waste and Pollution
            1.1 Focus on designing products that minimize waste and pollution from the outset.
            1.2 Implement sustainable manufacturing processes.
        2. Keep Products and Materials in Use
            2.1 Promote the reuse, repair, and refurbishment of products.
            2.2 Emphasize durability and modularity in product design.
        3. Regenerate Natural Systems
            3.1 Encourage the use of renewable resources.
            3.2 Implement practices that restore and revitalize natural ecosystems.
    """
    file = client.files.create(
        file=open(
                solution_file_path,
                "rb",
            ),
            purpose="assistants",
    )

    # Create an assistant
    assistant = client.beta.assistants.create(
        instructions=assistant_prompt_instruction,
        model="gpt-4",
        tools=[{"type": "retrieval"},
               {"type": "code_interpreter"},
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
        file_ids=[file.id],
    )

    return assistant, client, tavily_client

def get_solution_prompt_answers(solution_file_path):
    assistant, client, tavily_client = create_solution_evaluation_assistant(solution_file_path)

    prompt_list = [
    # "Does the solution address the problem directly? Answer yes or no",
    # "How feasible is the solution?",
    # "How unique is this solution? Use web search to support your claims",
    # "What are the risks in implementing this solution?",
    # "What are the potential challenges in implementing this solution?",
    "What additional data does this solution need to help your evaluation further?"
    ]

    prompt_answer_dict_list = utils.get_eval_answers(prompt_list, assistant, client, tavily_client)

    return prompt_answer_dict_list
