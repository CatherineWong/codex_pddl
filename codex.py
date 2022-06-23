import openai
import os
from time import sleep

if not os.getenv("OPENAI_API_KEY"):
    raise ValueError(
        "OPENAI_API_KEY is not set. Please set this in the shell via `export OPENAI_API_KEY=...`"
    )
openai.api_key = os.environ["OPENAI_API_KEY"]


def get_completion(prompt, temperature, stop):
    response = openai.Completion.create(
        engine="code-davinci-002",
        prompt=prompt,
        temperature=temperature,
        max_tokens=800,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
        stop=stop,
        n=1,
    )
    return response.choices[0]["text"]

