import os
import openai
import streamlit as st

# Set your OpenAI API key
OPENAI_API_KEY = "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"  # Replace this with your actual API key
client = openai.OpenAI(api_key=OPENAI_API_KEY)

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
