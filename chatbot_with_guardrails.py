import os
import re
import logging
from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory

# Load API key from .env
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

# Setup logging
logging.basicConfig(filename="logs/red_team_attempts.log", level=logging.INFO)

# Red team keyword detection
def detect_prompt_injection(prompt):
    jailbreaking_keywords = [
        "ignore previous", "pretend", "disregard above", "system message", "you are now",
        "roleplay", "bypass", "forget instructions", "act as", "simulate"
    ]
    for keyword in jailbreaking_keywords:
        if keyword.lower() in prompt.lower():
            return True
    return False

# Init LLM with memory
llm = ChatOpenAI(temperature=0.7, openai_api_key=openai_api_key)
conversation = ConversationChain(llm=llm, memory=ConversationBufferMemory())

# Chat loop
print("🛡️ Guarded Chatbot | Type 'exit' to quit\n")
while True:
    user_input = input("You: ")

    if user_input.strip().lower() == "exit":
        print("Goodbye.")
        break

    # Guard check
    if detect_prompt_injection(user_input):
        print("🚨 Potential prompt injection detected. Input blocked.")
        logging.info(f"[BLOCKED] {user_input}")
        continue

    # Normal response
    response = conversation.predict(input=user_input)
    print(f"Bot: {response}")
