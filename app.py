import streamlit as st
import google.generativeai as genai

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

# 3. Model Initialization (Modern Endpoint)
model = genai.GenerativeModel('gemini-3.5-flash')

# 4. Custom Premium Dark Theme Styles
st.markdown("""
<style>
:root {
   --bg-base: #0B0F19;
   --bg-surface: #1E293B;
   --rose: #F43F5E;
   --blue: #3B82F6;
   --emerald: #10B981;
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
   color: var(--emerald);
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

# 5. Global Navigation Header
st.markdown("""
<div class="header-bar">
   <div class="brand-title">🎓 ExamZen AI</div>
   <div class="status-badge">● AI Core Online</div>
</div>
""", unsafe_allow_html=True)

# 6. Set Up 4 Functional Tabs
tabs = st.tabs([
   "💬 Arya Mentor Chat",
   "🔍 Correctify AI Engine",
   "⚡ AI Flashcard Gen",
   "📅 Smart Study Planner"
])


# --- TAB 1: ARYA MENTOR CHAT ---
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


# --- TAB 2: CORRECTIFY AI ---
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


# --- TAB 3: AI FLASHCARD & QUIZ GENERATOR (NEW FEATURE) ---
with tabs[2]:
   st.markdown("<h3 style='color: #F1F5F9; margin-bottom: 4px;'>⚡ AI Flashcard & Quiz Builder</h3>", unsafe_allow_html=True)
   st.markdown("<p style='color: #94A3B8; margin-bottom: 20px;'>Turn any topic or syllabus chapter into an instant revision quiz.</p>", unsafe_allow_html=True)
   
   quiz_topic = st.text_input("Enter study topic or chapter:", placeholder="e.g., Photosynthesis Light Reactions, Quadratic Equations...")
   quiz_difficulty = st.select_slider("Select Quiz Difficulty Level:", options=["Beginner", "Intermediate", "Advanced"])
   
   if st.button("Generate Interactive Revision Kit", type="primary"):
       if not quiz_topic:
           st.warning("Please specify a topic to build flashcards.")
       else:
           with st.spinner("Formulating test modules..."):
               quiz_prompt = f"Create a set of 3 flashcards (Question and Answer) and 2 multiple-choice questions for the topic: '{quiz_topic}' at an '{quiz_difficulty}' academic difficulty level. Format it beautifully with clear titles."
               try:
                   quiz_response = model.generate_content(quiz_prompt)
                   st.markdown("<h4 style='color: #F1F5F9; margin-top: 20px;'>Your Personalized Study Kit:</h4>", unsafe_allow_html=True)
                   st.markdown(quiz_response.text)
               except Exception as api_err:
                   st.error(f"Failed to generate quiz: {api_err}")


# --- TAB 4: SMART STUDY PLANNER (NEW FEATURE) ---
with tabs[3]:
   st.markdown("<h3 style='color: #F1F5F9; margin-bottom: 4px;'>📅 Smart Study Route Planner</h3>", unsafe_allow_html=True)
   st.markdown("<p style='color: #94A3B8; margin-bottom: 20px;'>Tell the AI your time limits to generate a custom, realistic preparation itinerary.</p>", unsafe_allow_html=True)
   
   subject_name = st.text_input("What subject or exam are you prepping for?", placeholder="e.g., Final Term Physics, Calculus Midterm...")
   days_left = st.number_input("How many days do you have left to prepare?", min_value=1, max_value=60, value=7)
   hours_per_day = st.slider("How many hours can you commit each day?", min_value=1, max_value=12, value=3)
   
   if st.button("Generate Tactical Study Plan", type="primary"):
       if not subject_name:
           st.warning("Please provide a subject or exam target name.")
       else:
           with st.spinner("Structuring optimized timetable..."):
               planner_prompt = f"Design a highly realistic day-by-day study schedule for an upcoming '{subject_name}' exam. The student has exactly {days_left} days left, and can study for {hours_per_day} hours per day. Break down what areas they should focus on each day to avoid burnout."
               try:
                   planner_response = model.generate_content(planner_prompt)
                   st.markdown("<h4 style='color: #F1F5F9; margin-top: 20px;'>Your Strategic Blueprint:</h4>", unsafe_allow_html=True)
                   st.markdown(planner_response.text)
               except Exception as api_err:
                   st.error(f"Failed to assemble timeline: {api_err}")
