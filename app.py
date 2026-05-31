import streamlit as st
import google.generativeai as genai
import pandas as pd
import json
import os
from datetime import datetime

# --- 1. App Configuration & Premium UI Setup ---
st.set_page_config(page_title="Apex AI Coach Pro", page_icon="📈", layout="wide")

# --- 2. API Key Management ---
API_KEY = os.environ.get("GEMINI_API_KEY")
if not API_KEY:
    st.error("🔒 **Enterprise Security Lock:** Please set your `GEMINI_API_KEY` as an environment variable to access the coaching engine.")
    st.stop()

genai.configure(api_key=API_KEY)

# --- 3. Premium Feature: Multi-Persona Engine ---
PERSONAS = {
    "The Taskmaster (Productivity & Academics)": """
        You are an elite, highly demanding academic and productivity coach. 
        Focus strictly on time-blocking, deep work protocols (like Pomodoro), and ruthless elimination of distractions. 
        Do not coddle the user. Use bullet points, bold text for emphasis, and actionable checklists.
    """,
    "The Biohacker (Nutrition & Fitness)": """
        You are an advanced sports nutritionist and biohacking coach. 
        Focus entirely on optimizing physical performance, sleep architecture, and macronutrient timing. 
        Prioritize high-protein, plant-based diets and evidence-based workout protocols (hypertrophy, VO2 max).
    """,
    "The Zen Mentor (Mindset & Burnout Recovery)": """
        You are a psychological resilience and mindset coach. 
        Your goal is to prevent burnout during intense study or work periods. 
        Focus on breathwork, cognitive reframing, stoic philosophy, and sustainable pacing. Speak calmly and empathetically.
    """
}

# --- 4. Persistent State & Database Simulation ---
if "messages" not in st.session_state:
    st.session_state.messages = []
if "metrics" not in st.session_state:
    # Simulating a database of user progress
    st.session_state.metrics = pd.DataFrame({
        "Date": pd.date_range(start="2024-05-24", periods=7),
        "Study Hours": [4, 5, 3, 6, 7, 5, 8],
        "Protein (g)": [120, 130, 110, 140, 135, 125, 150],
        "Sleep (hrs)": [7, 6.5, 8, 7.5, 6, 7, 8]
    }).set_index("Date")
if "current_model" not in st.session_state:
    st.session_state.current_model = None

# --- 5. Sidebar Dashboard (The "Expensive" Feel) ---
with st.sidebar:
    st.title("⚙️ Apex Control Center")
    
    st.markdown("### 🧬 Select Your Coach")
    selected_persona = st.selectbox("Current Active Module:", list(PERSONAS.keys()))
    
    # Initialize or update model if persona changes
    if st.session_state.get("last_persona") != selected_persona:
        model = genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            system_instruction=PERSONAS[selected_persona]
        )
        st.session_state.chat_session = model.start_chat(history=[])
        st.session_state.last_persona = selected_persona
        # Optional: clear chat when switching coaches to keep context clean
        # st.session_state.messages = [] 
        st.toast(f"Switched to: {selected_persona}", icon="🔄")

    st.divider()
    
    # KPI Tracking Feature
    st.markdown("### 📊 Daily KPI Tracker")
    col1, col2 = st.columns(2)
    with col1:
        st.metric(label="Study Target", value="8 hrs", delta="1.5 hrs", delta_color="normal")
    with col2:
        st.metric(label="Protein Intake", value="150g", delta="20g", delta_color="normal")
        
    st.divider()
    
    # Export Feature
    st.markdown("### 📥 Session Export")
    if len(st.session_state.messages) > 0:
        chat_transcript = "\n\n".join([f"{msg['role'].upper()}: {msg['content']}" for msg in st.session_state.messages])
        st.download_button(
            label="Download Action Plan",
            data=chat_transcript,
            file_name=f"Apex_Plan_{datetime.now().strftime('%Y%m%d')}.txt",
            mime="text/plain",
            use_container_width=True
        )

# --- 6. Main Content Area ---
# Using tabs to separate the Chat from the Analytics dashboard
tab1, tab2 = st.tabs(["💬 Coaching Console", "📈 Performance Analytics"])

with tab1:
    st.header(f"Active Session: {selected_persona.split('(')[0]}")
    
    # Display chat history
    for msg in st.session_state.messages:
        avatar = "🧑‍💻" if msg["role"] == "user" else "🤖"
        with st.chat_message(msg["role"], avatar=avatar):
            st.markdown(msg["content"])

    # Input handling
    if prompt := st.chat_input("Enter your blockages, questions, or updates..."):
        with st.chat_message("user", avatar="🧑‍💻"):
            st.markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})

        with st.chat_message("assistant", avatar="🤖"):
            try:
                with st.spinner("Analyzing protocol..."):
                    response = st.session_state.chat_session.send_message(prompt)
                    st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            except Exception as e:
                st.error(f"System Error: {e}")

with tab2:
    st.header("Weekly Performance Telemetry")
    st.markdown("Review your trailing 7-day data across key lifestyle and academic metrics.")
    
    # Render an interactive line chart based on our mock database
    st.line_chart(st.session_state.metrics, use_container_width=True)
    
    # Provide a data editor for the user to manually input today's stats
    st.markdown("### 📝 Log Today's Data")
    edited_df = st.data_editor(st.session_state.metrics, num_rows="dynamic", use_container_width=True)
    if st.button("Save Telemetry"):
        st.session_state.metrics = edited_df
        st.success("Database updated successfully.")
