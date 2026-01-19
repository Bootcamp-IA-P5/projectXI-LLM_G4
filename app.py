import os
import sys
import locale


import io
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
import streamlit as st

from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

# Use the content generator pipeline for the second tab
from content_generator import generate_content


# ---------- Setup ----------
# Load environment variables with UTF-8 encoding
load_dotenv(encoding='utf-8')
st.set_page_config(page_title="LLM Content Generator & Chat", layout="centered")


@st.cache_resource(show_spinner=False)
def get_llm():
    """Create and cache the chat model once per session."""
    # Prefer the larger, more capable model if available
    model_name = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")
    temperature = float(os.getenv("MODEL_TEMPERATURE", "0.3"))
    return ChatGroq(model=model_name, temperature=temperature)


def ensure_api_key():
    if not os.getenv("GROQ_API_KEY"):
        st.error("GROQ_API_KEY is missing. Add it to your .env file.")
        return False
    return True

# ---------- Sidebar: User Profile ----------
if "user_profile" not in st.session_state:
    st.session_state.user_profile = {
        "name": "",
        "industry": "",
        "tone": "",
        "values": ""
    }

with st.sidebar:
    st.header("👤 Brand / User Profile")

    with st.expander("Configure profile", expanded=True):
        with st.form("user_profile_form"):
            name = st.text_input(
                "Company or person name",
                value=st.session_state.user_profile.get("name", "")
            )

            industry = st.text_input(
                "Industry / Sector",
                value=st.session_state.user_profile.get("industry", "")
            )

            tone = st.text_area(
                "Characteristic tone of voice",
                placeholder="e.g. professional, friendly, bold, educational…",
                value=st.session_state.user_profile.get("tone", "")
            )

            values = st.text_area(
                "Values / Mission (optional)",
                placeholder="e.g. innovation, transparency, social impact…",
                value=st.session_state.user_profile.get("values", "")
            )

            save_profile = st.form_submit_button("Save profile")

        if save_profile:
            st.session_state.user_profile = {
                "name": name,
                "industry": industry,
                "tone": tone,
                "values": values
            }
            st.success("Profile saved ✔️")

# ---------- UI ----------
st.title("🧠 LLM Content Generator & Chat")
tabs = st.tabs(["Chat", "Content Generator"])


# ---------- Chat Tab ----------
with tabs[0]:
    st.subheader("Chat Assistant")
    st.caption("Backed by Groq Llama 3.3. Your messages are ephemeral and stored only in this session.")

    if ensure_api_key():
        llm = get_llm()

        # Initialize chat history
        if "chat_history" not in st.session_state:
            st.session_state.chat_history = [
                AIMessage(content="Hi! I'm your AI assistant. How can I help today?")
            ]

        # Render history
        for msg in st.session_state.chat_history:
            role = "assistant" if isinstance(msg, AIMessage) else "user"
            with st.chat_message(role):
                st.markdown(msg.content)

        # Chat input
        user_input = st.chat_input("Type your message…")
        if user_input:
            user_msg = HumanMessage(content=user_input)
            st.session_state.chat_history.append(user_msg)

            with st.chat_message("user"):
                st.markdown(user_input)

            with st.chat_message("assistant"):
                with st.spinner("Thinking…"):
                    # Optional system prompt for behavior
                    system_msg = SystemMessage(content=os.getenv(
                        "SYSTEM_PROMPT",
                        "You are a helpful and concise assistant."
                    ))
                    messages = [system_msg] + st.session_state.chat_history
                    try:
                        ai_msg = llm.invoke(messages)
                        st.session_state.chat_history.append(ai_msg)
                        st.markdown(ai_msg.content)
                    except Exception as e:
                        st.error(f"Model error: {e}")


# ---------- Content Generator Tab ----------
with tabs[1]:
    st.subheader("Generate Marketing Content")
    st.caption("Fill in the fields and generate ready-to-publish content.")

    with st.form("content_form"):
        topic = st.text_input("Topic", placeholder="e.g., The benefits of virtual reality for education")
        platform = st.selectbox(
            "Platform",
            ["Blog Post", "Twitter/X", "Instagram Caption", "LinkedIn Post"],
            index=0,
        )
        audience = st.text_input("Audience", placeholder="e.g., School Administrators and Educators")
        tone = st.selectbox("Tone", ["Informative", "Professional", "Friendly", "Playful", "Persuasive"], index=0)
        submitted = st.form_submit_button("Generate")

    if submitted:
        if not all([topic.strip(), audience.strip(), tone.strip(), platform.strip()]):
            st.warning("Please fill in all fields.")
        elif not ensure_api_key():
            pass
        else:
            with st.spinner("Generating content…"):
                try:
                    output = generate_content(
                        topic=topic,
                        platform=platform,
                        audience=audience,
                        tone=tone,
                        user_profile=st.session_state.get("user_profile", {})
                    )
                    st.markdown("---")
                    st.markdown(output)
                except Exception as e:
                    st.error(f"Generation failed: {e}")
