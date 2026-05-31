import streamlit as st
import google.generativeai as genai

# 1. Page Configuration (Launches app instantly into widescreen mode)
st.set_page_config(
   page_title="ExamZen",
   layout="wide",
   initial_sidebar_state="collapsed"
)

# 2. Configure Gemini API Key Safely
if "GEMINI_API_KEY" in st.secrets:
   genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
   st.error("Missing API Key! Please verify GEMINI_API_KEY inside your Streamlit Cloud secrets.")

# 3. Model Initialization
model = genai.GenerativeModel('gemini-1.5-flash')

# 4. Custom Dark Premium Theme Styles
st.markdown("""
<style>
:root {
   --bg-base: #0B0F19;
   --bg-surface: #1E293B;
   --rose: #F43F5E;
   --blue: #3B82F6;
   --text-primary: #F1F5F9;
   --text-secondary: #94A3B8;
   --radius-md: 12px;
}

html, body, [class*="css"] {
   font-family: 'Plus Jakarta Sans', sans-serif !important;
   color: var(--text-secondary) !important;
}

.stApp {
   background: var(--bg-base) !important;
}

/* Clear out Streamlit generic headers/footers */
header, [data-testid="collapsedControl"], .stDeployButton, footer, #MainMenu {
   display: none !important;
}

.block-container {
   padding: 1.5rem 1rem 3rem 1rem !important;
}

.header-bar {
   display: flex;
   justify-content: space-between;
   align-items: center;
   padding-bottom: 1.5rem;
   margin-bottom: 1.5rem;
   border-bottom: 1px solid #1E293B;
}
.brand-title {
   color: var(--text-primary);
   font-size: 26px;
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
</style>
""", unsafe_allow_html=True)

# 5. Global Branding Navigation Bar
st.markdown("""
<div class="header-bar">
   <div class="brand-title">🎓 ExamZen AI</div>
   <div class="status-badge">● AI Core Online</div>
</div>
""", unsafe_allow_html=True)

# 6. Streamlined Dynamic Navigation (Removed fake Hub/Review tabs entirely)
tabs = st.tabs(["💬 Arya Mentor Chat", "🔍 Correctify AI Engine"])


# --- TAB 1: ARYA MENTOR CHAT (Now your primary landing interface) ---
with tabs[0]:
   st.markdown("<h2 style='color: #F1F5F9; margin-bottom: 4px;'>Arya Core Mentorship</h2>", unsafe_allow_html=True)
   st.markdown("<p style='color: #94A3B8; margin-bottom: 24px;'>Ask complex questions about formulas, proofs, structures, or theorems across STEM subjects.</p>", unsafe_allow_html=True)
   
   if "chat_history" not in st.session_state:
       st.session_state.chat_history = []
       
   for msg in st.session_state.chat_history:
       with st.chat_message(msg["role"]):
           st.markdown(msg["content"])
           
   if user_query := st.chat_input("Ask Arya to unpack a concept..."):
       st.session_state.chat_history.append({"role": "user", "content": user_query})
       with st.chat_message("user"):
           st.markdown(user_query)
           
       try:
           with st.chat_message("assistant"):
               with st.spinner("Compiling structural insights..."):
                   response = model.generate_content(user_query)
                   st.markdown(response.text)
                   st.session_state.chat_history.append({"role": "assistant", "content": response.text})
       except Exception as api_err:
           st.error(f"Core Engine Error: {api_err}")
           
   st.write("")
   if st.button("Reset Chat Stream", key="reset_chat"):
       st.session_state.chat_history = []
       st.rerun()


# --- TAB 2: CORRECTIFY AI (Derivation Step Validator) ---
with tabs[1]:
   st.markdown("<h3 style='color: #F1F5F9; margin-bottom: 4px;'>Correctify AI Engine</h3>", unsafe_allow_html=True)
   st.markdown("<p style='color: #94A3B8; margin-bottom: 20px;'>Input math proofs or chemical mechanisms below to locate step-by-step logic gaps.</p>", unsafe_allow_html=True)
   
   problem_statement = st.text_area("1. Target Question or Formula:", placeholder="e.g., Solve the integration of x * ln(x) dx...")
   user_steps = st.text_area("2. Your Complete Working Workflow:", placeholder="Step 1: ...\nStep 2: ...", height=180)
   
   if st.button("Analyze Logic Breakdown", type="primary", use_container_width=True):
       if not problem_statement or not user_steps:
           st.warning("Both parameters are essential to execute an analysis report.")
       else:
           with st.spinner("Scanning data matrices for calculation errors..."):
               prompt = f"Analyze this problem and working steps for any logical or mathematical errors:\nProblem: {problem_statement}\nSteps: {user_steps}"
               try:
                   analysis_response = model.generate_content(prompt)
                   st.markdown("<h4 style='color: #F1F5F9; margin-top: 20px;'>Analysis Matrix Feedback:</h4>", unsafe_allow_html=True)
                   st.info(analysis_response.text)
               except Exception as api_err:
                   st.error(f"Parsing Failure: {api_err}")
!
