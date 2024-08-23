import streamlit as st
import os
import asyncio
from dotenv import load_dotenv
from agent import WeatherAgent

load_dotenv(".env")

st.set_page_config(page_title="My Webpage", page_icon=":tada:", layout="wide")

# Your Streamlit code here
st.subheader("Welcome to Weather forecast :wave:")
st.title("A weather forecasting app")
st.write("A way to get infromation on weather of a city or region easily")

user_input = st.text_input(
    label="Enter your region:",  # Label for the text input
    value="",                    # Default value
    max_chars=100,               # Maximum number of characters allowed
    placeholder="Type here...",  # Placeholder text
)

async def climate(region):
    # Initialize the weather agent with your LLM model and OpenAI API key
    api_key = os.getenv('OPENAI_API_KEY')
    os.environ["OPENAI_API_KEY"] = api_key
    
    agent = WeatherAgent(api_key=api_key)
    jawaban = await agent.run(region=region)
    return jawaban
    

# Create a button to process the input
if st.button("Run Agent"):
    if user_input:
        try:
            # Call the function from agent.py with the user input
            result = asyncio.run(climate(region=user_input))
            
            # Display the result
            st.write("Agent Output:")
            st.write(result)
        except Exception as e:
            st.error(f"An error occurred: {e}")
    else:
        st.warning("Please enter a value before running the agent.")