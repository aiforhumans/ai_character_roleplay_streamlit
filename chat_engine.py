from openai import OpenAI
from utils import build_system_prompt


class ChatEngine:
    """Wrapper around the OpenAI client used by the app."""

    def __init__(self, base_url: str = "http://localhost:1234/v1", api_key: str = "lm-studio"):
        self.client = OpenAI(base_url=base_url, api_key=api_key)

    def list_models(self):
        """Return available model identifiers."""
        try:
            models = self.client.models.list()
            return [m.id for m in models.data]
        except Exception:
            return ["gpt-3.5-turbo"]

    def stream_chat(self, messages, model, temperature, top_p, max_tokens):
        """Yield chunks of a streamed chat completion."""
        stream = self.client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature,
            top_p=top_p,
            max_tokens=max_tokens,
            stream=True,
        )
        for chunk in stream:
            delta = chunk.choices[0].delta
            content = getattr(delta, "content", None)
            if content is not None:
                yield content

    def chat_with_history(self, persona_file, history, user_input, model="gpt-3.5-turbo"):
        """Send chat completion request using stored history."""
        messages = [{"role": "system", "content": build_system_prompt(persona_file)}]
        for entry in history:
            messages.append({"role": "user", "content": entry["user"]})
            messages.append({"role": "assistant", "content": entry["ai"]})
        messages.append({"role": "user", "content": user_input})

        completion = self.client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=0.7,
            stream=False,
        )
        return completion.choices[0].message.content
