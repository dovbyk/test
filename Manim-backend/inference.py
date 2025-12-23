import os
from openai import OpenAI
from dotenv import load_dotenv
import random


def load_system_prompt(file_path="system_prompt.txt"):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read().strip()
    except FileNotFoundError:
        raise RuntimeError(f"Critical Error: {file_path} not found.")


def generate_manim_script(user_prompt, previous_script=None, previous_error = None, filename="manim_output6.py", directory = "temp"):
    load_dotenv()

    
    api_keys_str = os.getenv("OPENROUTER_API_KEYS", "")
    api_keys_list = [k.strip() for k in api_keys_str.split(",") if k.strip()]
    
    if not api_keys_list:
        raise RuntimeError("No API keys found in environment variables.")

    
    selected_key = random.choice(api_keys_list)
    print(f"Using API Key: {selected_key[:10]}...") 
    
    
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=selected_key,
    )

    if not os.path.exists(directory):
        os.makedirs(directory)

    file_path = os.path.join(directory, filename)
    
    
    model_name = "xiaomi/mimo-v2-flash:free"

    if not previous_script or not previous_error:
        system_prompt = load_system_prompt()
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
    else:
        messages = [
            {"role": "system", "content": "You are a Manim animation code expert."},
            {"role": "user", "content": f"## User Prompt:\n{user_prompt}\n\n## Previous Script (with Manim error):\n```python\n{previous_script}\n```\n\n## Error Message:\n{previous_error}\n\n1. Analyze Traceback. 2. Identify Root Cause. 3. Correct code only. 4. Preserve intent. 5. Output only Python script in markdown code block and nothing else."}
        ]

    try:
        response = client.chat.completions.create(
            model=model_name,
            messages=messages,
            extra_body={
                "include_reasoning": False 
            },
            extra_headers={
                "HTTP-Referer": "http://localhost:3000", # Useful for rankings
                "X-Title": "Manim-Video-Generator",
            }
        )
        
        script_content = response.choices[0].message.content
        if script_content:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(script_content)
            return os.path.abspath(file_path)
        else:
            raise RuntimeError("OpenRouter returned empty response.")
    except Exception as e:
        raise RuntimeError(f"API call failed: {str(e)}")
