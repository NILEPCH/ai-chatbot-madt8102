import streamlit as st
import google.generativeai as genai

import streamlit as st

st.title("🐶 Dog Advisory chatbot app")
st.write(
    "Let's start conversation"
)

# Capture Gemini API Key
gemini_api_key = st.text_input("Gemini API Key: ", placeholder="Type your API Key here...", type="password")

#if st.button('Clear', type="primary"):
   # st.session_state.chat_history()

# Initialize the Gemini Model to None first
model = None

# Initialize the model only if the API key is provided
if gemini_api_key:
    try:
        # Configure Gemini with the provided API Key
        genai.configure(api_key=gemini_api_key)  # Use the gemini_api_key provided by the user
        model = genai.GenerativeModel("gemini-pro") 
        st.success("Gemini API Key successfully configured.")
    except Exception as e:
        st.error(f"An error occurred while setting up the Gemini model: {e}")

# Initialize session state for storing chat history
if "chat_history" not in st.session_state: 
    st.session_state.chat_history = []  # Initialize with an empty list

# Display previous chat history using st.chat_message (if available)
for role, message in st.session_state.chat_history: 
    st.chat_message(role).markdown(message)

# Capture user input and generate bot response
if user_input := st.chat_input("Type your message here..."): 
    # Store and display user message
    st.session_state.chat_history.append(("user", user_input)) 
    st.chat_message("user").markdown(user_input)

    # Ensure the model is initialized before using it
    if model is not None:
        try:
             # Personality prompt for the chatbot
            personality_prompt = (
            "Your name is 'Meow'. You are women who love dog and specialist about Dog. You are very polite, "
            "wise, and offer thoughtful and professional advice about dog. You are calm and "
            "always maintain a respectful tone."
             )

            # Combine the personality prompt with the user input
            full_input = f"{personality_prompt}\nUser: {user_input}\nAssistant:"

             # Generate a response using the model with the personality prompt included
            response = model.generate_content(full_input) 
            bot_response = response.text

             # Store and display the bot response
            st.session_state.chat_history.append(("assistant", bot_response))
            st.chat_message("assistant").markdown(bot_response) 

        except Exception as e:
              st.error(f"An error occurred while generating the response: {e}")
    else:
        st.warning("Please provide a valid Gemini API Key to start the conversation.")
