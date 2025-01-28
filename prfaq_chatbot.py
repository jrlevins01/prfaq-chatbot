import os
import openai
import streamlit as st


# Check if API key exists in Streamlit Secrets
if "OPENAI_API_KEY" in st.secrets:
    api_key = st.secrets["OPENAI_API_KEY"]  # Store it in a variable
    client = openai.OpenAI(api_key=api_key)  # Use the variable
else:
    st.error("❌ OpenAI API Key is missing! Please set it in Streamlit Secrets.")


st.title("PRFAQuick - by EI/I&S Procurement")

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

    response = client.chat.completions.create(
        model="gpt-4-turbo",
        messages=[{"role": "user", "content": prompt}]
    )

    st.subheader("Generated PRFAQ")
    st.write(response.choices[0].message.content)
