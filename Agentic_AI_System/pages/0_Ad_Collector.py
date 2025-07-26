import os
import streamlit as st
from datetime import date

from tools.ad_library.ad_search import search_ads
from agents.multi_prompt_vision_agent import MultiPromptVisionAgent
from tools.utils.screenshot import capture as capture_screenshot

st.set_page_config(page_title="Ad Collector", layout="wide")

st.title("🔍 Ad Collector & Analyzer")

query = st.text_input("Suchbegriffe")
region = st.text_input("Region")
platform = st.selectbox("Plattform", ["Meta", "Google", "Beide"])
num_ads = st.number_input("Anzahl Ads", min_value=1, max_value=10, value=3)
start_date = st.date_input("Startdatum", date.today())
end_date = st.date_input("Enddatum", date.today())

if st.button("Start"):
    timeframe = f"{start_date} - {end_date}"
    ads = search_ads(query, region, platform, int(num_ads), timeframe)
    agent = MultiPromptVisionAgent()

    snap_dir = os.path.join("outputs", "snapshots")
    os.makedirs(snap_dir, exist_ok=True)

    for ad in ads:
        st.subheader(f"{ad['platform']} Ad {ad['id']}")
        st.write(f"Snapshot URL: {ad['snapshot_url']}")

        img_path = ad['image_path']
        if os.path.exists(img_path):
            st.image(img_path, width=300)
        else:
            st.write(f"Bild nicht gefunden: {img_path}")

        screenshot_path = os.path.join(snap_dir, f"{ad['id']}.png")
        try:
            capture_screenshot(ad['snapshot_url'], screenshot_path)
            st.image(screenshot_path, caption="Snapshot", width=300)
            analyze_path = screenshot_path
        except Exception as e:
            st.warning(f"Screenshot fehlgeschlagen: {e}")
            analyze_path = img_path

        result = agent.analyze(analyze_path)
        st.json(result['merged_output'])

