from dotenv import load_dotenv
import streamlit as st
import os
import google.generativeai as genai
from PIL import Image
import matplotlib.pyplot as plt

# Load all the environment variables
load_dotenv()

#Debugging
# api_key = os.getenv("GOOGLE_API_KEY")
# if not api_key:
#     st.error("API key not found. Please check your .env file.")
# else:
#     st.write("API key loaded successfully.")    

# Configure the Generative AI with the API key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to get the response from Gemini Pro model
def get_gemini_response(input, prompt):
    model = genai.GenerativeModel('gemini-pro') 
    response = model.generate_content([input, prompt])
    return response.text

# Function to plot and save the confidence score image
def plot_confidence_score(confidence_score):
    fig, ax = plt.subplots()
    ax.barh(['Confidence'], [confidence_score], color='blue')
    ax.set_xlim(0, 100)
    ax.set_xlabel('Confidence Score (%)')
    plt.title('Diagnosis Confidence Score')
    plt.savefig('confidence_score.png')

# Initialize the Streamlit app
st.set_page_config(page_title="SymptomAI Health App")
st.header("SymptomAI Health App")

# Input fields for user prompt
input = st.text_input("Describe your symptoms: ", key="input")

# Submit button
submit = st.button("Get Diagnosis")

# Input prompt template for the generative model
input_prompt = """
You are an expert doctor. Diagnose the illness based on the described symptoms and provide a confidence score for your diagnosis.
"""

# If submit button is clicked
if submit:
    if input:
        # Get the response from the generative model
        response = get_gemini_response(input, input_prompt)
        
        # For illustration purposes, we will generate a random confidence score
        # In a real application, this should be derived from the model response
        import random
        confidence_score = random.uniform(70, 100)  # Random confidence score between 70 and 100
        
        # Plot and save the confidence score image
        plot_confidence_score(confidence_score)
        
        # Display the response and the confidence score image
        st.subheader("Diagnosis")
        st.write(response)
        st.image('confidence_score.png', caption="Diagnosis Confidence Score", use_column_width=True)
    else:
        st.error("Please enter the symptoms in the input field.")