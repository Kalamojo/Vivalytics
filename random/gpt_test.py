import os
import openai
import streamlit as st
#openai.api_key = os.getenv("OPENAI_API_KEY")
openai.api_key_path = "api_key.txt"

# Define a function to generate a response based on the user input
def get_response(user_input):
    # Add your logic here to generate a response based on the user input
  completion = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
      {"role": "user", "content": user_input}
    ]
  )

  return completion.choices[0].message["content"]



# Define the Streamlit app
def app():
    # Set the app title
    st.title("Chatbot App")
    
    # Get the user input
    user_input = st.text_input("You:", "")
    
    # Generate a response based on the user input
    response = get_response(user_input)
    
    # Display the response
    st.text_area("Chatbot:", value=response, height=100)
    
# Run the Streamlit app
if __name__ == "__main__":
    app()