from pathlib import Path
from openai import OpenAI

key_file_path = Path(r"C:\Users\alexj\Documents\open_ai\key_1.txt")

with open(file_path, 'r') as file:
    key = file.read()

client = OpenAI(api_key=key)

completion = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {
            "role": "user",
            "content": "Write a haiku about recursion in programming."
        }
    ]
)

print(completion.choices[0].message)