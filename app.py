import streamlit as st
import os

st.set_page_config(page_title="Agentic AI Interface", layout="wide")

# Sidebar-Header
st.sidebar.title("🧠 Agentic AI Navigation")

# --- Tool Explorer ---
st.sidebar.markdown("### 🔧 Tool Explorer")
tool_page = st.sidebar.radio("Wähle ein Tool:", [
    "Vision Tools", 
    "Text Tools"
], key="tools")

# --- Output Viewer ---
st.sidebar.markdown("---")
st.sidebar.markdown("### 📤 Output Viewer")
output_page = st.sidebar.radio("Ausgabe anzeigen:", [
    "Übersicht"
], key="output")

# --- Analysis Viewer ---
st.sidebar.markdown("---")
st.sidebar.markdown("### 📈 Analysis Viewer")
analysis_page = st.sidebar.radio("Analyse anzeigen:", [
    "Übersicht"
], key="analysis")

# --- Documentation ---
st.sidebar.markdown("---")
st.sidebar.markdown("### 📄 Dokumentation")
doc_page = st.sidebar.radio("Dokumentation:", [
    "Übersicht"
], key="docs")

# Hauptanzeige (Starttext)
st.title("👋 Willkommen im Agentic AI Interface")
st.markdown("Navigiere über die linke Sidebar durch Tools, Analysen und Dokumentation.")
