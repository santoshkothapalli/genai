import os
from secret_key import GOOGLE_API_KEY
import streamlit as st
import google.generativeai as genai
import google.ai.generativelanguage as glm
from PIL import Image
## 1. Specify the google key , set the same to environment variable and select the model to use
os.environ['GOOGLE_API_KEY'] = GOOGLE_API_KEY
genai.configure(api_key=os.environ['GOOGLE_API_KEY'])
model = genai.GenerativeModel("gemini-pro-vision")
##2. File Uploader to upload the JPEG or PNG files
uploaded_file = st.file_uploader(label="Upload to Image to Analyze",accept_multiple_files=False, 
                 type=["JPEG","PNG"])
##3. Text field to post the question to model
question = st.text_area(label="Ask Question: ", 
                        value="" , height=50)
##4. Event which is invoked when the Submit is clicked 
def button_click():
    if uploaded_file is not None and question is not None :
        image = Image.open(uploaded_file)
      ##5. Displaying the image uploaded by the user
        st.image(image, caption="Uploaded Image...")
        input_prompt = "Analyze the uploaded image"
        ##6. Model cant take the uploaded file directly , this need to be convered to Content Parts
        ## i.e. Create Blob using the mime type and stream 
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
        ##7. Write the response from llm model to the browser
        st.write(response.text)

st.button("Submit", on_click=button_click)
