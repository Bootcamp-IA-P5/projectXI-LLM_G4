# Import necessary modules
import os
import sys
import locale
import io

# Fix UTF-8 encoding issues - Must be at the very top
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

# Set locale to UTF-8
try:
    locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
except:
    try:
        locale.setlocale(locale.LC_ALL, 'C.UTF-8')
    except:
        pass

from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate


# 1. Load Environment Variables
# This loads the GROQ_API_KEY from the .env file with UTF-8 encoding
load_dotenv(encoding='utf-8')

# 2. Define the LLM Model
# Initializes the connection to the Groq API
# temperature=0.7 allows for creative but still coherent responses
# The model can be changed to any other supported LLM
llm = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0.7
)

# 3. Define the Prompt Template
# This is the "Prompt Engineering" step. The template structures the input
# for the model, telling it what its role is and what to focus on.
# It uses f-string-style placeholders (like {topic}) that LangChain fills in.
prompt_template = """
You are an expert digital content creator specializing in marketing and SEO.
Your task is to generate compelling, ready-to-publish content.

**Instructions:**
- **Topic:** {topic}
- **Platform:** {platform}
- **Audience:** {audience}
- **Tone:** {tone}
- **Length:** Generate content that is appropriate for the selected platform.

**Specific Platform Guidelines:**
- **Blog Post:** Use Markdown for formatting (headings, bolding, lists). Write a detailed introduction and several main points.
- **Twitter/X:** Use concise language, strong hooks, and relevant hashtags (max 280 characters).
- **Instagram Caption:** Use a short, engaging description and a few popular hashtags.
- **LinkedIn Post:** Write a professional post focused on insights or career advice.

**GENERATE CONTENT BELOW:**
"""

# 4. Create the ChatPromptTemplate object
# This takes the string and defines the expected input variables.
prompt = ChatPromptTemplate.from_template(prompt_template)

# 5. Create the Chain using LCEL (LangChain Expression Language)
# Modern LangChain uses the pipe operator (|) to chain components.
# This creates: Prompt -> LLM pipeline
chain = prompt | llm


# 6. Content Generation Function
# A simple function to take the user inputs and run the chain.
def generate_content(topic: str, platform: str, audience: str, tone: str, user_profile: dict = None) -> str:
    """
    Generates content by invoking the LangChain chain with user inputs.
    
    Args:
        topic: The topic for the content
        platform: Target platform (Blog Post, Twitter/X, etc.)
        audience: Target audience
        tone: Desired tone for the content
        user_profile: Optional dictionary with user/company profile information
    """
    # Build the base prompt template
    base_template = """
You are an expert digital content creator specializing in marketing and SEO.
Your task is to generate compelling, ready-to-publish content.

**Instructions:**
- **Topic:** {topic}
- **Platform:** {platform}
- **Audience:** {audience}
- **Tone:** {tone}
- **Length:** Generate content that is appropriate for the selected platform.

**Specific Platform Guidelines:**
- **Blog Post:** Use Markdown for formatting (headings, bolding, lists). Write a detailed introduction and several main points.
- **Twitter/X:** Use concise language, strong hooks, and relevant hashtags (max 280 characters).
- **Instagram Caption:** Use a short, engaging description and a few popular hashtags.
- **LinkedIn Post:** Write a professional post focused on insights or career advice.
"""
    
    # Add user profile section if profile exists and has data
    profile_section = ""
    if user_profile and any(user_profile.values()):
        profile_parts = []
        if user_profile.get("name"):
            profile_parts.append(f"- **Name:** {user_profile['name']}")
        if user_profile.get("industry"):
            profile_parts.append(f"- **Industry:** {user_profile['industry']}")
        if user_profile.get("tone"):
            profile_parts.append(f"- **Voice/Tone:** {user_profile['tone']}")
        if user_profile.get("values"):
            profile_parts.append(f"- **Values:** {user_profile['values']}")
        
        if profile_parts:
            profile_section = "\n**Company/Personal Profile:**\n" + "\n".join(profile_parts) + "\n"
    
    # Combine base template with profile section
    prompt_template = base_template + profile_section + "\n**GENERATE CONTENT BELOW:**\n"
    
    # Create the prompt template dynamically
    prompt = ChatPromptTemplate.from_template(prompt_template)
    
    # Recreate the chain with the new prompt
    dynamic_chain = prompt | llm
    
    # The .invoke method executes the chain with the provided variables.
    response = dynamic_chain.invoke({
        "topic": topic,
        "platform": platform,
        "audience": audience,
        "tone": tone
    })
    
    # The response is an AIMessage object, access content with .content
    return response.content

# Example of how to use the function (for testing)
if __name__ == "__main__":
    test_content = generate_content(
        topic="The benefits of virtual reality for education",
        platform="Blog Post",
        audience="School Administrators and Educators",
        tone="Informative and Professional"
    )
    print("--- GENERATED CONTENT ---")
    print(test_content)