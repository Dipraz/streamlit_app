import streamlit as st
from streamlit_chat import message
import json
import pandas as pd

# Load questions and categories from JSON file
def load_questions(filepath):
    with open(filepath, "r") as file:
        data = json.load(file)
    return data["Sections"]

# Main app
def main():
    # Initialize session state variables if not already done
    if 'current_section_index' not in st.session_state:
        st.session_state.current_section_index = 0
        st.session_state.current_question_index = 0
        st.session_state.answers = {}

    sections = load_questions("questionnaire.json")

    # CSS for custom radio button styling
    st.markdown("""
    <style>
    div.stRadio > div[role="radiogroup"] > label {
        font-size: 18px; 
        margin-right: 20px;
        background-color: #F0F0F0; 
        border: 2px solid #007BFF; 
        padding: 8px 15px;
        border-radius: 5px; 
    }
    </style>
    """, unsafe_allow_html=True)

    # Check if there are more sections and questions
    if st.session_state.current_section_index < len(sections):
        section = sections[st.session_state.current_section_index]
        questions = section["questions"]
         
        # Display section title (when starting the first question of the section)
        st.title(section["name"])

        if st.session_state.current_question_index < len(questions):
            question = questions[st.session_state.current_question_index]
            message(question["question"])

            # Wait for user input
            options = [1, 2, 3, 4, 5]
            answer = st.radio("Your answer:", options, 
                              key=f'{st.session_state.current_section_index}-{st.session_state.current_question_index}', 
                              horizontal=True)

            # Generate a unique key for the "Submit" button
            submit_button_key = f'submit-{st.session_state.current_section_index}-{st.session_state.current_question_index}'

            if st.button("Submit", key=submit_button_key):
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
        st.header("Results")

        # Calculate and display average results per category
        results = {}
        for category, answers in st.session_state.answers.items():
            avg_score = sum(answers) / len(answers)
            results[category] = avg_score

        # Display results in a table
        if st.session_state.answers:
            df = pd.DataFrame(results.items(), columns=['Category', 'Average Score'])
            st.table(df)
        else:
            st.write("No answers recorded yet.")

        # Save results into a JSON file
        with open("results.json", "w") as outfile:
            json.dump(results, outfile)

# Run the app
if __name__ == "__main__":
    main()
