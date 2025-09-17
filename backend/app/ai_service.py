import os
from typing import Optional
from openai import OpenAI

class AIService:
    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY")
        self.model = os.getenv("AI_MODEL", "gpt-4o-mini")
        if not api_key:
            self.client = None
        else:
            self.client = OpenAI(api_key=api_key)

    def summarize_or_answer(self, prompt: str) -> str:
        if not self.client:
            return "AI is not configured. Please set OPENAI_API_KEY."
        resp = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "You are a helpful culinary assistant."},
                {"role": "user", "content": prompt},
            ],
            temperature=0.2
        )
        return resp.choices[0].message.content.strip()
