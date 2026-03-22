import streamlit as st
from monitoring.analytics import get_stats

st.title("📊 System Monitoring Dashboard")

stats = get_stats()

st.metric("Total Requests", stats["total_requests"])
st.metric("Avg Latency", stats["avg_latency"])

st.write("Intent Distribution")
st.json(stats["intent_distribution"])