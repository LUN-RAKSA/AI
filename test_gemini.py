import streamlit as st
from google import genai
import time

st.set_page_config(page_title="Gemini Connection Test")

st.title("ZENTRA AI - Gemini Test")

try:
    api_key = st.secrets["GEMINI_API_KEY"].strip()
    client = genai.Client(api_key=api_key)

    st.info("Connecting to Gemini...")

    response = None

    # Retry up to 3 times if the server is temporarily busy
    for attempt in range(3):
        try:
            response = client.models.generate_content(
                model="gemini-3.5-flash-lite",
                contents="Say Hello to ZENTRA AI in one sentence."
            )
            break

        except Exception as e:
            if "503" in str(e) and attempt < 2:
                st.warning(
                    f"Gemini is busy. Retrying "
                    f"({attempt + 1}/3)..."
                )
                time.sleep(2 ** (attempt + 1))
            else:
                raise e

    if response:
        st.success("Gemini connection successful! 🎉")
        st.write("Model: Gemini 3.5 Flash-Lite")
        st.write("Response:")
        st.write(response.text)

except Exception as e:
    st.error("Connection failed ❌")
    st.exception(e)