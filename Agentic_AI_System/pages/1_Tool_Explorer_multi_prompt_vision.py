import streamlit as st

from agents.multi_prompt_vision_agent import MultiPromptVisionAgent

st.set_page_config(page_title="Multi Prompt Vision", layout="wide")

st.title("🖼️ Multi-Prompt Vision Analyzer")

st.markdown("Gib eine oder mehrere Bild-URLs ein (eine URL pro Zeile).")

urls_input = st.text_area("Bild-URLs", "")
start = st.button("Analyse starten")

if start and urls_input:
    urls = [u.strip() for u in urls_input.splitlines() if u.strip()]
    if urls:
        agent = MultiPromptVisionAgent()
        results = agent.analyze_batch(urls)
        for res in results:
            st.subheader(res["image_url"])
            st.json(res["merged_output"])
    else:
        st.warning("Bitte mindestens eine gültige URL eingeben.")
