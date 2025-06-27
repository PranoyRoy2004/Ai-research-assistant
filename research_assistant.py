import streamlit as st
import requests
import json

# ---------------------- CONFIG ----------------------
GEMINI_API_KEY = "Your_gemini_API_key"  # Replace with your actual Gemini API key
EXA_API_KEY = "Your_Exa_API_key"   # Replace with your actual Exa API key


# ---------------------- FUNCTIONS ----------------------

def call_gemini_api(prompt):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GEMINI_API_KEY}"
    headers = {'Content-Type': 'application/json'}
    payload = {"contents": [{"parts": [{"text": prompt}]}]}
    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()
    return response.json()["candidates"][0]["content"]["parts"][0]["text"]

def rewrite_query(query):
    prompt = f"Rewrite this query to be more specific and search-friendly. Only return the rewritten query without explanations:\n\n{query}"
    return call_gemini_api(prompt)

def summarize_content(content):
    prompt = f"Summarize this content into 3 bullet points:\n\n{content}"
    return call_gemini_api(prompt)

def search_exa(query):
    url = "https://api.exa.ai/search"
    headers = {
        "x-api-key": "your_exa_API_key",  # ✅ fixed
        "Content-Type": "application/json"
    }
    payload = {
        "query": query,
        "type": "auto",
        "contents": {
            "text": True
        }
    }
    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()
    return response.json()





# ---------------------- STREAMLIT UI ----------------------

st.title("🔍 AI Research Assistant (Powered by Gemini + Exa)")

query = st.text_input("Enter your search query:")
if st.button("Search") and query.strip():
    with st.spinner("Rewriting query and fetching results..."):
        new_query = rewrite_query(query)
        st.markdown(f"**Rewritten Query:** {new_query}")

        results = search_exa(new_query)

        if "results" not in results or len(results["results"]) == 0:
            st.warning("No results found.")
        else:
            for idx, item in enumerate(results["results"], 1):
                st.subheader(f"{idx}. {item.get('title', 'No Title')}")
                st.write(item.get('url', 'No URL'))
                summary = summarize_content(item.get('text', ''))
                st.markdown("**Summary:**")
                st.markdown(summary)
