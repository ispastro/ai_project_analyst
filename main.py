import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()

print("Key loaded:", os.getenv("OPENROUTER_API_KEY")[:8] if os.getenv("OPENROUTER_API_KEY") else "MISSING")

llm = ChatOpenAI(
    model="openrouter/free",
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1",
    timeout=30,
)

print("Sending request...")
response = llm.invoke("Say hello and confirm you're working.")
print("Response received:")
print(response.content)