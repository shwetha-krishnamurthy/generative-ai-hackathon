import json
import time

# Function to perform a Tavily search
def tavily_search(query, tavily_client):
    search_result = tavily_client.get_search_context(query, search_depth="advanced", max_tokens=8000)
    return search_result

# Function to wait for a run to complete
def wait_for_run_completion(thread_id, run_id, client):
    while True:
        time.sleep(1)
        run = client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run_id)
        print(f"Current run status: {run.status}")
        if run.status in ['completed', 'failed', 'requires_action']:
            return run

# Function to handle tool output submission
def submit_tool_outputs(thread_id, run_id, tools_to_call, client, tavily_client):
    tool_output_array = []
    for tool in tools_to_call:
        output = None
        tool_call_id = tool.id
        function_name = tool.function.name
        function_args = tool.function.arguments

        if function_name == "tavily_search":
            output = tavily_search(query=json.loads(function_args)["query"], tavily_client=tavily_client)

        if output: #Uncomment the condition if it throws an invalid request type error.
            tool_output_array.append({"tool_call_id": tool_call_id, "output": output})

    return client.beta.threads.runs.submit_tool_outputs(
        thread_id=thread_id,
        run_id=run_id,
        tool_outputs=tool_output_array
    )

# Function to print messages from a thread
def get_messages_from_thread(thread_id, client):
    messages = client.beta.threads.messages.list(thread_id=thread_id)

    prompt_answer_dict_list =[]
    user_answer_tuple_list = []

    for msg in messages:
        # print(f"{msg.role}: {msg.content[0].text.value}")
        user_answer_tuple_list.append((msg.role, msg.content[0].text.value))
        
    for idx, pair in enumerate(user_answer_tuple_list):
        if idx % 2 == 0:
            # prompt_answer_dict = {}
            next = user_answer_tuple_list[idx + 1]
            # prompt_answer_dict[pair[0]] = pair[1]
            # prompt_answer_dict[next[0]] = next[1]

            prompt_answer_dict_list.append((next[1], pair[1]))

    return prompt_answer_dict_list

def get_eval_answers(prompt_list, assistant, client, tavily_client):

    assistant_id = assistant.id
    print(f"Assistant ID: {assistant_id}")

    # Create a thread
    thread = client.beta.threads.create()
    print(f"Thread: {thread}")


    # Ongoing conversation loop
    for user_input in prompt_list:

        # Create a message
        message = client.beta.threads.messages.create(
            thread_id=thread.id,
            role="user",
            content=user_input,
        )

        # Create a run
        run = client.beta.threads.runs.create(
            thread_id=thread.id,
            assistant_id=assistant_id,
        )
        print(f"Run ID: {run.id}")

        # Wait for run to complete
        run = wait_for_run_completion(thread.id, run.id, client=client)

        if run.status == 'failed':
            print(run)
            continue

        elif run.status == 'requires_action':
            run = submit_tool_outputs(thread.id, run.id, run.required_action.submit_tool_outputs.tool_calls, client=client, tavily_client=tavily_client)
            run = wait_for_run_completion(thread.id, run.id, client=client)

    # Print messages from the thread
    prompt_answer_dict_list = get_messages_from_thread(thread.id, client)
    
    return prompt_answer_dict_list
