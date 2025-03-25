import subprocess
import json
import os

MODEL_PATH = "./_internal/llama.cpp/models/llama-2-7b-chat.Q4_K_M.gguf"
LLAMA_CLI_PATH = "./_internal/llama.cpp/build/bin/llama-cli"

def generate_response(prompt: str, temperature=0.7, max_tokens=256):
    command = [
        LLAMA_CLI_PATH,
        "-m", MODEL_PATH,
        "--temp", str(temperature),
        "-c", "1024",
        "--repeat-penalty", "1.1",
        "-p", prompt,
        "-n", str(max_tokens),
        "--simple-io"
    ]

    try:
        result = subprocess.run(command, capture_output=True, text=True, timeout=120)
        if result.returncode != 0:
            raise Exception(f"Llama error: {result.stderr}")

        response = result.stdout.strip()

        # Remove the original prompt from the response if present
        if response.startswith(prompt):
            response = response[len(prompt):].strip()

        # Remove the trailing '[end of text]' marker
        response = response.replace("[end of text]", "").strip()

        return response

    except subprocess.TimeoutExpired:
        raise Exception("Request timed out.")

def generate_structured_response(prompt: str):
    json_prompt = f"""
You are a friendly conversational AI assistant. The user will provide you with a message or ask a question, and your task is to respond in a conversational, friendly, and engaging manner.

User's message: "{prompt}"

Respond strictly in JSON format as follows:
{{
  "reply": "<Your conversational and engaging response here>"
}}

Ensure the reply is a single conversational response, wrapped clearly in a JSON object.
Don't include the initial prompt with your reply.
"""
    
    os.system('clear')
    print('---')
    print(raw_response)

    raw_response = generate_response(json_prompt)
    try:
        response_json = json.loads(raw_response)
        return response_json
    except json.JSONDecodeError:
        raise Exception("Failed to parse response as JSON.")