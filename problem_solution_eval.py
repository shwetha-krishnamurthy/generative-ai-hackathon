import create_problem_assistant
import create_solution_assistant

def get_problem_solution_eval_result(problem_file_path, solution_file_path):

    problem_prompt_answers = create_problem_assistant.get_problem_prompt_answers(problem_file_path)
    solution_prompt_answers = create_solution_assistant.get_solution_prompt_answers(solution_file_path)

    print(problem_prompt_answers)
    print(solution_prompt_answers)

if __name__ == '__main__':
    get_problem_solution_eval_result("./problem_file.txt", "./solution_file.txt")