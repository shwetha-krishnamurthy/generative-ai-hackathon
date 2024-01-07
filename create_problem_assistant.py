import os
import utils
from openai import OpenAI
from tavily import TavilyClient

os.environ['OPENAI_API_KEY'] = "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"
os.environ["TAVILY_API_KEY"] = "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"

def create_problem_evaluation_assistant(problem_file_path):
    # Initialize clients with API keys
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    tavily_client = TavilyClient(api_key=os.environ["TAVILY_API_KEY"])

    assistant_prompt_instruction = """You a VC analyst specializing in sustainability investing.
    You need to evaluate the problem given in the file.
    You need to search the web whenever the document doesn't have enough information.
    """
    file = client.files.create(
        file=open(
                problem_file_path,
                "rb",
            ),
            purpose="assistants",
    )

    # Create an assistant
    assistant = client.beta.assistants.create(
        instructions=assistant_prompt_instruction,
        model="gpt-4-1106-preview",
        tools=[{"type": "retrieval"},
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

def get_problem_prompt_answers(problem_file_path):
    assistant, client, tavily_client = create_problem_evaluation_assistant(problem_file_path)

    prompt_list = [
    # "Does the problem being addressed has any impact on the climate?",
    # "What is the scale of the problem? (people, volume, money, etc)",
    # "Who faces this problem predominantly?",
    # "Who else is solving this problem?",
    "Has this problem been solved elsewhere?"
    ]

    prompt_answer_dict_list = utils.get_eval_answers(prompt_list, assistant, client, tavily_client)

    return prompt_answer_dict_list
