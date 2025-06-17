import openai
import os

# Use environment variable set earlier (from PowerShell)
openai.api_key = os.getenv("OPENAI_API_KEY")

def format_natural_translation(original, translated, to_lang):
    """
    Uses OpenAI to reformat the translation into a natural, culturally appropriate version
    and optionally provide literal meaning or breakdown.
    """
    if not openai.api_key:
        print("❌ OpenAI API key not set. Please set it as an environment variable.")
        return translated

    prompt = f"""
You are a professional translator and linguistic assistant.

Original Sentence: "{original}"
Rough Translation: "{translated}"
Target Language: {to_lang}

Now, refine this translation for:
1. Direct Accurate Translation
2. Literal Meaning Breakdown (if relevant)
3. Natural/Native-Sounding Version

Output Format:
------------------------
📘 Direct Translation: ...
🧩 Literal Breakdown: ...
💬 Native/Natural Style: ...
------------------------
Use the target language ({to_lang}) wherever necessary.
"""

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{
                "role": "user",
                "content": prompt
            }],
            temperature=0.7,
            max_tokens=500
        )
        answer = response.choices[0].message.content.strip()
        return answer
    except Exception as e:
        print(f"❌ OpenAI formatting failed: {e}")
        return translated
