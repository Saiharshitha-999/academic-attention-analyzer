import streamlit as st
import pickle
import numpy as np

# Load ML model
model = pickle.load(open("model.pkl","rb"))

st.set_page_config(page_title="Academic Attention Analyzer", layout="centered")

# ---------- STYLE ----------
st.markdown("""
<style>

html, body {
    overflow: hidden;
}

.block-container{
    max-width:800px;
    padding-top:3rem;
}

/* Lavender container */
[data-testid="stVerticalBlock"] {
    background: linear-gradient(135deg,#E6E6FA,#D8BFD8);
    padding:40px;
    border-radius:20px;
    box-shadow:0px 10px 30px rgba(0,0,0,0.15);
}

.question{
    font-size:30px;
    font-weight:600;
}

div[data-baseweb="radio"] label{
    font-size:20px;
}

</style>
""", unsafe_allow_html=True)

# ---------- SESSION STATE ----------
if "page" not in st.session_state:
    st.session_state.page = "home"

if "step" not in st.session_state:
    st.session_state.step = 0

if "answers" not in st.session_state:
    st.session_state.answers = []

# ---------- QUESTIONS ----------
questions = [

("How strongly do your peers influence your academic performance?",
[
"I rarely feel influenced by peers",
"Occasionally I compare myself with others",
"Peer performance sometimes affects my confidence",
"I often feel pressured to match others",
"I constantly feel intense peer pressure"
]),

("How much academic expectation do you feel from your family?",
[
"My family encourages me without pressure",
"They expect good results but remain supportive",
"Moderate expectations to perform well",
"Strong expectations to achieve high scores",
"Constant pressure to excel academically"
]),

("How competitive is your academic environment?",
[
"Very relaxed environment",
"Mild competition among students",
"Balanced competition",
"Highly competitive environment",
"Extremely intense competition"
]),

("How often do you feel overwhelmed by academic responsibilities?",
[
"Almost never",
"Occasionally during exams",
"Sometimes during heavy workload",
"Frequently throughout the semester",
"Almost all the time"
]),

("How demanding is your current academic stage?",
[
"Very manageable",
"Slightly challenging",
"Moderately challenging",
"Quite demanding",
"Extremely demanding"
])

]

# ---------- HOME PAGE ----------
if st.session_state.page == "home":

    with st.container():

        st.title("🧠 Academic Attention Analyzer")

        st.write("""
This assessment analyzes how **academic stress affects attention and concentration**.

• Peer pressure  
• Family expectations  
• Academic competition  
• Stress levels  
• Academic stage
""")

        if st.button("Start Assessment"):
            st.session_state.page = "questions"
            st.session_state.step = 0
            st.session_state.answers = []
            st.rerun()

# ---------- QUESTIONS PAGE ----------
elif st.session_state.page == "questions":

    q_index = st.session_state.step
    question, options = questions[q_index]

    st.progress((q_index+1)/len(questions))
    st.caption(f"Question {q_index+1} of {len(questions)}")

    with st.container():

        st.markdown(f'<div class="question">{question}</div>', unsafe_allow_html=True)

        answer = st.radio(
            "Select the option that best describes you:",
            options,
            index=None
        )

        if st.button("Next"):

            if answer is None:
                st.warning("Please select an option before continuing.")
            else:
                st.session_state.answers.append(options.index(answer)+1)
                st.session_state.step += 1

                if st.session_state.step >= len(questions):
                    st.session_state.page = "result"

                st.rerun()

# ---------- RESULT PAGE ----------
elif st.session_state.page == "result":

    # Convert answers to model input
    features = np.array(st.session_state.answers).reshape(1,-1)

    # Get prediction from ML model
    prediction = model.predict(features)[0]

    st.title("📊 Attention Analysis Result")

    if prediction == 0:

        st.success("Low Risk Zone")

        st.markdown("### Suggestions")

        st.write("""
• Maintain your current study habits  
• Continue balancing academics and personal life  
• Follow consistent study routines
""")

    else:

        st.error("High Risk Zone")

        st.markdown("### Suggestions")

        st.write("""
• Reduce academic pressure  
• Talk with mentors or counselors  
• Practice relaxation or meditation  
• Focus on mental wellbeing
""")

    if st.button("Restart Assessment"):

        st.session_state.page = "home"
        st.session_state.step = 0
        st.session_state.answers = []
        st.rerun()