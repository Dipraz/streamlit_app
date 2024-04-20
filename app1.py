import streamlit as st
from groq import Groq
import os
import time

from dotenv import load_dotenv

load_dotenv()

def icon(emoji: str):
    """Shows an emoji as a Notion-style page icon."""
    st.write(
        f'<span style="font-size: 78px; line-height: 1">{emoji}</span>',
        unsafe_allow_html=True,
    )

def initialize_session_state():
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "selected_model" not in st.session_state:
        st.session_state.selected_model = None

def load_groq_api_key():
    return os.environ.get('GROQ_API_KEY')

def display_chat_history():
    for message in st.session_state.messages:
        avatar = '' if message["role"] == "assistant" else '‍'
        with st.chat_message(message["role"], avatar=avatar):
            st.markdown(message["content"])

def generate_chat_responses(chat_completion):
    """Yield chat response content from the Groq API response."""
    for chunk in chat_completion:
        if chunk.choices[0].delta.content:
            yield chunk.choices[0].delta.content

def main():
    st.set_page_config(page_icon="", layout="wide", page_title="Groq Goes Brrrrrrrr...")

    icon("️")
    st.subheader("Groq Chat Streamlit App", divider="rainbow", anchor=False)

    initialize_session_state()
    client = Groq(api_key=load_groq_api_key())

    models = {
        "gemma-7b-it": {"name": "Gemma-7b-it", "tokens": 8192, "developer": "Google"},
        "llama2-70b-4096": {"name": "LLaMA2-70b-chat", "tokens": 4096, "developer": "Meta"},
        "llama3-70b-8192": {"name": "LLaMA3-70b-8192", "tokens": 8192, "developer": "Meta"},
        "llama3-8b-8192": {"name": "LLaMA3-8b-8192", "tokens": 8192, "developer": "Meta"},
        "mixtral-8x7b-32768": {"name": "Mixtral-8x7b-Instruct-v0.1", "tokens": 32768, "developer": "Mistral"},
    }

    col1, col2 = st.columns(2)

    with col1:
        model_option = st.selectbox(
            "Choose a model:",
            options=list(models.keys()),
            format_func=lambda x: models[x]["name"],
            index=4
        )

    if st.session_state.selected_model != model_option:
        st.session_state.messages = []
        st.session_state.selected_model = model_option

    max_tokens_range = models[model_option]["tokens"]

    with col2:
        max_tokens = st.slider(
            "Max Tokens:",
            min_value=512,
            max_value=max_tokens_range,
            value=min(32768, max_tokens_range),
            step=512,
            help=f"Adjust the maximum number of tokens (words) for the model's response. Max for selected model: {max_tokens_range}"
        )

    display_chat_history()

    try:
        if prompt := st.chat_input("Enter your prompt here..."):
            st.session_state.messages.append({"role": "user", "content": prompt})

            with st.chat_message("user", avatar='‍'):
                st.markdown(prompt)

            chat_completion = client.chat.completions.create(
                model=model_option,
                messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages],
                max_tokens=max_tokens,
                stream=False
            )
            full_response = chat_completion.choices[0].message.content

            with st.chat_message("assistant", avatar=""):
                st.write(full_response)
                for chunk in generate_chat_responses(chat_completion):
                    st.text(chunk)

            for i in range(1, len(full_response) // 100 + 1):
                st.write(full_response[i * 100: (i + 1) * 100])
                time.sleep(0.1)

    except Exception as e:
        st.error(e, icon="")
        full_response = None

if __name__ == "__main__":
    main()
