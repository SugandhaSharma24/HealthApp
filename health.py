from dotenv import load_dotenv
load_dotenv()  # Load environment variables

import streamlit as st
import os
import google.generativeai as genai
from PIL import Image

# Configure the API key for Google Gemini
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise ValueError("API key not found. Please set the GOOGLE_API_KEY environment variable.")

genai.configure(api_key=api_key)

def get_gemini_response(input_text, image_data, prompt):
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(
            input_text=input_text,
            image=image_data,
            prompt=prompt
        )
        return response.text
    except Exception as e:
        st.error(f"Error calling Gemini API: {e}")
        return None

def input_image_setup(uploaded_file):
    if uploaded_file is not None:
        bytes_data = uploaded_file.read()
        image_data = {
            "mime_type": uploaded_file.type,
            "data": bytes_data
        }
        return image_data
    else:
        raise FileNotFoundError("No file uploaded")

# Initialize Streamlit app
st.set_page_config(page_title="Gemini Health App")
st.header("Gemini Health App")

input_prompt = st.text_input("Input Prompt: ", key="input")
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

image = ""
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image.", use_column_width=True)

submit = st.button("Tell me the total calories")

input_text = """
You are an expert nutritionist who needs to analyze the food items in the image and calculate the total calories, providing details for each item in the following format:

1. Item 1 - Calories
2. Item 2 - Calories
----
----
"""

# If the submit button is clicked
if submit:
    try:
        image_data = input_image_setup(uploaded_file)
        response = get_gemini_response(input_text, image_data, input_prompt)
        if response:
            st.subheader("The Response is")
            st.write(response)
    except FileNotFoundError:
        st.warning("Please upload a file.")
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")
