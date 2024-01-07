import os
import utils
from openai import OpenAI
from tavily import TavilyClient


def create_summarization_assistant():
    # Initialize clients with API keys
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    tavily_client = TavilyClient(api_key=os.environ["TAVILY_API_KEY"])

    assistant_prompt_instruction = """Given a list of questions and answers, you need to summarize
    only the answers parts.
    You are a VC analyst who specializes in sustainability investing.
    Based on the answers, you need to make a good suggestion on whether you will recommend to invest in
    this idea. 
    """

    # Create an assistant
    assistant = client.beta.assistants.create(
        instructions=assistant_prompt_instruction,
        model="gpt-4-1106-preview",
    )

    return assistant, client, tavily_client

def get_summarization(problem_sol_prompt_answer_dict_list):
    assistant, client, tavily_client = create_summarization_assistant()

    prompt_list = [f"Question: {d[0]}; Answer: {d[1]}" for d in problem_sol_prompt_answer_dict_list]

    prompt_answer_dict_list = utils.get_eval_answers(prompt_list, assistant, client, tavily_client)

    return prompt_answer_dict_list
