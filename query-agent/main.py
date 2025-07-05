from classify import classify_query
from embedder import get_embedding
from vector_store import check_similarity, add_to_store
from scraper import get_web_results
from summarizer import summarize_text, summarize_multiple
from cache import add_to_cache, get_cached_summary, get_all_queries, get_all_summaries
from llm_semantic_match import llm_find_similar_index


def main():
    user_query = input("Enter your query: ")
    user_query_lc = user_query.lower()

    # Step 1: Classify
    category = classify_query(user_query)
    if category != "web search":
        print("❌ This is not a valid web search query. Exiting.")
        return

    # Step 2: Embed
    embedding = get_embedding(user_query_lc).tolist()

    # Step 2a: Check cache for exact match
    cache_summary = get_cached_summary(user_query_lc)
    if cache_summary:
        print("\n✅ Found exact query in cache! Returning cached summary:\n")
        print(cache_summary)
        return

    # Step 2b: Vector store semantic match
    sim_summary = check_similarity(user_query_lc)
    if sim_summary:
        print("\n🔄 Returning cached summary (vector semantic match):\n")
        print(sim_summary)
        return

    # Step 2c: LLM-based semantic match
    cached_queries = get_all_queries()
    cached_summaries = get_all_summaries()
    idx = llm_find_similar_index(user_query_lc, cached_queries)
    if idx != -1:
        print("\n🤖 LLM found a semantically similar cached query! Returning cached summary:\n")
        print(cached_summaries[idx])
        return

    # Step 3: Scrape
    print("\n🔎 Scraping the web for fresh results...")
    snippets = get_web_results(user_query)
    if not snippets:
        print("❌ No web results found. Exiting.")
        return

    # Step 4: Summarize each page
    print("\n📝 Summarizing each page...")
    page_summaries = [summarize_text(snippet) for snippet in snippets]

    # Step 5: Summarize all summaries
    print("\n🧩 Combining all summaries...")
    final_summary = summarize_multiple(page_summaries)

    # Step 6: Show and cache result
    print("\n=== FINAL SUMMARY ===\n")
    print(final_summary)
    add_to_store(user_query_lc, final_summary)
    add_to_cache(user_query_lc, embedding, final_summary)
    print("\n✅ Result cached for future similar queries.")

if __name__ == "__main__":
    main() 