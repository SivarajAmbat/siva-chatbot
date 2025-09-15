import streamlit as st
import google.generativeai as genai

# Show title and description.
st.title("💬 Chatbot")
st.write(
    "This is a simple chatbot that uses Google's Gemini model to generate responses. "
    "To use this app, you need to provide a Google Gemini API key, which you can get [here](https://aistudio.google.com/app/u/1/apikey). "
)

# Ask user for their Gemini API key
gemini_api_key = st.text_input("Google Gemini API Key", type="password")
if not gemini_api_key:
    st.info("Please add your Gemini API key to continue.", icon="🗝️")
else:
    # Configure Gemini
    genai.configure(api_key=gemini_api_key)

    # Create a session state variable to store the chat messages. This ensures that the
    # messages persist across reruns.
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display the existing chat messages via `st.chat_message`.
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Create a chat input field to allow the user to enter a message. This will display
    # automatically at the bottom of the page.
    if prompt := st.chat_input("Ask anything"):

        # Store and display the current prompt.
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Generate response using Gemini
        model = genai.GenerativeModel("gemini-2.5-flash-nano")
        response = model.generate_content(
            [m["content"] for m in st.session_state.messages]
        )

        reply = response.text if response and response.text else "⚠️ No response from Gemini."

        # Display response
        with st.chat_message("assistant"):
            st.markdown(reply)

        st.session_state.messages.append({"role": "assistant", "content": response})
