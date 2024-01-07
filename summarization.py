import os
import utils
from openai import OpenAI
from tavily import TavilyClient

os.environ['OPENAI_API_KEY'] = "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"
os.environ["TAVILY_API_KEY"] = "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"

def create_summarization_assistant():
    # Initialize clients with API keys
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    tavily_client = TavilyClient(api_key=os.environ["TAVILY_API_KEY"])

    assistant_prompt_instruction = """Given a list of questions and answers, you need to summarize
    the text in 50 words.
    """

    # Create an assistant
    assistant = client.beta.assistants.create(
        instructions=assistant_prompt_instruction,
        model="gpt-4",
    )

    return assistant, client, tavily_client

def get_summarization(problem_sol_prompt_answer_dict_list):
    assistant, client, tavily_client = create_summarization_assistant()

    prompt_list = [f"Question: {d[0]}; Answer: {d[1]}" for d in problem_sol_prompt_answer_dict_list]

    prompt_answer_dict_list = utils.get_eval_answers(prompt_list, assistant, client, tavily_client)

    return prompt_answer_dict_list
