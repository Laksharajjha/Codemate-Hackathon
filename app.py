import os
from dotenv import load_dotenv
import requests 
from flask import Flask, render_template, request, jsonify
from main import process_command 

# Load environment variables from .env file for local development
load_dotenv()

app = Flask(__name__)

# --- SECURE API KEY SETUP ---
# This will get the key from your local .env file OR from PythonAnywhere's secrets
API_KEY = os.environ.get('API_KEY')
# --- END SETUP ---

KNOWN_COMMANDS = ['ls', 'cd', 'pwd', 'mkdir', 'rm', 'status', 'echo']

@app.route('/', methods=['GET', 'POST'])
def index():
    output = ""
    if request.method == 'POST':
        command = request.form['command'].strip()
        
        if not command:
            return render_template('index.html', output="")

        first_word = command.split()[0].lower()

        if first_word in KNOWN_COMMANDS:
            output = process_command(command)
        
        else:
            # THIS IS THE CORRECTED CHECK
            if not API_KEY:
                output = "AI feature is not configured. Please set the API_KEY environment variable."
            else:
                try:
                    user_query = command
                    prompt = f"Given the user request '{user_query}', convert it to a single, basic shell command. The available commands are: ls, cd, pwd, mkdir, rm, status, echo. Important: The 'rm' command works for both files and directories without any flags like '-r'. Just use 'rm <path>'. Return only the command itself with no explanation or extra text."
                    
                    response = requests.post(
                        url="https://openrouter.ai/api/v1/chat/completions",
                        headers={"Authorization": f"Bearer {API_KEY}"},
                        json={
                            "model": "mistralai/mistral-7b-instruct:free",
                            "messages": [{"role": "user", "content": prompt}]
                        }
                    )
                    response.raise_for_status()
                    
                    raw_ai_response = response.json()['choices'][0]['message']['content'].strip()
                    ai_command = raw_ai_response.replace("<s>", "").replace("</s>", "").replace("[OUT]", "").replace("[/OUT]", "").strip()
                    
                    output = f"> Your request: '{user_query}'\n> Executing: '{ai_command}'\n\n{process_command(ai_command)}"

                except Exception as e:
                    output = f"AI Error: {e}\n\n{response.text if 'response' in locals() else 'No response from server.'}"
            
    return render_template('index.html', output=output)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
