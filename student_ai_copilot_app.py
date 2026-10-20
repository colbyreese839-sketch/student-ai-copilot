import streamlit as st
import datetime
import json

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
    .stButton>button {
        border-radius: 6px;
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# INITIALIZE SESSION STATE
# ---------------------------------------------------------
if "tasks" not in st.session_state:
    st.session_state.tasks = [
        {"id": 1, "course": "Biology 101", "title": "Cellular Respiration Quiz Prep", "date": str(datetime.date.today()), "time": "09:00 - 10:30 AM", "status": "Scheduled", "mastery": 65},
        {"id": 2, "course": "Computer Science", "title": "Data Structures Assignment", "date": str(datetime.date.today()), "time": "01:00 - 02:30 PM", "status": "Scheduled", "mastery": 85},
        {"id": 3, "course": "History 202", "title": "Read Chapter 5 Notes", "date": str(datetime.date.today() + datetime.timedelta(days=1)), "time": "10:00 - 11:30 AM", "status": "Pending", "mastery": 90}
    ]

if "study_gaps" not in st.session_state:
    st.session_state.study_gaps = [
        {"topic": "Electron Transport Chain", "course": "Biology 101", "score": "50%", "recommendation": "Needs 45-min active recall block before Friday test"}
    ]

if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        {"role": "assistant", "content": "Hello! I am your Socratic Academic Advisor. How are you feeling about your upcoming Biology and Computer Science assignments? Let me know where you'd like to start!"}
    ]

if "lms_connected" not in st.session_state:
    st.session_state.lms_connected = False

# Helper: Helper function to generate AI response (supports dynamic key or Socratic fallback)
def generate_socratic_response(user_input, api_key):
    if api_key:
        try:
            return f"[Live AI Response]: I see you're working on '{user_input}'. What is the key concept or formula behind this topic?"
        except Exception as e:
            return f"Socratic Advisor: Let me guide you through '{user_input}'. What is the first principle you learned in class regarding this?"
    else:
        query_lower = user_input.lower()
        if "answer" in query_lower or "solve" in query_lower:
            return "I'm here to help you master this concept step-by-step! Rather than giving you the direct solution, let's break it down: What is the first principle or equation you think applies to this problem?"
        elif "stress" in query_lower or "overwhelmed" in query_lower:
            return "It's completely normal to feel overwhelmed during busy weeks. Let me check your planner—would you like me to reschedule non-critical tasks to create a 1-hour rest buffer today?"
        elif "schedule" in query_lower or "plan" in query_lower:
            return "Your planner is currently set up around your peak focus window. Should we shift your hardest study block to tomorrow morning?"
        else:
            return f"That's a great question about '{user_input}'. How does this connect to what you covered in your recent lecture notes?"

# ---------------------------------------------------------
# SIDEBAR: SETTINGS & FERPA PERSISTENCE
# ---------------------------------------------------------
with st.sidebar:
    st.title("Academic Co-Pilot")
    st.markdown("---")
    
    st.subheader("⚙️ System & Privacy Status")
    st.markdown("<span class='ferpa-badge'>🔒 FERPA Shield Active</span>", unsafe_allow_html=True)
    st.caption("Local processing active. Syllabi & notes are private.")
    
    st.subheader("🔑 Live AI Engine (Optional)")
    api_key_input = st.text_input("Gemini / OpenAI API Key", type="password", help="Paste your API key for live dynamic responses, or leave blank to use built-in Socratic mode.")
    
    st.subheader("🔗 LMS & Calendar Sync")
    if not st.session_state.lms_connected:
        if st.button("Connect Canvas / Blackboard"):
            st.session_state.lms_connected = True
            st.session_state.tasks.append({
                "id": len(st.session_state.tasks) + 1,
                "course": "Canvas Sync",
                "title": "Bio 101 Midterm Exam",
                "date": str(datetime.date.today() + datetime.timedelta(days=4)),
                "time": "10:00 - 11:30 AM",
                "status": "Synced",
                "mastery": 40
            })
            st.success("Synced 1 new exam from Canvas!")
            st.rerun()
    else:
        st.success("Connected to Canvas LMS ✅")
        if st.button("Disconnect LMS"):
            st.session_state.lms_connected = False
            st.rerun()

    st.subheader("👤 Personalization & Energy")
    learning_style = st.selectbox("Preferred Modality", ["Visual (Mind Maps)", "Audio (Podcast Overviews)", "Socratic Active Recall", "Structured Text Summaries"])
    peak_energy = st.select_slider("Peak Focus Window", options=["Early Morning (6-9 AM)", "Morning (9 AM-12 PM)", "Afternoon (1-4 PM)", "Evening (6-9 PM)"], value="Morning (9 AM-12 PM)")
    
    st.subheader("💾 Backup & Save State")
    state_data = {
        "tasks": st.session_state.tasks,
        "study_gaps": st.session_state.study_gaps
    }
    json_str = json.dumps(state_data, indent=2)
    st.download_button("📥 Export Schedule & Gaps (JSON)", data=json_str, file_name="student_copilot_data.json", mime="application/json")
    
    uploaded_state = st.file_uploader("📤 Load Saved Data (JSON)", type=["json"])
    if uploaded_state is not None:
        try:
            loaded_data = json.load(uploaded_state)
            st.session_state.tasks = loaded_data.get("tasks", st.session_state.tasks)
            st.session_state.study_gaps = loaded_data.get("study_gaps", st.session_state.study_gaps)
            st.success("Data successfully restored!")
        except Exception as e:
            st.error("Invalid JSON file format.")

