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
You are an expert procurement manager at a leading tech company. 
Your job is to craft an engaging, persuasive, and structured internal PRFAQ for proposed projects to assist procurement.

📌 **Format**:
1️⃣ **Press Release** (Catchy opening, problem statement, and announcement)
2️⃣ **FAQs** (Key stakeholder questions with clear, concise answers)
3️⃣ **Justification** (Why this project matters and how it will help procurement)
4️⃣ **Competitive Advantage** (What makes this stand out and how it impacts procurement KPIs)
5️⃣ **Call to Action** (Encouraging adoption)

Use the following details, but enhance them with compelling examples and business value insights:

**Title:** {title}
**Problem:** {problem}
**Audience:** {audience}
**Solution:** {solution}
**How It Works:** {how_it_works}
**Benefits:** {benefits}

Make sure the PRFAQ is engaging, concise, and persuasive, appealing to both technical and business audiences.
"""


    try:
    response = client.chat.completions.create(
    model="gpt-4-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.9,  # High creativity
        top_p=0.85,  # Encourages diversity in responses
        frequency_penalty=0.3,  # Reduces repetition
        presence_penalty=0.4,  # Encourages new ideas
        max_tokens=1000  # Ensures a detailed response
    )


        st.subheader("Generated PRFAQ")
        st.write(response.choices[0].message.content)
    except openai.OpenAIError as e:
        st.error(f"❌ OpenAI API Error: {e}")

