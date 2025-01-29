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

st.title("PRFAQuick - by EI/I&S Procurement")

# User inputs
title = st.text_input("What is the title of your initiative?")
problem = st.text_area("What problem does it solve?")
audience = st.text_area("Who is the target audience? (e.g., executives, engineers, product managers, end-users)")
solution = st.text_area("Describe your solution.")
how_it_works = st.text_area("How does it work?")
benefits = st.text_area("What are the key benefits?")

# Placeholder for the generated PRFAQ
generated_prfaq = st.session_state.get("generated_prfaq", None)

if st.button("Generate PRFAQ"):
    prompt = f"""
    You are an expert procurement manager at a leading medtech company, tasked with crafting a compelling PRFAQ for an upcoming project, program or initiative for internal use, not directed toward external parties or customers.

    🎯 **Target Audience:** {audience}  
    - Understand their role, concerns, and priorities.
    - Use language, structure, and key messages that appeal directly to them.
    - Highlight aspects that matter most to their responsibilities.

    📌 **Format**:
    1️⃣ **Press Release** (Engaging opening, problem statement, and announcement)
    2️⃣ **FAQs** (Key stakeholder questions with persuasive answers)
    3️⃣ **Internal Justification** (Why this program/product is needed)
    4️⃣ **Benefits** (What are the main benefits this program solves for)
    5️⃣ **Summary** (brief summary and bullet points of the main features/benefits and closing statement)

    **Use the following details to generate the PRFAQ** while ensuring it resonates with the target audience:

    **Title:** {title}  
    **Problem:** {problem}  
    **Solution:** {solution}  
    **How It Works:** {how_it_works}  
    **Benefits:** {benefits}  

    📢 **Guidelines**:
    - Make the PRFAQ clear, structured, and compelling.
    - Avoid technical jargon if the audience is non-technical.
    - Emphasize ROI and business impact for executives.
    - Highlight ease of integration for engineers.
    - Focus on usability and efficiency for end-users.

    Generate a well-structured, engaging internal use PRFAQ that directly speaks to the needs and concerns of the intended audience to pitch the idea to the audience and/or explain what the program is about.
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.9,  # High creativity
            top_p=0.85,  # Encourages diverse responses
            frequency_penalty=0.3,  # Reduces repetition
            presence_penalty=0.4,  # Encourages new ideas
            max_tokens=1000  # Ensures a detailed response
        )

        generated_prfaq = response.choices[0].message.content
        st.session_state["generated_prfaq"] = generated_prfaq  # Store in session state

        st.subheader("Generated PRFAQ")
        st.write(generated_prfaq)

    except openai.OpenAIError as e:
        st.error(f"❌ OpenAI API Error: {e}")

# Section for Editing PRFAQ
if generated_prfaq:
    st.subheader("🔄 Would You Like to Edit the PRFAQ?")
    
    section_to_edit = st.text_input("Which section (or whole document) would you like to edit?")
    edit_feedback = st.text_area("Describe the changes you'd like to make.")

    if st.button("Update PRFAQ"):
        edit_prompt = f"""
        You previously generated the following PRFAQ:

        {generated_prfaq}

        The user has provided feedback and would like to modify the section: {section_to_edit}.  
        Here is their requested change:  
        "{edit_feedback}"

        Please regenerate the PRFAQ while keeping the original structure, only making the requested adjustments.
        """

        try:
            response = client.chat.completions.create(
                model="gpt-4-turbo",
                messages=[{"role": "user", "content": edit_prompt}],
                temperature=0.8,  # Keep it structured but flexible
                top_p=0.85,
                max_tokens=1000
            )

            updated_prfaq = response.choices[0].message.content
            st.session_state["generated_prfaq"] = updated_prfaq  # Store the updated PRFAQ

            st.subheader("Updated PRFAQ")
            st.write(updated_prfaq)

        except openai.OpenAIError as e:
            st.error(f"❌ OpenAI API Error: {e}")
