import os
from typing import List
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables from .env file
load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-2.5-flash")

# Summarize a single page
def summarize_text(text: str) -> str:
    prompt = (
        "Summarize the following web page content in concise bullet points. "
        "Focus on the most important facts, skip ads, navigation, and unrelated info. "
        "Limit to 10 bullets or less.\n\n"
        f"Content:\n{text[:4000]}"
    )
    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        print(f"[Error] Gemini summarization failed: {e}")
        return "[Summary unavailable]"

# Summarize multiple summaries into a final result
def summarize_multiple(summaries: List[str]) -> str:
    joined = "\n\n".join(summaries)
    prompt = (
        "Given the following bullet-point summaries from multiple web pages, "
        "combine them into a single, concise, non-redundant summary. "
        "Use bullet points or a structured format. Keep the total under 4096 tokens.\n\n"
        f"Summaries:\n{joined[:4000]}"
    )
    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        print(f"[Error] Gemini multi-summary failed: {e}")
        return "[Final summary unavailable]"

# Example usage
if __name__ == "__main__":
    # Example: summarize a single text
    text = input("Paste web page text to summarize:\n")
    print("\n--- Summary ---\n")
    print(summarize_text(text))

    # Example: summarize multiple summaries
    # summaries = ["- Point 1\n- Point 2", "- Fact A\n- Fact B"]
    # print("\n--- Final Summary ---\n")
    # print(summarize_multiple(summaries)) 