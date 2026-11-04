import streamlit as st

from database import save_progress, get_progress
from learning_plan import generate_study_plan
from quiz_manager import generate_quiz, evaluate_quiz


# Page configuration
st.set_page_config(
    page_title="AI Personalized Learning Coach",
    page_icon="🎓",
    layout="wide"
)

# Title
st.title("🎓 AI Personalized Learning Coach")
st.write("Your personal AI-powered learning assistant.")

st.sidebar.title("Navigation")

page = st.sidebar.radio(
    "Choose a Section",
    ["Dashboard", "Study Planner", "AI Quiz", "My Progress"]
)


# DASHBOARD
if page == "Dashboard":

    st.header("Welcome to Your Learning Dashboard")

    st.write("""
    Learn smarter with your personal AI learning assistant.

    Features:
    - Personalized Study Plans
    - AI Generated Quizzes
    - Automatic Quiz Evaluation
    - Learning Progress Tracking
    """)


# STUDY PLANNER
elif page == "Study Planner":

    st.header("📚 AI Personalized Study Planner")

    with st.form("study_form"):

        name = st.text_input("Student Name")
        subject = st.text_input("Enter Subject")

        level = st.selectbox(
            "Your Learning Level",
            ["Beginner", "Intermediate", "Advanced"]
        )

        hours = st.selectbox(
            "Daily Study Hours",
            [1, 2, 3, 4, 5, 6]
        )

        goal = st.text_input("Your Learning Goal")

        submit = st.form_submit_button("Generate Study Plan")

    if submit:

        if name and subject and goal:

            with st.spinner("AI is creating your study plan..."):

                plan = generate_study_plan(
                    name, subject, level, hours, goal
                )

            st.subheader("Your Personalized Study Plan")
            st.write(plan)

        else:
            st.warning("Please fill in all the details.")


# AI QUIZ
elif page == "AI Quiz":

    st.header("📝 AI Quiz Generator")

    with st.form("quiz_form"):

        name = st.text_input("Student Name")
        topic = st.text_input("Enter Topic")

        level = st.selectbox(
            "Difficulty Level",
            ["Beginner", "Intermediate", "Advanced"]
        )

        num = st.selectbox(
            "Number of Questions",
            [5, 10]
        )

        generate = st.form_submit_button("Generate Quiz")

    if generate:

        if name and topic:

            with st.spinner("Generating your quiz..."):

                questions = generate_quiz(topic, level, num)

            if questions:

                st.session_state.questions = questions
                st.session_state.student_name = name
                st.session_state.topic = topic
                st.session_state.submitted = False

            else:
                st.error("Quiz generation failed. Please try again.")

        else:
            st.warning("Enter your name and topic.")

    if "questions" in st.session_state:

        questions = st.session_state.questions

        if not st.session_state.submitted:

            with st.form("answer_form"):

                answers = {}

                for i, q in enumerate(questions):

                    st.write(f"**Q{i+1}. {q['question']}**")

                    answers[i] = st.radio(
                        "Select your answer:",
                        q["options"],
                        key=f"answer_{i}"
                    )

                check = st.form_submit_button("Submit Answers")

            if check:

                score, total, results = evaluate_quiz(
                    questions, answers
                )

                save_progress(
                    st.session_state.student_name,
                    st.session_state.topic,
                    score,
                    total
                )

                st.session_state.score = score
                st.session_state.total = total
                st.session_state.results = results
                st.session_state.submitted = True

                st.rerun()

        else:

            st.success(
                f"Your Score: {st.session_state.score}/"
                f"{st.session_state.total}"
            )

            for result in st.session_state.results:

                st.write(result["question"])

                if result["is_correct"]:
                    st.success("Correct answer!")

                else:
                    st.error(
                        "Correct answer: "
                        + result["correct_answer"]
                    )

            if st.button("Take Another Quiz"):
                del st.session_state.questions
                st.session_state.submitted = False
                st.rerun()


# MY PROGRESS
elif page == "My Progress":

    st.header("📊 My Learning Progress")

    student = st.text_input("Enter your Student Name")

    if st.button("View Progress"):

        if student:

            data = get_progress(student)

            if data:

                for row in data:

                    st.write(f"Topic: {row[2]}")
                    st.write(f"Score: {row[3]}/{row[4]}")

                    st.progress(row[3] / row[4])

                    st.divider()

            else:
                st.info("No progress records found.")

        else:
            st.warning("Please enter your name.")


# Footer
st.divider()

st.caption("Developed by Videesha | AI Personalized Learning Coach")