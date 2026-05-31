import streamlit as st
import google.generativeai as genai
import pandas as pd
import numpy as np

# 1. Page Configuration
st.set_page_config(
   page_title="ExamZen",
   layout="wide",
   initial_sidebar_state="collapsed"
)

# 2. Configure Gemini API Key
if "GEMINI_API_KEY" in st.secrets:
   genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
   st.error("Missing API Key! Please verify GEMINI_API_KEY inside your Streamlit Cloud secrets.")

# 3. Model Initialization (Clean, Standard Format)
model = genai.GenerativeModel('gemini-3.5-flash')

# 4. Custom UI Theme Variables & Global Styles
st.markdown("""
<style>
:root {
   --bg-base: #0B0F19;
   --bg-surface: #1E293B;
   --rose: #F43F5E;
   --blue: #3B82F6;
   --grad-brand: linear-gradient(135deg, #3B82F6 0%, #6366F1 100%);
   --text-primary: #F1F5F9;
   --text-secondary: #94A3B8;
   --text-muted: #64748B;
   --radius-md: 12px;
}

html, body, [class*="css"] {
   font-family: 'Plus Jakarta Sans', sans-serif !important;
   color: var(--text-secondary) !important;
}

.stApp {
   background: var(--bg-base) !important;
}

header, [data-testid="collapsedControl"], .stDeployButton, footer, #MainMenu {
   display: none !important;
}

.block-container {
   padding: 1rem 1rem 3rem 1rem !important;
}

.header-bar {
   display: flex;
   justify-content: space-between;
   align-items: center;
   padding-bottom: 1.5rem;
   margin-bottom: 1rem;
   border-bottom: 1px solid #1E293B;
}
.brand-title {
   color: var(--text-primary);
   font-size: 24px;
   font-weight: 700;
   display: flex;
   align-items: center;
   gap: 8px;
}
.status-badge {
   background-color: rgba(16, 185, 129, 0.1);
   color: #10B981;
   padding: 6px 14px;
   border-radius: 30px;
   font-size: 13px;
   font-weight: 600;
}

.dashboard-card {
   background-color: var(--bg-surface);
   padding: 1.25rem;
   border-radius: var(--radius-md);
   border: 1px solid #334155;
   margin-bottom: 1rem;
}
.card-title {
   color: var(--text-muted);
   font-size: 14px;
   text-transform: uppercase;
   font-weight: 600;
   letter-spacing: 0.5px;
}
.card-value {
   color: var(--text-primary);
   font-size: 28px;
   font-weight: 700;
   margin-top: 5px;
}
</style>
""", unsafe_allow_html=True)

# 5. Global Navigation Header
st.markdown("""
<div class="header-bar">
   <div class="brand-title">🎓 ExamZen</div>
   <div class="status-badge">● AI Core Online</div>
</div>
""", unsafe_allow_html=True)

# 6. Navigation Tabs
tabs = st.tabs(["Hub", "Mentor Chat", "Correctify AI", "Review"])

# --- TAB 1: HUB ---
with tabs[0]:
   st.markdown("<h3 style='color: #F1F5F9; margin-bottom: 20px;'>ExamZen Core Hub</h3>", unsafe_allow_html=True)
   
   col1, col2, col3 = st.columns(3)
   with col1:
       st.markdown('<div class="dashboard-card"><div class="card-title">🔥 Current Study Streak</div><div class="card-value">12 Days</div></div>', unsafe_allow_html=True)
   with col2:
       st.markdown('<div class="dashboard-card"><div class="card-title">🎯 Solutions Scanned</div><div class="card-value">47 Problems</div></div>', unsafe_allow_html=True)
   with col3:
       st.markdown('<div class="dashboard-card"><div class="card-title">⚡ Conceptual Accuracy</div><div class="card-value">84.2%</div></div>', unsafe_allow_html=True)

   st.markdown("<h4 style='color: #F1F5F9; margin-top: 15px;'>Recent Core Tasks</h4>", unsafe_allow_html=True)
   st.info("💡 Tip: Use the Mentor Chat tab to break down complex formulas.")
   
   st.checkbox("Review Organic Chemistry reaction mechanisms", value=True)
   st.checkbox("Analyze calculus derivation errors in Correctify AI", value=False)
   st.checkbox("Complete Mock Physics Assessment Set 3", value=False)


