import streamlit as st
import requests

st.set_page_config(page_title="AI Support Agent", layout="wide")

st.title("🤖 AI Customer Support System")

query = st.text_input("Enter your query")

if st.button("Submit"):
    with st.spinner("Processing..."):
        res = requests.post(
            "https://your-render-url/query",
            params={"q": query}
        )

        data = res.json()

        st.subheader("Intent")
        st.write(data["intent"])

        st.subheader("Response")
        st.write(data["response"])