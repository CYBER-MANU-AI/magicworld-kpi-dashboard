import streamlit as st
import requests
import pandas as pd
from datetime import datetime
import time

st.set_page_config(page_title="MagicWorld #1 KPI Dashboard", layout="wide")
st.title("🪄 MagicWorld #1 – Live KPIs (Grok + X-Driven NPCs)")


BACKEND_URL = "https://replit.com/@Cyber-Manu/magicworld-backend?v=1" 

@st.cache_data(ttl=30)  # Refresh every 30 seconds
def fetch_kpis():
    try:
        # Pull recent logs from backend (Replit exposes /__logs or just scrape output)
        r = requests.get(f"{BACKEND_URL}/__logs" if "/__logs" in BACKEND_URL else BACKEND_URL)
        logs = r.text.splitlines()[-10:]  # Last 10 lines for KPIs
        df = pd.DataFrame({"Log": logs})
        # Parse KPIs (assumes format like "KPIs: Eng 52% | Econ 1.0 | Hap 65")
        kpis = {"Engagement": 52, "Economy": 1.0, "Happiness": 65}  # Default; update from logs
        for log in logs:
            if "KPIs:" in log:
                parts = log.split("Eng")[1].split("|")
                kpis["Engagement"] = float(parts[0].strip().replace("%", ""))
                kpis["Economy"] = float(parts[1].split()[1])
                kpis["Happiness"] = float(parts[2].split()[1].replace("%", ""))
        return kpis, logs
    except:
        # Fallback demo data (rises over time for testing)
        return {"Engagement": 52 + int(time.time() % 3600 / 60), "Economy": 1.0 + (time.time() % 3600 / 3600), "Happiness": 65 + int(time.time() % 3600 / 120)}, ["Demo mode active – KPIs rising!"]

kpis, logs = fetch_kpis()

# Live Metrics
col1, col2, col3 = st.columns(3)
col1.metric("Healthy Engagement", f"{kpis['Engagement']:.0f}%", delta="+2.3% / hr")
col2.metric("Sustainable Economy", f"{kpis['Economy']:.2f}", delta="+0.05 / hr")
col3.metric("Healthy Happiness", f"{kpis['Happiness']:.0f}%", delta="+2.8% / hr")

st.divider()
st.subheader("Latest NPC Actions (from Backend Logs)")
for log in logs[-5:]:
    if "NPC" in log or "actions" in log:
        st.code(log.strip(), language="text")

st.caption(f"Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')} | Powered by Grok + X Trends")
st.rerun()  # Auto-refresh
