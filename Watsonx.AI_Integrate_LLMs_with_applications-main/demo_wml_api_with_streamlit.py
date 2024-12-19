"""
author: Elena Lowery (Modified by [Your Name])

This code demonstrates how to interact with Large Language Models (LLMs) hosted on watsonx.ai.
Documentation: https://ibm.github.io/watson-machine-learning-sdk/foundation_models.html
You will need your IBM Cloud API key and a watsonx.ai project ID to access watsonx.ai.
This example showcases a basic question-and-answer (Q&A) functionality with improved prompt customization.
"""

# Prerequisite installations:
# pip install ibm-watson-machine-learning
# pip install streamlit
# pip install python-dotenv (if not using Anaconda)

# Import required libraries
import os
from dotenv import load_dotenv
import streamlit as st
from ibm_watson_machine_learning.foundation_models import Model
from ibm_watson_machine_learning.metanames import GenTextParamsMetaNames as GenParams
from ibm_watson_machine_learning.foundation_models.utils.enums import ModelTypes, DecodingMethods

# Constants
API_URL = "https://us-south.ml.cloud.ibm.com"
watsonx_project_id = ""
api_key = ""

def load_credentials():
    """
    Load API credentials from the .env file
    """
    load_dotenv()
    global api_key, watsonx_project_id
    api_key = os.getenv("API_KEY", "")
    watsonx_project_id = os.getenv("PROJECT_ID", "")
    if not api_key or not watsonx_project_id:
        raise ValueError("API Key and Project ID must be set in the .env file")

def create_model(model_type, max_tokens, min_tokens, decoding, stop_sequences):
    """
    Initialize the model with the provided parameters
    """
    params = {
        GenParams.MAX_NEW_TOKENS: max_tokens,
        GenParams.MIN_NEW_TOKENS: min_tokens,
        GenParams.DECODING_METHOD: decoding,
        GenParams.STOP_SEQUENCES: stop_sequences
    }
    return Model(
        model_id=model_type,
        params=params,
        credentials={
            "apikey": api_key,
            "url": API_URL
        },
        project_id=watsonx_project_id
    )

def build_prompt(question):
    """
    Construct the input prompt for the model
    """
    instruction = "Answer the following question concisely:"
    examples = (
        "\n\nQuestion: What is the capital of France?\nAnswer: Paris\n\n"
        "Question: Who wrote Hamlet?\nAnswer: William Shakespeare\n\n"
        "Question: What are the primary colors?\nAnswer: Red, blue, yellow\n\n"
        "Question: "
    )
    return f"{instruction}{examples}{question}\nAnswer:"

def main():
    """
    Main application logic for Streamlit UI and model interaction
    """
    load_credentials()
    st.title('🚀 watsonx.ai Interactive Q&A')
    question = st.text_input("Ask a question (e.g., 'What is AI?')")

    if not question.strip():
        question = "What is IBM?"

    prompt = build_prompt(question)
    st.text_area("Generated Prompt", prompt, height=200)

    model_type = ModelTypes.FLAN_UL2
    max_tokens = 150
    min_tokens = 30
    decoding = DecodingMethods.BEAM_SEARCH
    stop_sequences = ['\n']

    model = create_model(model_type, max_tokens, min_tokens, decoding, stop_sequences)
    response = model.generate(prompt=prompt)
    output = response.get('results', [{}])[0].get('generated_text', "No response generated.")
    
    st.markdown(f"### **Answer:** {output}")

if __name__ == "__main__":
    main()
