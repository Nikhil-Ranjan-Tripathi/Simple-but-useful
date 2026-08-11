from dotenv import load_dotenv
load_dotenv()

import os
import streamlit as st
from PIL import Image
from google import genai


# ---------------------------------------------------
# GEMINI CONFIGURATION
# ---------------------------------------------------

API_KEY = os.getenv("Google_API_Key")

if not API_KEY:
    st.error("Google API Key not found. Check your .env file.")
    st.stop()

client = genai.Client(api_key=API_KEY)


# ---------------------------------------------------
# GEMINI RESPONSE FUNCTION
# ---------------------------------------------------

def get_gemini_response(input_text, image, prompt):

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=[
            input_text,
            image,
            prompt
        ]
    )

    return response.text


# ---------------------------------------------------
# IMAGE SETUP
# ---------------------------------------------------

def input_image_setup(uploaded_file):

    if uploaded_file is not None:
        return Image.open(uploaded_file)

    raise FileNotFoundError("No file uploaded")


# ---------------------------------------------------
# STREAMLIT PAGE CONFIGURATION
# ---------------------------------------------------

st.set_page_config(
    page_title="Gemini Invoice Analyzer",
    page_icon="🧾"
)

st.header("Gemini Invoice Analyzer")


# ---------------------------------------------------
# USER INPUT
# ---------------------------------------------------

input_text = st.text_input(
    "Input Prompt:",
    key="input"
)

uploaded_file = st.file_uploader(
    "Choose an invoice image...",
    type=["jpg", "jpeg", "png"]
)


# ---------------------------------------------------
# DISPLAY IMAGE
# ---------------------------------------------------

image = None

if uploaded_file is not None:

    image = Image.open(uploaded_file)

    st.image(
        image,
        caption="Uploaded Invoice",
        use_container_width=True
    )


# ---------------------------------------------------
# GEMINI INVOICE INSTRUCTION
# ---------------------------------------------------

input_prompt = """
You are an expert invoice analysis assistant.

You will receive an image of an invoice.

Analyze the invoice carefully and answer the user's question
based on the information visible in the invoice.

Extract information accurately.

Pay special attention to:

- Invoice number
- Invoice date
- Vendor / seller name
- Customer / buyer name
- Product or service names
- Quantity
- Unit price
- Tax
- Discount
- Subtotal
- Grand total
- Payment information

Do not invent information that is not present in the invoice.

If a piece of information cannot be found, clearly say
"Not available in the invoice".
"""


# ---------------------------------------------------
# SUBMIT BUTTON
# ---------------------------------------------------

submit = st.button("Analyze Invoice")


# ---------------------------------------------------
# PROCESS REQUEST
# ---------------------------------------------------

if submit:

    if uploaded_file is None:

        st.warning("Please upload an invoice image first.")

    else:

        with st.spinner("Analyzing invoice..."):

            try:

                image_data = input_image_setup(uploaded_file)

                response = get_gemini_response(
                    input_text,
                    image_data,
                    input_prompt
                )

                st.subheader("Gemini Response")

                st.write(response)

            except Exception as e:

                st.error(f"Error: {e}")

