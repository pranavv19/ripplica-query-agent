import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-2.5-flash")

def llm_find_similar_index(user_query: str, cached_queries: list[str]) -> int:
    if not cached_queries:
        return -1
    prompt = (
        "Given the following list of previous queries, does any of them mean the same as: '" + user_query + "'?\n"
        "If yes, return the 0-based index of the most similar one from the list below.\n"
        "If not, return -1.\n"
        "List of previous queries (one per line):\n" + "\n".join(f"{i}: {q}" for i, q in enumerate(cached_queries))
    )
    try:
        response = model.generate_content(prompt)
        reply = response.text.strip()
        # Try to extract an integer index from the reply
        for line in reply.splitlines():
            line = line.strip()
            if line.isdigit() or (line.startswith('-') and line[1:].isdigit()):
                return int(line)
        # fallback: try to parse the whole reply
        try:
            return int(reply)
        except Exception:
            return -1
    except Exception as e:
        print(f"[Error] Gemini LLM semantic match failed: {e}")
        return -1

# Example usage
def test():
    queries = [
        "best places to visit in delhi",
        "how to bake a cake",
        "current weather in new york",
        "python list comprehension tutorial"
    ]
    user_query = "top tourist attractions in delhi"
    idx = llm_find_similar_index(user_query, queries)
    print(f"LLM returned index: {idx}")
    if idx != -1:
        print(f"Most similar cached query: {queries[idx]}")
    else:
        print("No similar query found.")

if __name__ == "__main__":
    test() 