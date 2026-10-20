import streamlit as st
import datetime

# Page configuration
st.set_page_config(
    page_title="AI Academic Co-Pilot & Student Planner",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.2rem;
        font-weight: 700;
        color: #1E3A8A;
        margin-bottom: 0px;
    }
    .sub-header {
        font-size: 1.1rem;
        color: #4B5563;
        margin-bottom: 20px;
    }
    .ferpa-badge {
        background-color: #DEF7EC;
        color: #03543F;
        padding: 6px 12px;
        border-radius: 16px;
        font-weight: 600;
        font-size: 0.85rem;
        display: inline-block;
        margin-bottom: 15px;
    }
    .card {
        background-color: #F9FAFB;
        border: 1px solid #E5E7EB;
        padding: 18px;
        border-radius: 10px;
        margin-bottom: 15px;
    }
    .feedback-loop-box {
        background-color: #EFF6FF;
        border-left: 4px solid #3B82F6;
        padding: 15px;
        border-radius: 6px;
        margin-top: 10px;
        margin-bottom: 15px;
    }
</style>
""", unsafe_allow_html=True)

# Initialize Session State for Closed Feedback Loop
if "tasks" not in st.session_state:
    st.session_state.tasks = [
        {"id": 1, "course": "Biology 101", "title": "Cellular Respiration Quiz Prep", "date": datetime.date.today(), "time": "09:00 - 10:30 AM", "status": "Scheduled", "mastery": 65},
        {"id": 2, "course": "Computer Science", "title": "Data Structures Assignment", "date": datetime.date.today(), "time": "01:00 - 02:30 PM", "status": "Scheduled", "mastery": 85},
        {"id": 3, "course": "History 202", "title": "Read Chapter 5 Notes", "date": datetime.date.today() + datetime.timedelta(days=1), "time": "10:00 - 11:30 AM", "status": "Pending", "mastery": 90}
    ]

if "study_gaps" not in st.session_state:
    st.session_state.study_gaps = [
        {"topic": "Electron Transport Chain", "course": "Biology 101", "score": "50%", "recommendation": "Needs 45-min active recall block before Friday test"}
    ]

if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        {"role": "assistant", "content": "Hello! I am your Socratic Academic Advisor. How are you feeling about your upcoming Biology and Computer Science assignments? Let me know where you'd like to start!"}
    ]

# Sidebar Navigation & Settings
with st.sidebar:
    st.title("Academic Co-Pilot")
    st.markdown("---")
    
    st.subheader("⚙️ System Status")
    st.markdown("<span class='ferpa-badge'>🔒 FERPA Privacy Shield Active</span>", unsafe_allow_html=True)
    st.caption("Your syllabi, transcripts, and study notes are processed locally and never used to train public LLM models.")
    
    st.subheader("👤 Learning Preferences")
    learning_style = st.selectbox("Preferred Modality", ["Visual (Mind Maps)", "Audio (Podcast Overviews)", "Socratic Active Recall", "Structured Text Summaries"])
    peak_energy = st.select_slider("Biological Peak Focus Hours", options=["Early Morning (6-9 AM)", "Morning (9 AM-12 PM)", "Afternoon (1-4 PM)", "Evening (6-9 PM)"], value="Morning (9 AM-12 PM)")
    
    st.markdown("---")
    st.caption("Unified Architecture: Planning ↔ Studying ↔ Advising")

# Main Header
st.markdown("<div class='main-header'>All-in-One AI Student Planner & Co-Pilot</div>", unsafe_allow_html=True)
st.markdown("<div class='sub-header'>Integrating Guided Planning, Socratic Study Assets, and Academic Advising in a Unified Feedback Loop</div>", unsafe_allow_html=True)

# Tabs Navigation
tab_planner, tab_study, tab_advisor, tab_feedback = st.tabs([
    "📅 Guided Planner", 
    "📚 Multi-Modal Study Helper", 
    "🎓 Socratic Advisor", 
    "🔄 Closed Feedback Loop Engine"
])

# ==========================================
# TAB 1: GUIDED PLANNER
# ==========================================
with tab_planner:
    st.header("Guided Ritual Planner")
    st.write("Unlike black-box 'auto-pilot' schedulers, this guided ritual planner proposes optimal study blocks based on your energy levels while keeping **you** in control to avoid automation bias.")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Today's Schedule & Study Blocks")
        for task in st.session_state.tasks:
            with st.container():
                c1, c2, c3, c4 = st.columns([3, 2, 2, 2])
                c1.markdown(f"**{task['title']}**\n*{task['course']}*")
                c2.text(f"🕒 {task['time']}")
                c3.progress(task['mastery'] / 100, text=f"Mastery: {task['mastery']}%")
                if c4.button("Approve Block", key=f"app_{task['id']}"):
                    st.success(f"Approved time block for {task['title']}")
                    
        st.markdown("---")
        st.subheader("➕ Add New Academic Task")
        with st.form("add_task_form"):
            new_title = st.text_input("Task Title", "Prep for Chemistry Midterm")
            new_course = st.text_input("Course Name", "Chemistry 101")
            new_date = st.date_input("Due Date", datetime.date.today() + datetime.timedelta(days=3))
            submitted = st.form_submit_button("Suggest Optimal Time Block")
            if submitted:
                st.session_state.tasks.append({
                    "id": len(st.session_state.tasks) + 1,
                    "course": new_course,
                    "title": new_title,
                    "date": new_date,
                    "time": "03:00 - 04:30 PM",
                    "status": "Suggested",
                    "mastery": 50
                })
                st.success(f"AI Planner suggested a study block for '{new_title}' during your peak energy hours!")
                st.rerun()

    with col2:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.subheader("⚡ Energy & Focus Alignment")
        st.info(f"**Peak Focus Window:** {peak_energy}\n\nHigh-density study blocks (like Socratic active recall) are aligned to this window.")
        st.markdown("</div>", unsafe_allow_html=True)
        
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.subheader("💡 Context-Switch Guard")
        st.caption("Reduces the 23-minute focus recovery cost by embedding all study assets directly inside your schedule.")
        st.markdown("</div>", unsafe_allow_html=True)

# ==========================================
# TAB 2: MULTI-MODAL STUDY HELPER
# ==========================================
with tab_study:
    st.header("Multi-Modal Study Helper")
    st.write("Convert raw lecture recordings, transcripts, or notes into your preferred learning asset.")
    
    lecture_input = st.text_area("Paste Lecture Notes, Transcript, or Syllabus Content:", height=150, value="""Cellular respiration is a set of metabolic reactions taking place in cells to convert biochemical energy from nutrients into ATP. The stages include Glycolysis, the Citric Acid (Krebs) Cycle, and Electron Transport Chain (ETC). Glycolysis occurs in the cytoplasm and yields 2 ATP. The Citric Acid Cycle occurs in the mitochondrial matrix. The Electron Transport Chain occurs in the inner mitochondrial membrane and generates the majority of ATP (~32-34 ATP) via oxidative phosphorylation.""")
    
    col_a, col_b, col_c = st.columns(3)
    gen_flashcards = col_a.button("📇 Generate Socratic Flashcards")
    gen_podcast = col_b.button("🎙️ Generate Audio Overview Script")
    gen_mindmap = col_c.button("🗺️ Generate Visual Mind Map")
    
    if gen_flashcards:
        st.subheader("Generated Active-Recall Flashcards")
        cards = [
            {"q": "Where in the cell does Glycolysis occur, and what is its net ATP yield?", "a": "Occurs in the cytoplasm; yields a net of 2 ATP."},
            {"q": "Why is the Electron Transport Chain responsible for the majority of ATP synthesis?", "a": "It uses oxidative phosphorylation across the inner mitochondrial membrane to yield ~32-34 ATP."},
            {"q": "What is the key functional difference between Glycolysis and the Citric Acid Cycle location?", "a": "Glycolysis happens in cytoplasm; Citric Acid Cycle happens in the mitochondrial matrix."}
        ]
        for idx, card in enumerate(cards, 1):
            with st.expander(f"Flashcard {idx}: {card['q']}"):
                st.write(f"**Answer:** {card['a']}")
                col_yes, col_no = st.columns(2)
                if col_yes.button("Got it right", key=f"fc_right_{idx}"):
                    st.toast("Mastery updated (+10%)")
                if col_no.button("Needs review", key=f"fc_wrong_{idx}"):
                    st.session_state.study_gaps.append({"topic": f"Cellular Respiration Q{idx}", "course": "Biology 101", "score": "Needs Review", "recommendation": "Auto-added 30-min review to Planner"})
                    st.toast("Flagged gap & updated Planner schedule!", icon="🔄")

    if gen_podcast:
        st.subheader("🎙️ NotebookLM-Style Audio Overview Script")
        st.markdown("""
        **Host A (Alex):** Welcome back! Today we're diving into cellular respiration. Think of it as the cell's power grid.
        
        **Host B (Jordan):** Right, and it all starts in the cytoplasm with *Glycolysis*. It's quick, but only gives you 2 ATP.
        
        **Host A (Alex):** But the real heavy lifting happens in the mitochondria—specifically the Electron Transport Chain in the inner membrane, pumping out around 32 to 34 ATP!
        """)

    if gen_mindmap:
        st.subheader("🗺️ Visual Mind Map Structure")
        st.code("""
        [Cellular Respiration]
           ├── Glycolysis (Location: Cytoplasm | Yield: 2 ATP)
           ├── Citric Acid / Krebs Cycle (Location: Mitochondrial Matrix)
           └── Electron Transport Chain (Location: Inner Membrane | Yield: ~32-34 ATP)
        """, language="text")

# ==========================================
# TAB 3: SOCRATIC ADVISOR
# ==========================================
with tab_advisor:
    st.header("Socratic Academic Advisor")
    st.write("An AI co-pilot designed to guide your critical thinking and manage stress without generating direct homework answers.")
    
    # Display Chat History
    for msg in st.session_state.chat_history:
        if msg["role"] == "user":
            st.chat_message("user").write(msg["content"])
        else:
            st.chat_message("assistant").write(msg["content"])

    user_query = st.chat_input("Ask a question about your studies, schedule, or well-being...")
    if user_query:
        st.session_state.chat_history.append({"role": "user", "content": user_query})
        st.chat_message("user").write(user_query)
        
        # Socratic Response Logic
        if "answer" in user_query.lower() or "solve" in user_query.lower():
            response = "I'm here to help you master this concept step-by-step! Rather than giving you the direct solution, let's break it down: What is the first principle or equation you think applies to this problem?"
        elif "stress" in user_query.lower() or "overwhelmed" in user_query.lower():
            response = "It's completely normal to feel overwhelmed during busy weeks. Let me look at your planner—would you like me to reschedule non-critical tasks to create a 1-hour rest buffer today?"
        else:
            response = f"That's a great question about {user_query}. How does this connect to what you covered in your recent lecture notes?"
            
        st.session_state.chat_history.append({"role": "assistant", "content": response})
        st.chat_message("assistant").write(response)

# ==========================================
# TAB 4: CLOSED FEEDBACK LOOP ENGINE
# ==========================================
with tab_feedback:
    st.header("Closed Feedback Loop Engine")
    st.write("This dashboard demonstrates how learning performance automatically updates your planner and advisor in real time.")
    
    st.markdown("<div class='feedback-loop-box'>", unsafe_allow_html=True)
    st.subheader("🔗 How the Pillars Synchronize")
    st.markdown("""
    1. **Studying ➔ Planning**: When flashcards or quiz scores show a gap (<70%), the engine automatically inserts a review block into your Planner.
    2. **Planning ➔ Advising**: If your weekly schedule exceeds 30 study hours, the Socratic Advisor proactively offers workload rebalancing.
    3. **Advising ➔ Studying**: Concepts flagged during Socratic Q&A sessions are automatically converted into active recall cards.
    """)
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.subheader("Current Detected Study Gaps & Automated Interventions")
    if st.session_state.study_gaps:
        for idx, gap in enumerate(st.session_state.study_gaps, 1):
            st.warning(f"**Gap #{idx}: {gap['topic']}** ({gap['course']})\n\n- **Status/Score:** {gap['score']}\n- **Automated Recommendation:** {gap['recommendation']}")
    else:
        st.success("No critical study gaps detected. Your schedule is optimized!")

    if st.button("Sync All Pillars & Refresh Schedule"):
        st.toast("System synchronized across Planner, Study Helper, and Advisor!", icon="✅")
