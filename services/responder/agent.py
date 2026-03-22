import google.generativeai as genai
import os

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

model = genai.GenerativeModel("gemini-1.5-flash")

def generate_response(query: str, docs):
    context = "\n".join([doc.page_content for doc in docs])

    prompt = f"""
    You are a smart customer support assistant.

    Context:
    {context}

    User Query:
    {query}

    Give a helpful, accurate response.
    """

    response = model.generate_content(prompt)
    return response.text