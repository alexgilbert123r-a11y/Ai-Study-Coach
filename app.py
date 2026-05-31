import streamlit as st
import google.generativeai as genai
import pandas as pd
import numpy as np

# 1. Page Configuration (Must be the absolute first Streamlit command)
st.set_page_config(
   page_title="ExamZen",
   layout="wide",
   initial_sidebar_state="collapsed"
)

# 2. Configure Gemini API Key Safely
if "GEMINI_API_KEY" in st.secrets:
   genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
   st.error("Missing API Key! Please verify GEMINI_API_KEY inside your Streamlit Cloud secrets configuration panel.")

# FIX: Added 'models/' prefix to fully qualify the path and clear the 400 error
model = genai.GenerativeModel('models/gemini-1.5-flash-001')

# 3. Inject Your Custom UI Theme Variables & Global Styles
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
   --radius-lg: 16px;
}

/* APP BASE RESET */
html, body, [class*="css"] {
   font-family: 'Plus Jakarta Sans', sans-serif !important;
   color: var(--text-secondary) !important;
}

.stApp {
   background: var(--bg-base) !important;
}

/* HIDE STREAMLIT BRANDING AND NAVIGATION FOOTERS */
header, [data-testid="collapsedControl"], .stDeployButton, footer, #MainMenu {
   display: none !important;
}

/* APP WINDOW WIDTH LOCK */
.block-container {
   padding: 1rem 1rem 3rem 1rem !important;
}

/* Custom Component Layout Styles */
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

/* Metrics and Dashboard Cards */
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

# 4. Global Navigation Header Elements
st.markdown("""
<div class="header-bar">
   <div class="brand-title">🎓 ExamZen</div>
   <div class="status-badge">● AI Core Online</div>
</div>
""", unsafe_allow_html=True)

# 5. Initialize App Structure Navigation Tabs
tabs = st.tabs(["Hub", "Mentor Chat", "Correctify AI", "Review"])

# --- TAB 1: HUB (Dashboard Overview) ---
with tabs[0]:
   st.markdown("<h3 style='color: #F1F5F9; margin-bottom: 20px;'>ExamZen Core Hub</h3>", unsafe_allow_html=True)
   
   col1, col2, col3 = st.columns(3)
   with col1:
       st.markdown("""
       <div class="dashboard-card">
           <div class="card-title">🔥 Current Study Streak</div>
           <div class="card-value">12 Days</div>
       </div>
       """, unsafe_allow_html=True)
   with col2:
       st.markdown("""
       <div class="dashboard-card">
           <div class="card-title">🎯 Solutions Scanned</div>
           <div class="card-value">47 Problems</div>
       </div>
       """, unsafe_allow_html=True)
   with col3:
       st.markdown("""
       <div class="dashboard-card">
           <div class="card-title">⚡ Conceptual Accuracy</div>
           <div class="card-value">84.2%</div>
       </div>
       """, unsafe_allow_html=True)

   st.markdown("<h4 style='color: #F1F5F9; margin-top: 15px;'>Recent Core Tasks</h4>", unsafe_allow_html=True)
   st.info("💡 Tip: Use the **Mentor Chat** tab to instantly break down any complex formulas or theorems you find confusing.")
   
   st.checkbox("Review Organic Chemistry reaction mechanisms", value=True)
   st.checkbox("Analyze calculus derivation errors in Correctify AI", value=False)
   st.checkbox("Complete Mock Physics Assessment Set 3", value=False)


# --- TAB 2: MENTOR CHAT (Interactive AI Chat) ---
with tabs[1]:
   st.markdown("<h2 style='color: #F1F5F9; margin-bottom: 4px;'>Arya Core Mentorship</h2>", unsafe_allow_html=True)
   st.markdown("<p style='color: #94A3B8; margin-bottom: 24px;'>Ask questions about formulas, mechanisms, or theorems across Physics, Chemistry, Math, and Biology.</p>", unsafe_allow_html=True)
   
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


# --- TAB 3: CORRECTIFY AI (Derivation Error Checker) ---
with tabs[2]:
   st.markdown("<h3 style='color: #F1F5F9; margin-bottom: 4px;'>Correctify AI Engine</h3>", unsafe_allow_html=True)
   st.markdown("<p style='color: #94A3B8; margin-bottom: 20px;'>Submit problem steps here to parse runtime logical flow errors, calculation slips, or derivation mistakes.</p>", unsafe_allow_html=True)
   
   problem_statement = st.text_area("1. Paste the Question / Problem Statement:", placeholder="e.g., Integrate x*ln(x) dx...")
   user_steps = st.text_area("2. Paste your Step-by-Step Working / Derivation:", placeholder="Step 1: ...\nStep 2: ...", height=200)
   
   if st.button("Analyze Derivation Flow", type="primary", use_container_width=True):
       if not problem_statement or not user_steps:
           st.warning("Please fill out both the problem statement and your derivation steps to execute the analysis.")
       else:
           with st.spinner("Scanning logic matrices for errors..."):
               prompt = f"""
               You are an elite academic evaluator. Analyze the following problem and user-provided working steps for any errors.
               
               Problem Statement:
               {problem_statement}
               
               User's Steps:
               {user_steps}
               
               Provide a clear, formatted breakdown highlighting where any mistake occurs and how to fix it.
               """
               try:
                   analysis_response = model.generate_content(prompt)
                   st.markdown("<h4 style='color: #F1F5F9; margin-top: 20px;'>AI Correctify Analysis Report:</h4>", unsafe_allow_html=True)
                   st.info(analysis_response.text)
               except Exception as api_err:
                   st.error(f"Execution Exception encountered during parsing: {api_err}")


# --- TAB 4: REVIEW (Analytical Metrics & Flagged Items) ---
with tabs[3]:
   st.markdown("<h3 style='color: #F1F5F9; margin-bottom: 4px;'>Performance Analytical Review</h3>", unsafe_allow_html=True)
   st.markdown("<p style='color: #94A3B8; margin-bottom: 20px;'>Track performance metrics and concepts flagged for critical revision.</p>", unsafe_allow_html=True)
   
   chart_data = pd.DataFrame(
       np.random.randint(65, 98, size=(10, 3)),
       columns=['Physics Accuracy', 'Chemistry Accuracy', 'Math Accuracy']
   )
   
   col_graph, col_list = st.columns([2, 1])
   
   with col_graph:
       st.markdown("<b style='color: #F1F5F9;'>Accuracy Metrics Timeline (Last 10 Sessions)</b>", unsafe_allow_html=True)
       st.line_chart(chart_data)
       
   with col_list:
       st.markdown("<b style='color: #F1F5F9;'>🚨 Flagged Concept Focus</b>", unsafe_allow_html=True)
       st.markdown("""
       <div class="dashboard-card" style="border-left: 4px solid var(--rose);">
           <span style="color: #F1F5F9; font-weight:600;">Integration by Parts</span><br/>
           <span style="font-size:12px; color: var(--text-secondary);">Flagged 3 times via Correctify AI</span>
       </div>
       <div class="dashboard-card" style="border-left: 4px solid var(--rose);">
           <span style="color: #F1F5F9; font-weight:600;">Le Chatelier's Principle</span><br/>
           <span style="font-size:12px; color: var(--text-secondary);">Flagged 2 times via Mentor Chat</span>
       </div>
       <div class="dashboard-card" style="border-left: 4px solid var(--blue);">
           <span style="color: #F1F5F9; font-weight:600;">Rotational Kinematics</span><br/>
           <span style="font-size:12px; color: var(--text-secondary);">Marked for standard weekly review</span>
       </div>
       """, unsafe_allow_html=True)
