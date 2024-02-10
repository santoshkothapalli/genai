import os
from secret_key import GOOGLE_API_KEY
import streamlit as st
import google.generativeai as genai
import google.ai.generativelanguage as glm
from PIL import Image

os.environ['GOOGLE_API_KEY'] = GOOGLE_API_KEY
genai.configure(api_key=os.environ['GOOGLE_API_KEY'])
model = genai.GenerativeModel("gemini-pro-vision")

uploaded_file = st.file_uploader(label="Upload to Image to Analyze",accept_multiple_files=False, 
                 type=["JPEG","PNG"])

question = st.text_area(label="Ask Question: ", 
                        value="" , height=50)

def button_click():
    if uploaded_file is not None and question is not None :
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image...")
        input_prompt = "Analyze the uploaded image"
        
        response = model.generate_content(
        glm.Content(
            parts = [
                glm.Part(text=question),
                glm.Part(
                    inline_data=glm.Blob(
                        mime_type='image/jpeg',
                        data=uploaded_file.getvalue()
                    )
                ),
            ],
        ),
        stream=True)
        response.resolve()
        st.write(response.text)

st.button("Submit", on_click=button_click)
