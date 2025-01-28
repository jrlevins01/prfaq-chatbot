import openai
import streamlit as st

# Retrieve API Key securely
if "OPENAI_API_KEY" in st.secrets:
    api_key = st.secrets["OPENAI_API_KEY"]
else:
    st.error("❌ OpenAI API Key is missing! Please set it in Streamlit Secrets.")
    st.stop()  # Stop execution if key is missing

# Set OpenAI client with the correct API key
client = openai.OpenAI(api_key=api_key)

st.title("PRFAQuick - Jason Levinson")

# User inputs
title = st.text_input("What is the title of your initiative?")
problem = st.text_area("What problem does it solve?")
audience = st.text_area("Who is your target audience?")
solution = st.text_area("Describe your solution.")
how_it_works = st.text_area("How does it work?")
benefits = st.text_area("What are the key benefits?")

if st.button("Generate PRFAQ"):
    prompt = f"""
    Generate a PRFAQ using the following details:

    Title: {title}
    Problem: {problem}
    Audience: {audience}
    Solution: {solution}
    How It Works: {how_it_works}
    Benefits: {benefits}

    Format the response as a structured PRFAQ document.
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        st.subheader("Generated PRFAQ")
        st.write(response.choices[0].message.content)
    except openai.OpenAIError as e:
        st.error(f"❌ OpenAI API Error: {e}")