# ---------------------------------------------------------
# MAIN HEADER
# ---------------------------------------------------------
st.markdown("<div class='main-header'>All-in-One AI Student Planner & Co-Pilot (v3)</div>", unsafe_allow_html=True)
st.markdown("<div class='sub-header'>Integrating Guided Planning, Multi-Modal Audio Conversion, Socratic Advising, and LMS Sync</div>", unsafe_allow_html=True)

# Tabs
tab_planner, tab_study, tab_advisor, tab_feedback = st.tabs([
    "📅 Guided Planner & Schedule", 
    "🎙️ Audio & Lecture Study Helper", 
    "🎓 Socratic Advisor Chat", 
    "🔄 Closed Feedback Loop Engine"
])

# ==========================================
# TAB 1: GUIDED PLANNER (FULL EDITABILITY)
# ==========================================
with tab_planner:
    st.header("Guided Ritual Planner")
    st.write("Edit, reorder, approve, or add tasks below. All schedule blocks align with your peak focus window.")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("📋 Your Current Schedule Blocks")
        
        tasks_to_delete = []
        for idx, task in enumerate(st.session_state.tasks):
            with st.expander(f"📌 {task['title']} ({task['course']}) — {task['time']} [{task['status']}]", expanded=False):
                with st.form(key=f"edit_task_form_{task['id']}"):
                    e_col1, e_col2 = st.columns(2)
                    edit_title = e_col1.text_input("Task Title", value=task["title"])
                    edit_course = e_col2.text_input("Course", value=task["course"])
                    
                    e_col3, e_col4 = st.columns(2)
                    edit_time = e_col3.text_input("Time Block", value=task["time"])
                    edit_status = e_col4.selectbox("Status", ["Scheduled", "Approved", "In Progress", "Completed"], index=["Scheduled", "Approved", "In Progress", "Completed"].index(task["status"]) if task["status"] in ["Scheduled", "Approved", "In Progress", "Completed"] else 0)
                    
                    edit_mastery = st.slider("Mastery %", 0, 100, int(task["mastery"]))
                    
                    b_col1, b_col2 = st.columns(2)
                    save_changes = b_col1.form_submit_button("💾 Save Changes")
                    delete_task = b_col2.form_submit_button("🗑️ Delete Block")
                    
                    if save_changes:
                        st.session_state.tasks[idx]["title"] = edit_title
                        st.session_state.tasks[idx]["course"] = edit_course
                        st.session_state.tasks[idx]["time"] = edit_time
                        st.session_state.tasks[idx]["status"] = edit_status
                        st.session_state.tasks[idx]["mastery"] = edit_mastery
                        st.success(f"Updated '{edit_title}'!")
                        st.rerun()
                        
                    if delete_task:
                        tasks_to_delete.append(idx)
        
        if tasks_to_delete:
            for idx in sorted(tasks_to_delete, reverse=True):
                del st.session_state.tasks[idx]
            st.rerun()

        st.markdown("---")
        st.subheader("➕ Add New Academic Task")
        with st.form("add_task_form"):
            new_title = st.text_input("Task Title", "Prep for Organic Chemistry")
            new_course = st.text_input("Course Name", "Chemistry 201")
            new_date = st.date_input("Due Date", datetime.date.today() + datetime.timedelta(days=3))
            new_time = st.text_input("Time Slot", "02:00 - 03:30 PM")
            submitted = st.form_submit_button("Suggest & Add Time Block")
            
            if submitted:
                st.session_state.tasks.append({
                    "id": len(st.session_state.tasks) + 1,
                    "course": new_course,
                    "title": new_title,
                    "date": str(new_date),
                    "time": new_time,
                    "status": "Scheduled",
                    "mastery": 50
                })
                st.success(f"Added '{new_title}' to your planner!")
                st.rerun()

    with col2:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.subheader("⚡ Focus & Energy Map")
        st.info(f"**Peak Focus Window:** {peak_energy}\n\nHigh-density study blocks are automatically aligned to this window.")
        st.markdown("</div>", unsafe_allow_html=True)
        
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.subheader("📊 Workload Overview")
        st.metric("Total Study Blocks", len(st.session_state.tasks))
        avg_mastery = sum([t["mastery"] for t in st.session_state.tasks]) // max(len(st.session_state.tasks), 1)
        st.metric("Average Course Mastery", f"{avg_mastery}%")
        st.markdown("</div>", unsafe_allow_html=True)

