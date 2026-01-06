import json
import os
from openai import OpenAI
from tools import create_file, read_file, list_files
from prompts import SYSTEM_PROMPT
import dotenv

dotenv.load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def main():
    while True:
        task = input("What do you want to do? (type 'exit' to stop): ")

        if task.lower() == "exit":
            break

        # 1. Read project structure
        files = list_files()

        # 2. Read existing file contents
        context = ""
        for file_path in files:
            context += f"\nFile: {file_path}\n"
            context += read_file(file_path)
            context += "\n"

        # 3. Build augmented prompt
        user_prompt = f"""
User request:
{task}

Current project files and contents:
{context}
"""

        # 4. Call OpenAI
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.2
        )

        text = response.choices[0].message.content

        # 5. Parse JSON
        try:
            start = text.find("{")
            end = text.rfind("}") + 1
            data = json.loads(text[start:end])
        except Exception:
            print("❌ Invalid JSON from model")
            print(text)
            continue

        # 6. Apply changes
        for file in data["files"]:
            create_file(file["path"], file["content"])

        print(f"✅ Updated {len(data['files'])} file(s)")

if __name__ == "__main__":
    main()
