import os
from typing import Literal
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables from .env file
load_dotenv()

# Configure Gemini API
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
# Initialize model
model = genai.GenerativeModel("gemini-2.5-flash")

def classify_query(query: str) -> Literal["web search", "assistant task", "unknown"]:
    prompt = (
        "Classify the following user query as either a 'web search query' or a 'personal assistant task'.\n"
        "Only reply with one of: 'web search' or 'assistant task'.\n\n"
        f"Query: {query}"
    )

    try:
        response = model.generate_content(prompt)
        reply = response.text.strip().lower()

        if "web search" in reply:
            return "web search"
        elif "assistant task" in reply:
            return "assistant task"
        else:
            return "unknown"
    except Exception as e:
        print(f"[Error] Gemini classification failed: {e}")
        return "unknown"

# Example usage
if __name__ == "__main__":
    user_query = input("Enter your query: ")
    result = classify_query(user_query)

    if result == "web search":
        print("✅ Valid Web Search Query. Proceeding...")
        # continue to scraping/summarization module
    elif result == "assistant task":
        print("❌ Detected Assistant Task. Currently unsupported.")
    else:
        print("⚠️ Could not classify the query. Please try again.")