# --- TAB 2: MENTOR CHAT ---
with tabs[1]:
   st.markdown("<h2 style='color: #F1F5F9; margin-bottom: 4px;'>Arya Core Mentorship</h2>", unsafe_allow_html=True)
   st.markdown("<p style='color: #94A3B8; margin-bottom: 24px;'>Ask questions about formulas across Physics, Chemistry, Math, and Biology.</p>", unsafe_allow_html=True)
   
   if "chat_history" not in st.session_state:
       st.session_state.chat_history = []
       
   for msg in st.session_state.chat_history:
       with st.chat_message(msg["role"]):
           st.markdown(msg["content"])
           
   if user_query := st.chat_input("Ask Arya to explain a complex topic..."):
       st.session_state.chat_history.append({"role": "user", "content": user_query})
       with st.chat_message("user"):
           st.markdown(user_query)
           
       try:
           with st.chat_message("assistant"):
               with st.spinner("Compiling insights..."):
                   response = model.generate_content(user_query)
                   st.markdown(response.text)
                   st.session_state.chat_history.append({"role": "assistant", "content": response.text})
       except Exception as api_err:
           st.error(f"Execution Exception encountered: {api_err}")
           
   st.write("")
   if st.button("Reset Conversation Matrix", key="reset_chat"):
       st.session_state.chat_history = []
       st.rerun()


# --- TAB 3: CORRECTIFY AI ---
with tabs[2]:
   st.markdown("<h3 style='color: #F1F5F9; margin-bottom: 4px;'>Correctify AI Engine</h3>", unsafe_allow_html=True)
   st.markdown("<p style='color: #94A3B8; margin-bottom: 20px;'>Submit problem steps here to parse mistakes.</p>", unsafe_allow_html=True)
   
   problem_statement = st.text_area("1. Paste the Question:", placeholder="e.g., Integrate x*ln(x) dx...")
   user_steps = st.text_area("2. Paste your Working:", placeholder="Step 1: ...\nStep 2: ...", height=200)
   
   if st.button("Analyze Derivation Flow", type="primary", use_container_width=True):
       if not problem_statement or not user_steps:
           st.warning("Please fill out both boxes.")
       else:
           with st.spinner("Scanning logic matrices for errors..."):
               prompt = f"Analyze the following problem and working steps for errors.\nProblem: {problem_statement}\nSteps: {user_steps}"
               try:
                   analysis_response = model.generate_content(prompt)
                   st.markdown("<h4 style='color: #F1F5F9; margin-top: 20px;'>Report:</h4>", unsafe_allow_html=True)
                   st.info(analysis_response.text)
               except Exception as api_err:
                   st.error(f"Error: {api_err}")


# --- TAB 4: REVIEW ---
with tabs[3]:
   st.markdown("<h3 style='color: #F1F5F9; margin-bottom: 4px;'>Performance Analytical Review</h3>", unsafe_allow_html=True)
   
   chart_data = pd.DataFrame(
       np.random.randint(65, 98, size=(10, 3)),
       columns=['Physics', 'Chemistry', 'Math']
   )
   
   col_graph, col_list = st.columns([2, 1])
   
   with col_graph:
       st.markdown("<b style='color: #F1F5F9;'>Accuracy Timeline</b>", unsafe_allow_html=True)
       st.line_chart(chart_data)
       
   with col_list:
       st.markdown("<b style='color: #F1F5F9;'>🚨 Flagged Concepts</b>", unsafe_allow_html=True)
       st.markdown("""
       <div class="dashboard-card" style="border-left: 4px solid var(--rose);">
           <span style="color: #F1F5F9; font-weight:600;">Integration by Parts</span>
       </div>
       <div class="dashboard-card" style="border-left: 4px solid var(--rose);">
           <span style="color: #F1F5F9; font-weight:600;">Le Chatelier's Principle</span>
       </div>
       """, unsafe_allow_html=True)
