import streamlit as st
import google.generativeai as genai
import os

# --- Configuration ---
st.set_page_config(page_title="My AI Coach", page_icon="🏋️‍♂️", layout="centered")

# --- API Key Setup ---
# For local testing, you can temporarily hardcode your key here like: API_KEY = "your_key"
# However, using environment variables is much safer.
API_KEY = os.environ.get("GEMINI_API_KEY")

if not API_KEY:
    st.warning("⚠️ Please set your GEMINI_API_KEY as an environment variable to continue.")
    st.stop()

genai.configure(api_key=API_KEY)

# --- Coach Persona (System Instruction) ---
# This is where we define how the AI coach behaves.
COACH_SYSTEM_PROMPT = """
You are a high-performance lifestyle and academic coach. 
Your goal is to help the user achieve peak performance in their studies (specifically rigorous competitive entrance exams) 
while maintaining a healthy lifestyle, including fitness, personal grooming, and nutrition. 
When giving dietary advice, prioritize high-protein vegetarian options. 
When giving study advice, focus on practical time management, intensive study sprints, and long-term structured roadmaps.
Be direct, motivating, factual, and highly practical. Do not use overly flowery language.
"""

# Initialize the Gemini model with our specific coaching instructions
model = genai.GenerativeModel(
    model_name="gemini-3.5-flash",
    system_instruction=COACH_SYSTEM_PROMPT
)

# --- Session State Management ---
# This keeps track of the chat history so the AI remembers the conversation
if "messages" not in st.session_state:
    st.session_state.messages = []
if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])

# --- UI Layout ---
st.title("🤖 Peak Performance AI Coach")
st.markdown("Your personal guide for balancing intense academics, fitness routines, and overall self-improvement.")
st.divider()

# Display previous chat messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# --- User Input ---
if prompt := st.chat_input("Ask your coach for a study plan, workout, or advice..."):
    
    # 1. Show user message in the UI
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # 2. Save user message to session state
    st.session_state.messages.append({"role": "user", "content": prompt})

    # 3. Get AI response and display it
    with st.chat_message("assistant"):
        try:
            response = st.session_state.chat_session.send_message(prompt)
            st.markdown(response.text)
            # Save AI response to session state
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"An error occurred: {e}")
