import streamlit as st
import pandas as pd
from questions import load_questions, Question
from quiz import Quiz


@st.cache_data
def load_cheat_sheet():
    """Loads the pronoun and verb ending cheat sheet from a CSV file."""
    try:
        # Correctly read the CSV, using the first row (index 0) as the header
        df = pd.read_csv("german_pronouns.csv", header=0)
        # Select and rename the relevant columns, now including Verb Ending
        df = df[['English', 'Nominative/Subject', 'Verb Ending']]
        df = df.rename(columns={
            'Nominative/Subject': 'German Pronoun',
            'Verb Ending': 'Present Tense Ending'
        })
        # Remove any empty rows
        df = df.dropna()
        return df
    except FileNotFoundError:
        # Return None if the file doesn't exist so the app doesn't crash
        return None


def initialize_session_state():
    """Initializes the session state for the application."""
    if 'quiz_state' not in st.session_state:
        st.session_state.quiz_state = 'setup'  # 'setup', 'in_progress', 'finished'
    if 'feedback' not in st.session_state:
        st.session_state.feedback = None
    if 'show_next_button' not in st.session_state:
        st.session_state.show_next_button = False
    # 'quiz' is no longer initialized here


def display_question(question: Question):
    """Displays the current question to the user."""
    st.subheader("Translate and conjugate the verb:")

    st.markdown("**English Sentence:**")
    with st.container(border=True):
        st.markdown(f"<p style='font-size: 1.5rem; margin-bottom: 0;'>{question.english_sentence}</p>",
                    unsafe_allow_html=True)

    st.markdown("**German Verb:**")
    with st.container(border=True):
        st.markdown(
            f"<p style='font-size: 1.5rem; font-family: monospace; margin-bottom: 0;'>{question.german_verb}</p>",
            unsafe_allow_html=True)


def check_user_answer(quiz: Quiz, user_answer: str):
    """Checks the user's answer and provides feedback."""
    is_correct = quiz.check_answer(user_answer)
    correct_answer = quiz.get_current_question().german_answer
    if is_correct:
        st.session_state.feedback = {
            "message": "🎉 **Correct!** Well done.",
            "is_correct": True
        }
    else:
        st.session_state.feedback = {
            "message": f"🤔 **Not quite.** The correct answer is: `{correct_answer}`",
            "is_correct": False
        }
    st.session_state.show_next_button = True


def display_feedback():
    """Displays feedback to the user after they submit an answer."""
    if st.session_state.feedback:
        if st.session_state.feedback["is_correct"]:
            st.success(st.session_state.feedback["message"])
        else:
            st.warning(st.session_state.feedback["message"])


def handle_next_question():
    """Callback function to reset state for the next question."""
    st.session_state.quiz.next_question()  # Advance to the next question
    st.session_state.feedback = None
    st.session_state.show_next_button = False
    st.session_state.user_answer_input = ""


def reset_quiz():
    """Resets the quiz by changing the state back to 'setup'."""
    st.session_state.quiz_state = 'setup'
    if 'quiz' in st.session_state:
        del st.session_state.quiz
    st.session_state.feedback = None
    st.session_state.show_next_button = False


def main():
    """Main function to run the Streamlit application."""
    st.set_page_config(page_title="German Verb Conjugator", layout="centered")
    st.title("🇩🇪 German Verb Conjugation Practice")

    # Load cheat sheet popover
    cheat_sheet_df = load_cheat_sheet()
    if cheat_sheet_df is not None:
        with st.popover("📚 Pronoun & Endings Cheat Sheet", use_container_width=True):
            st.dataframe(cheat_sheet_df, hide_index=True, use_container_width=True)

    initialize_session_state()

    # Load all questions once to get the count
    all_questions = load_questions("questions.txt")
    max_questions = len(all_questions)

    # --- State 1: Setup Screen ---
    if st.session_state.quiz_state == 'setup':
        st.header("Start a New Quiz")

        # Default to 20 questions or max, whichever is smaller
        default_num = min(20, max_questions)

        num_questions = st.number_input(
            f"How many questions would you like? (1 - {max_questions})",
            min_value=1,
            max_value=max_questions,
            value=default_num,
            step=1
        )

        if st.button("Start Quiz"):
            # Create the quiz with the selected number of questions
            st.session_state.quiz = Quiz(all_questions, num_questions=num_questions)
            st.session_state.quiz_state = 'in_progress'
            st.session_state.feedback = None
            st.session_state.show_next_button = False
            st.rerun()

    # --- State 2: Quiz in Progress ---
    elif st.session_state.quiz_state == 'in_progress':
        quiz = st.session_state.quiz

        if quiz.is_finished():
            st.session_state.quiz_state = 'finished'
            st.rerun()
        else:
            current_question = quiz.get_current_question()
            display_question(current_question)

            with st.form(key="answer_form"):
                user_answer = st.text_input(
                    "Your answer:",
                    key="user_answer_input",
                    placeholder="Type the full German sentence...",
                    disabled=st.session_state.show_next_button,
                    autocomplete="off"
                )
                submit_button = st.form_submit_button(
                    "Check Answer",
                    disabled=st.session_state.show_next_button
                )

                if submit_button and user_answer:
                    check_user_answer(quiz, user_answer)
                    st.rerun()

            display_feedback()

            if st.session_state.show_next_button:
                st.button("➡️ Next Question", on_click=handle_next_question)

    # --- State 3: Quiz Finished ---
    elif st.session_state.quiz_state == 'finished':
        quiz = st.session_state.quiz  # Get the completed quiz from state
        st.header("Quiz Complete!")
        score, total = quiz.get_score()
        percentage = (score / total * 100) if total > 0 else 0
        st.metric(label="Your Score", value=f"{score}/{total}", delta=f"{percentage:.1f}%")

        # The on_click callback handles resetting the state
        st.button("🔄 Practice Again", on_click=reset_quiz)


if __name__ == "__main__":
    main()
