from query import run_open_ai
from pathlib import Path

with open(Path(__file__).parent / "CircularEconomyResearch.md", 'r', encoding="utf-8") as file:
    file_content = file.read()


def solution_first_eval(solution):
    system = "Here's your knowledge" + file_content
    user = "does this solution use the principles of circular economy? answer yes or no only" + solution
    model = "gpt-3.5-turbo"
    max_tokens = 100
    temperature = 0
    return run_open_ai(model, system, user, max_tokens, 1, None, temperature)

def solution_address_directly(problem, solution):
    system = "Here's your knowledge" + file_content
    user = "Does this solution address the problem directly? Problem /n" + problem + "Solution /n" + solution
    model = "gpt-4"
    max_tokens = 1500
    temperature = 1
    return run_open_ai(model, system, user, max_tokens, 1, None, temperature)
    
