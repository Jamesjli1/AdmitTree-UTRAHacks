import os
import requests
from dotenv import load_dotenv

# Load secrets from .env
load_dotenv()

DO_AGENT_ENDPOINT = os.getenv("DO_AGENT_ENDPOINT")
DO_AGENT_KEY = os.getenv("DO_AGENT_KEY")

def get_chat_response(user_message):
    """
    Forwards the user's message to the DigitalOcean Agent.
    """
    # 1. Safety Check
    if not DO_AGENT_ENDPOINT or not DO_AGENT_KEY:
        print("Error: Missing DO_AGENT_ENDPOINT or DO_AGENT_KEY in .env")
        return "I'm having trouble accessing my brain (credentials missing)."

    try:
        # 2. DEBUGGING: Print exactly what we are using (Check your terminal!)
        print(f"DEBUG: Endpoint: {DO_AGENT_ENDPOINT}")
        print(f"DEBUG: Key: '{DO_AGENT_KEY}'") # Quotes help you see invisible spaces!

        # 3. Prepare the Headers
        headers = {
            "Authorization": f"Bearer {DO_AGENT_KEY}",
            "Content-Type": "application/json"
        }
        
        # 4. Prepare the Payload (OpenAI Compatible Format)
        # We use this format because your URL ends in /completions
        payload = {
            "messages": [
                {
                    "role": "user", 
                    # Add context 
                    "content": user_message + " (Answer in 2-3 short sentences maximum. Be extremely concise and conversational. Use only plain paragraphs. Do not use tables, lists, or bold formatting.)"
                }
            ]
        }

        print(f"Sending message to Agent...")

        # 5. Send to DigitalOcean
        response = requests.post(DO_AGENT_ENDPOINT, json=payload, headers=headers)
        
        # 6. Handle Response
        if response.status_code == 200:
            data = response.json()
            
            # Try to grab the text from standard OpenAI format
            try:
                return data["choices"][0]["message"]["content"]
            except KeyError:
                # Fallback if DigitalOcean uses a different format
                return data.get("answer", "I received a response, but it was empty.")
                
        else:
            print(f"Agent Error {response.status_code}: {response.text}")
            return "Sorry, I'm having trouble connecting to the AI agent right now."

    except Exception as e:
        print(f"Connection Exception: {e}")
        return "Sorry, I'm having trouble connecting to the AI agent right now."