import streamlit as st
from streamlit_chat import message
import json

# Set page configuration
st.set_page_config(initial_sidebar_state="collapsed")

# Load questions and categories from JSON file
def load_questions(filepath):
    with open(filepath, "r") as file:
        data = json.load(file)
    return data["Sections"]

def main():
    # Load questions
    sections = load_questions("questionnaire.json")

    # Initialize session state variables
    if 'current_section_index' not in st.session_state:
        st.session_state.current_section_index = 0
        st.session_state.current_question_index = 0
        st.session_state.answers = {}
    if 'results_id' not in st.session_state:  # Initialize ID counter
        st.session_state.results_id = 0
    if 'js_selected_answer' not in st.session_state:
        st.session_state.js_selected_answer = None  # Initialize js_selected_answer

    st.title("Knowledge Management SECI Processes Questionnaire")

    # JavaScript function to update session state
    st.markdown(
        """
        <script>
            function setSelectedAnswer(selectedValue) {
                window.st.session_state.js_selected_answer = selectedValue;
            }
        </script>
        """,
        unsafe_allow_html=True
    )

    # Display sections and questions in a chat-like format
    chat_history = []  # Store chat messages for visual clarity

    if st.session_state.current_section_index < len(sections):
        section = sections[st.session_state.current_section_index]
        questions = section["questions"]

        # Display section title (when starting the first question)
        if st.session_state.current_question_index == 0:
            message(f"**{section['name']}**", is_user=False)

        if st.session_state.current_question_index < len(questions):
            question = questions[st.session_state.current_question_index]

            # Display current question
            message(question["question"], is_user=False)

            # Display previous conversation (if any)
            for past_message in chat_history:
                message(**past_message)

            # Get user input with custom radio buttons
            options = ["1", "2", "3", "4", "5"]
            answer_labels = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣"]

            col1, col2, col3, col4, col5 = st.columns(5)

            with col1:
                st.markdown(
                    f"""<div class="custom-radio" onclick="setSelectedAnswer('{options[0]}')">
                        <input type="radio" id="radio_1" name="answer" value="{options[0]}">
                        <label for="radio_1">{answer_labels[0]}</label>
                    </div>""",
                    unsafe_allow_html=True,
                )
            with col2:
                st.markdown(
                    f"""<div class="custom-radio" onclick="setSelectedAnswer('{options[1]}')">
                        <input type="radio" id="radio_2" name="answer" value="{options[1]}">
                        <label for="radio_2">{answer_labels[1]}</label>
                    </div>""",
                    unsafe_allow_html=True,
                )
            with col3:
                st.markdown(
                    f"""<div class="custom-radio" onclick="setSelectedAnswer('{options[2]}')">
                        <input type="radio" id="radio_3" name="answer" value="{options[2]}">
                        <label for="radio_3">{answer_labels[2]}</label>
                    </div>""",
                    unsafe_allow_html=True,
                )
            with col4:
                st.markdown(
                    f"""<div class="custom-radio" onclick="setSelectedAnswer('{options[3]}')">
                        <input type="radio" id="radio_4" name="answer" value="{options[3]}">
                        <label for="radio_4">{answer_labels[3]}</label>
                    </div>""",
                    unsafe_allow_html=True,
                )
            with col5:
                st.markdown(
                    f"""<div class="custom-radio" onclick="setSelectedAnswer('{options[4]}')">
                        <input type="radio" id="radio_5" name="answer" value="{options[4]}">
                        <label for="radio_5">{answer_labels[4]}</label>
                    </div>""",
                    unsafe_allow_html=True,
                )

            # Store user answers
            if st.button("Submit"):
                selected_answer = st.session_state.js_selected_answer
                if selected_answer:
                    answers = [selected_answer] * 5  # Create a placeholder list
                    if section["name"] not in st.session_state.answers:
                        st.session_state.answers[section["name"]] = []
                    st.session_state.answers[section["name"]].append(answers)

                    # Move to the next question or section
                    st.session_state.current_question_index += 1
                    if st.session_state.current_question_index >= len(questions):
                        st.session_state.current_section_index += 1
                        st.session_state.current_question_index = 0

                    # Clear previous chat history
                    chat_history.clear()

                    # Rerun the app to display next question or section
                    st.experimental_rerun()
    else:
        st.header("Average Results per Category")
        if not st.session_state.answers:
            st.write("No answers recorded yet.")
        else:
            results = {}
            for category, answer_lists in st.session_state.answers.items():
                scores_by_category = zip(*answer_lists)
                avg_scores = [sum(scores) / len(scores) for scores in scores_by_category]
                results[category] = avg_scores 

            # Display results 
            for category, scores in results.items():
                st.write(f"- {category}: {scores}") 

        # Save results into a JSON file
        results_data = []
        with open("results.json", "r+") as outfile:
            try:
                results_data = json.load(outfile)
            except json.JSONDecodeError:
                pass  

        results_data.append({
            "id": st.session_state.results_id,
            "result": results
        })
        st.session_state.results_id += 1

        with open("results.json", "w") as outfile:
            json.dump(results_data, outfile) 

if __name__ == "__main__":
    main()
