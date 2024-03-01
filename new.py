import streamlit as st
from streamlit_chat import message
import json

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

    st.title("Knowledge Management SECI Processes Questionnaire")

    # Display sections and questions in a chat-like format
    chat_history = []  # Store chat messages for visual clarity

    if st.session_state.current_section_index < len(sections):
        section = sections[st.session_state.current_section_index]
        questions = section["questions"]

        # Display section title
        message(f"**{section['name']}**", is_user=False)

        if st.session_state.current_question_index < len(questions):
            question = questions[st.session_state.current_question_index]

            # Display current question
            message(question["question"], is_user=False)

            # Display previous conversation (if any)
            for past_message in chat_history:
                message(**past_message)  # Unpack for correct formatting

            # Get user input (using radio buttons with default visuals)
            options = [1, 2, 3, 4, 5]
            answer = st.radio("Your answer:", options, key=f'radio_{st.session_state.current_section_index}-{st.session_state.current_question_index}', horizontal=True)

            if st.button("Submit", key=f'submit_button_{st.session_state.current_section_index}-{st.session_state.current_question_index}'):
                try:
                    val = int(answer)
                    if 1 <= val <= 5:
                        # Save the answer
                        if section["name"] not in st.session_state.answers:
                            st.session_state.answers[section["name"]] = []
                        st.session_state.answers[section["name"]].append(val)

                        # Store message in chat history
                        chat_history.append({"is_user": True, "message": f"You answered: {answer}"})

                        # Move to the next question
                        st.session_state.current_question_index += 1
                        if st.session_state.current_question_index >= len(questions):
                            st.session_state.current_section_index += 1
                            st.session_state.current_question_index = 0
                        st.experimental_rerun()
                    else:
                        st.error("Please enter a valid integer between 1 and 5.")
                except ValueError:
                    st.error("Please enter a valid integer between 1 and 5.")
    else:
        # Calculate and display average results per category
        st.header("Average Results per Category")
        for category, answers in st.session_state.answers.items():
            avg_score = sum(answers) / len(answers)
            st.write(f"- {category}: {avg_score:.2f}")

        # Save results into a JSON file
        with open("results.json", "w") as outfile:
            json.dump(st.session_state.answers, outfile)

if __name__ == "__main__":
    main()
