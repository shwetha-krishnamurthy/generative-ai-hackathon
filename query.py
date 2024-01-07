from openai import OpenAI


def run_open_ai(model, system, user, tokens, n, stop, temp):
    """
    Base OpenAI Function.

    Args:
        model (str): OpenAI model name
        system (str): System prompt
        user (str): User prompt
        tokens (int): Max tokens
        n (int): The number of completion choices to generate. Usually 1
        stop (str): optional setting that tells the API when to stop generating tokens. Usually None
        temp (float): Set temperature

    Returns:
        prompt response (str)

    """
    client = OpenAI()

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
        max_tokens=tokens,
        n=n,
        stop=stop,
        temperature=temp
    )

    return response.choices[0].message.content
