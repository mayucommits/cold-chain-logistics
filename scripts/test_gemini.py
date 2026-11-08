
import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY not found in .env")

llm = ChatGoogleGenerativeAI(
    model="gemini-3.8-flash",
    google_api_key=api_key,
    temperature=0.2,
)

response = llm.invoke("Explain cold chain logistics in 3 simple sentences.")

for block in response.content:
    if block.get("type") == "text":
        print(block["text"], flush=True)
