
import os
import json
from groq import Groq
from dotenv import load_dotenv

#Loading the Groq API key from the .env file
load_dotenv()

API_KEY = os.environ.get("GROQ_API_KEY")
if not API_KEY:
    # Fallback for environments where .env might not be loaded (e.g., some Streamlit cloud setups)
    try:
        import streamlit as st
        API_KEY = st.secrets.get("GROQ_API_KEY") 
    except ImportError:
        pass
    
    if not API_KEY:
        raise ValueError("GROQ_API_KEY not found. Please set it in your .env file, environment variables, or Streamlit secrets.")


client = Groq(api_key=API_KEY)
# Using the recommended replacement model from Groq
MODEL = 'mixtral-8x7b-32768'

def get_llm_response_with_tools(messages_history, tools_schemas=None):
    """
    Gets response from LLM, potentially using tools.
    messages_history: List of message objects.
    tools_schemas: List of tool schemas for the LLM to use.
    """
    try:
        params = {
            "messages": messages_history,
            "model": MODEL,
            "temperature": 0.7, # Can be a bit higher for more natural conversation
        }
        if tools_schemas:
            params["tools"] = tools_schemas
            params["tool_choice"] = "auto" # LLM decides whether to use a tool

        chat_completion = client.chat.completions.create(**params)
        print(f"LLM Response: {chat_completion.choices[0].message}")
        return chat_completion.choices[0].message # Return the whole message object
    
    except Exception as e:
        print(f"Error calling LLM: {e}")
        # Return an error structure that the agent can handle
        # Create a mock message object for error
        from groq.types.chat.chat_completion_message import ChatCompletionMessage, FunctionCall
        # For simplicity, returning a string error that the agent will wrap
        return f"LLM_ERROR: {str(e)}"
