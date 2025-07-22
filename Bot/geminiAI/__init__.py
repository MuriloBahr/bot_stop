import os
from dataclasses import dataclass
from google import genai
from google.genai import types
from configs.configs import config

client = genai.Client(api_key=config.GEMINI_KEY)

@dataclass
class GeminiAI:

    def generate(self, prompt):
        model = "gemini-2.5-flash-lite-preview-06-17"
        contents = [
            types.Content(
                role="user",
                parts=[types.Part.from_text(text=prompt)],
            ),
        ]

        generate_content_config = types.GenerateContentConfig(
            thinking_config=types.ThinkingConfig(thinking_budget=0),
            response_mime_type="text/plain",
        )

        response = client.models.generate_content(
            model=model,
            contents=contents,
            config=generate_content_config,
        )
        result = response.text.replace('\n', ' ').strip()
        print(result)

        return result
