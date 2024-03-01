import streamlit as st
from streamlit_chat import message
import json

# Load questions and categories from JSON file
def load_questions(filepath):
    with open(filepath, "r") as file:
        data = json.load(file)
    return data["Sections"]  # Assuming the questions are organized in 'Sections'

# Main app
def main():
    # Initialize session state variables if not already done
    if 'current_section_index' not in st.session_state:
        st.session_state.current_section_index = 0
        st.session_state.current_question_index = 0
        st.session_state.answers = {}

    sections = load_questions("questionnaire.json")

    # Check if there are more sections and questions
    if st.session_state.current_section_index < len(sections):
        section = sections[st.session_state.current_section_index]
        questions = section["questions"]
        
        if st.session_state.current_question_index < len(questions):
            question = questions[st.session_state.current_question_index]
            message( question["question"])
            
            # Wait for user input
            print(f'{st.session_state.current_section_index}-{st.session_state.current_question_index}')
            options = [1, 2, 3, 4, 5]
            answer = st.radio("Your answer:", options, key=f'{st.session_state.current_section_index}-{st.session_state.current_question_index}',  horizontal=True,
)
            
            if st.button("Submit", key=f'{st.session_state.current_section_index}-{st.session_state.current_question_index}'):
                try:
                    val = int(answer)
                    if 1 <= val <= 5:
                        # Save the answer
                        if section["name"] not in st.session_state.answers:
                            st.session_state.answers[section["name"]] = []
                        st.session_state.answers[section["name"]].append(val)
                        
                        # Move to the next question
                        st.session_state.current_question_index += 1
                        if st.session_state.current_question_index >= len(questions):
                            # Move to the next section
                            st.session_state.current_section_index += 1
                            st.session_state.current_question_index = 0
                        st.experimental_rerun()
                    else:
                        st.error("Please enter a valid integer between 1 and 5.")
                except ValueError:
                    st.error("Please enter a valid integer between 1 and 5.")
        else:
            # This should not happen, but it's a safeguard
            st.session_state.current_section_index += 1
            st.session_state.current_question_index = 0
            st.experimental_rerun()
    else:
        st.write("All questions answered.")
        # Calculate and display average results per category
        for category, answers in st.session_state.answers.items():
            avg_score = sum(answers) / len(answers)
            st.write(f"Average for {category}: {avg_score:.2f}")

# Run the app
if __name__ == "__main__":
    main()
