from openai import OpenAI
from utils import build_system_prompt

client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")

def chat_with_ai(persona, history, user_input):
    messages = [{"role": "system", "content": build_system_prompt(persona)}]
    for entry in history:
        messages.append({"role": "user", "content": entry["user"]})
        messages.append({"role": "assistant", "content": entry["ai"]})
    messages.append({"role": "user", "content": user_input})

    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=0.7,
        stream=False,
    )

    return completion.choices[0].message.content