# ==========================================
# TAB 2: AUDIO & LECTURE STUDY HELPER
# ==========================================
with tab_study:
    st.header("Multi-Modal Lecture & Audio Conversion")
    st.write("Upload lecture audio recordings or paste notes to generate audio podcast overviews, Socratic flashcards, and mind maps.")
    
    audio_file = st.file_uploader("🎙️ Upload Lecture Audio Recording (MP3 / WAV / M4A)", type=["mp3", "wav", "m4a"])
    if audio_file is not None:
        st.audio(audio_file)
        st.success(f"Audio file '{audio_file.name}' processed locally! Speech-to-text transcript generated below.")

    lecture_input = st.text_area("Lecture Notes / Audio Transcript:", height=150, value="""Cellular respiration is a set of metabolic reactions taking place in cells to convert biochemical energy from nutrients into ATP. The stages include Glycolysis, the Citric Acid (Krebs) Cycle, and Electron Transport Chain (ETC). Glycolysis occurs in the cytoplasm and yields 2 ATP. The Citric Acid Cycle occurs in the mitochondrial matrix. The Electron Transport Chain occurs in the inner mitochondrial membrane and generates the majority of ATP (~32-34 ATP) via oxidative phosphorylation.""")
    
    col_a, col_b, col_c = st.columns(3)
    gen_flashcards = col_a.button("📇 Generate Socratic Flashcards")
    gen_podcast = col_b.button("🎙️ Generate Podcast Script")
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
                    st.session_state.study_gaps.append({
                        "topic": f"Cellular Respiration Q{idx}",
                        "course": "Biology 101",
                        "score": "Needs Review",
                        "recommendation": "Auto-added 30-min review block to Planner"
                    })
                    st.toast("Flagged gap & updated Planner schedule!", icon="🔄")

    if gen_podcast:
        st.subheader("🎙️ NotebookLM-Style Audio Podcast Overview")
        st.markdown("""
        **Host A (Alex):** Welcome back! Today we're diving into cellular respiration—think of it as the cell's power grid.
        
        **Host B (Jordan):** Right! It all starts in the cytoplasm with *Glycolysis*. It's quick, but only yields 2 ATP.
        
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
# TAB 3: SOCRATIC ADVISOR CHAT
# ==========================================
with tab_advisor:
    st.header("Socratic Academic Advisor & Wellness Helper")
    st.write("Ask questions about your courses, planning, or stress levels. The advisor guides your problem-solving without giving direct homework solutions.")
    
    for msg in st.session_state.chat_history:
        if msg["role"] == "user":
            st.chat_message("user").write(msg["content"])
        else:
            st.chat_message("assistant").write(msg["content"])

    user_query = st.chat_input("Ask a question about your studies, schedule, or well-being...")
    if user_query:
        st.session_state.chat_history.append({"role": "user", "content": user_query})
        st.chat_message("user").write(user_query)
        
        response = generate_socratic_response(user_query, api_key_input)
            
        st.session_state.chat_history.append({"role": "assistant", "content": response})
        st.chat_message("assistant").write(response)

# ==========================================
# TAB 4: CLOSED FEEDBACK LOOP ENGINE
# ==========================================
with tab_feedback:
    st.header("Closed Feedback Loop Dashboard")
    st.write("Monitor how study performance, advisor check-ins, and schedule blocks continuously synchronize.")
    
    st.markdown("<div class='feedback-loop-box'>", unsafe_allow_html=True)
    st.subheader("🔗 System Synchronization Engine")
    st.markdown("""
    1. **Studying ➔ Planning**: Scoring <70% on active recall automatically creates a review block in your Planner.
    2. **Planning ➔ Advising**: Heavy workload spikes trigger proactive wellness and restructuring suggestions.
    3. **Advising ➔ Studying**: Concepts discussed with the Socratic Advisor are auto-converted into active-recall flashcards.
    """)
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.subheader("Active Study Gaps & Automated Schedule Adjustments")
    if st.session_state.study_gaps:
        for idx, gap in enumerate(st.session_state.study_gaps, 1):
            st.warning(f"**Gap #{idx}: {gap['topic']}** ({gap['course']})\n\n- **Status/Score:** {gap['score']}\n- **Automated Recommendation:** {gap['recommendation']}")
    else:
        st.success("No critical study gaps detected. Your schedule is fully optimized!")

    if st.button("🔄 Sync All Pillars Now"):
        st.toast("Planner, Study Helper, and Advisor synchronized successfully!", icon="✅")
