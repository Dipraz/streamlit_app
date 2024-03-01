import streamlit as st
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

    # Link the questionnaire to Streamlit
    if st.session_state.current_section_index < len(sections):
        section = sections[st.session_state.current_section_index]
        questions = section["questions"]

        # Show title of the section when starting the first question of the section
        if st.session_state.current_question_index == 0:
            st.write(f"**{section['name']}**")

        if st.session_state.current_question_index < len(questions):
            question = questions[st.session_state.current_question_index]

            # Display current question
            st.write(question["question"])

            # Display previous conversation (if any)
            for i, past_message in enumerate(chat_history):
                st.write(past_message["message"])  # Adjusted to display message directly

            # Custom UI/UX for the radio button
            options = ["1", "2", "3", "4", "5"]
            radio_style = """
                display: none;
            """

            col1, col2, col3, col4, col5 = st.columns(5)
            with col1:
                answer_1 = st.radio("1", options, style=radio_style, key="radio_1")
                st.write("1️⃣")
            with col2:
                answer_2 = st.radio("2", options, style=radio_style, key="radio_2")
                st.write("2️⃣")
            with col3:
                answer_3 = st.radio("3", options, style=radio_style, key="radio_3")
                st.write("3️⃣")
            with col4:
                answer_4 = st.radio("4", options, style=radio_style, key="radio_4")
                st.write("4️⃣")
            with col5:
                answer_5 = st.radio("5", options, style=radio_style, key="radio_5")
                st.write("5️⃣")

            # Submit button and answer validation
            if st.button("Submit", key=f'submit_button_{st.session_state.current_section_index}-{st.session_state.current_question_index}'):
                try:
                    answers = [int(answer_1), int(answer_2), int(answer_3), int(answer_4), int(answer_5)]
                    for val in answers:
                        if 1 <= val <= 5:
                            # Save the answer
                            if section["name"] not in st.session_state.answers:
                                st.session_state.answers[section["name"]] = []
                            st.session_state.answers[section["name"]].append(val)

                            # Store message in chat history
                            chat_history.append({"is_user": True, "message": f"You answered: {val}"})

                            # Move to the next question
                            st.session_state.current_question_index += 1
                            if st.session_state.current_question_index >= len(questions):
                                st.session_state.current_section_index += 1
                                st.session_state.current_question_index = 0
                            st.experimental_rerun()
                        else:
                            st.error("Please enter valid integers between 1 and 5.")
                            break
                except ValueError:
                    st.error("Please enter valid integers between 1 and 5.")

    # When all the questions are answered, display the average score for each section
    else:
        st.header("Average Results per Category")
        averages = {}
        for category, answers in st.session_state.answers.items():
            avg_score = sum(answers) / len(answers)
            averages[category] = avg_score
            st.write(f"- {category}: {avg_score:.2f}")

        # Save results into a JSON file
        with open("results.json", "w") as outfile:
            json.dump(averages, outfile)

if __name__ == "__main__":
    main()
