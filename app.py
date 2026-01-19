import os
import sys
import locale

# Fix UTF-8 encoding issues - Streamlit compatible approach
# Don't reconfigure sys.stdout/stderr as Streamlit manages them
# Instead, set environment variables and locale
try:
    locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
except:
    try:
        locale.setlocale(locale.LC_ALL, 'C.UTF-8')
    except:
        pass

# Set UTF-8 encoding in environment
os.environ['PYTHONIOENCODING'] = 'utf-8'

from dotenv import load_dotenv
import streamlit as st

from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

# Import LLM factory and content generator
from llm_factory import get_llm, get_available_models, validate_provider_config
from content_generator import generate_content
from image_generator import get_images_for_content, format_image_markdown


# ---------- Setup ----------
# Load environment variables with UTF-8 encoding
load_dotenv(encoding='utf-8')
st.set_page_config(page_title="LLM Content Generator & Chat", layout="centered")


# Initialize LLM provider selection in session state
if "llm_provider" not in st.session_state:
    st.session_state.llm_provider = "groq"
if "llm_model" not in st.session_state:
    st.session_state.llm_model = "llama-3.1-8b-instant"
if "llm_temperature" not in st.session_state:
    st.session_state.llm_temperature = 0.7


@st.cache_resource(show_spinner=False)
def get_cached_llm(provider, model, temperature):
    """Create and cache the chat model once per session."""
    return get_llm(provider, model, temperature)


def ensure_api_key(provider):
    """Check if API key exists for the selected provider."""
    is_valid, error_msg = validate_provider_config(provider)
    if not is_valid:
        st.error(f"{error_msg}")
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
    st.header("⚙️ Configuration")
    
    # LLM Provider Selection
    with st.expander("🤖 LLM Provider", expanded=True):
        provider = st.selectbox(
            "Select LLM Provider",
            ["groq", "openai", "ollama"],
            index=0 if st.session_state.llm_provider == "groq" else (1 if st.session_state.llm_provider == "openai" else 2),
            help="Choose the LLM provider for content generation"
        )
        
        # Get available models for selected provider
        available_models = get_available_models(provider)
        default_model_index = 0
        if st.session_state.llm_model in available_models:
            default_model_index = available_models.index(st.session_state.llm_model)
        
        model = st.selectbox(
            "Select Model",
            available_models,
            index=default_model_index,
            help=f"Available models for {provider}"
        )
        
        temperature = st.slider(
            "Temperature",
            min_value=0.0,
            max_value=1.0,
            value=st.session_state.llm_temperature,
            step=0.1,
            help="Controls randomness: 0 = deterministic, 1 = creative"
        )
        
        # Update session state
        st.session_state.llm_provider = provider
        st.session_state.llm_model = model
        st.session_state.llm_temperature = temperature
        
        # Show validation status
        is_valid, error_msg = validate_provider_config(provider)
        if is_valid:
            st.success(f"✅ {provider.upper()} configured")
        else:
            st.warning(f"⚠️ {error_msg}")
    
    st.divider()
    
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
tabs = st.tabs(["Chat", "Content Generator", "RAG - Scientific Content"])


# ---------- Chat Tab ----------
with tabs[0]:
    st.subheader("Chat Assistant")
    provider_display = st.session_state.llm_provider.upper()
    st.caption(f"Backed by {provider_display} ({st.session_state.llm_model}). Your messages are ephemeral and stored only in this session.")

    if ensure_api_key(st.session_state.llm_provider):
        try:
            llm = get_cached_llm(
                st.session_state.llm_provider,
                st.session_state.llm_model,
                st.session_state.llm_temperature
            )
        except Exception as e:
            st.error(f"Error initializing LLM: {e}")
            st.stop()

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
        language = st.selectbox(
            "Language",
            ["Spanish", "English", "French", "Italian"],
            index=0,
            help="Select the language for content generation"
        )
        submitted = st.form_submit_button("Generate")

    if submitted:
        if not all([topic.strip(), audience.strip(), tone.strip(), platform.strip()]):
            st.warning("Please fill in all fields.")
        elif not ensure_api_key(st.session_state.llm_provider):
            pass
        else:
            with st.spinner(f"Generating content in {language} with {st.session_state.llm_provider.upper()}…"):
                try:
                    output = generate_content(
                        topic=topic,
                        platform=platform,
                        audience=audience,
                        tone=tone,
                        language=language,
                        user_profile=st.session_state.get("user_profile", {}),
                        provider=st.session_state.llm_provider,
                        model=st.session_state.llm_model,
                        temperature=st.session_state.llm_temperature
                    )
                    
                    st.markdown("---")
                    st.markdown("### Generated Content")
                    st.markdown(output)
                    
                    # Fetch and display images
                    if os.getenv("UNSPLASH_ACCESS_KEY"):
                        with st.spinner("Fetching relevant images…"):
                            images = get_images_for_content(output, num_images=1)
                            if images:
                                st.markdown("---")
                                st.markdown("### Relevant Images")
                                for img in images:
                                    st.image(img["url"], caption=f"Photo by {img['photographer']} on Unsplash", use_container_width=True)
                                    st.caption(f"*{img['description']}*")
                    else:
                        st.info("💡 Tip: Add UNSPLASH_ACCESS_KEY to .env to enable image generation")
                    
                except Exception as e:
                    st.error(f"Generation failed: {e}")


# ---------- RAG Tab ----------
with tabs[2]:
    st.subheader("🔬 Scientific Content Generator (RAG)")
    st.caption("Generate science content based on your indexed documents (PDF/TXT from data/raw).")
    
    # Import RAG modules
    try:
        from rag.database import ingest_to_vectorstore, load_vectorstore
        from rag.retrieval import query_rag, get_retriever
        rag_available = True
    except ImportError as e:
        st.error(f"RAG modules not available: {e}")
        st.info("Make sure you have installed: `pip install langchain-community chromadb sentence-transformers`")
        rag_available = False
    
    if rag_available:
        # Initialize RAG state
        if "vectorstore" not in st.session_state:
            st.session_state.vectorstore = None
        if "rag_indexed" not in st.session_state:
            st.session_state.rag_indexed = False
        
        # Section 1: Index Documents
        with st.expander("📚 Index Documents", expanded=not st.session_state.rag_indexed):
            st.markdown("Index PDF and TXT files from `data/raw` folder.")
            
            col1, col2 = st.columns(2)
            with col1:
                chunk_size = st.number_input("Chunk size", min_value=100, max_value=4000, value=1000, step=100)
            with col2:
                chunk_overlap = st.number_input("Chunk overlap", min_value=0, max_value=500, value=200, step=50)
            
            if st.button("🔄 Index Documents", type="primary"):
                with st.spinner("Loading and indexing documents..."):
                    try:
                        vectorstore = ingest_to_vectorstore(
                            source_path="data/raw",
                            persist_directory="chroma_db",
                            collection_name="papers",
                            chunk_size=chunk_size,
                            chunk_overlap=chunk_overlap,
                        )
                        st.session_state.vectorstore = vectorstore
                        st.session_state.rag_indexed = True
                        st.success("✅ Documents indexed successfully!")
                    except FileNotFoundError:
                        st.warning("No PDF or TXT files found in `data/raw`. Add documents and try again.")
                    except Exception as e:
                        st.error(f"Indexing failed: {e}")
            
            # Option to load existing vectorstore
            if st.button("📂 Load Existing Index"):
                try:
                    vectorstore = load_vectorstore(
                        persist_directory="chroma_db",
                        collection_name="papers"
                    )
                    st.session_state.vectorstore = vectorstore
                    st.session_state.rag_indexed = True
                    st.success("✅ Loaded existing index from chroma_db")
                except Exception as e:
                    st.error(f"Could not load index: {e}")
        
        # Section 2: Query RAG
        st.markdown("---")
        st.markdown("### 🔍 Ask Questions")
        
        if not st.session_state.rag_indexed:
            st.info("👆 First, index your documents or load an existing index.")
        else:
            # Query form
            query = st.text_area(
                "Your question",
                placeholder="e.g., What are the main impacts of AI on the economy?",
                height=100
            )
            
            col1, col2 = st.columns(2)
            with col1:
                num_sources = st.slider("Number of sources to retrieve", min_value=1, max_value=10, value=4)
            with col2:
                use_llm = st.checkbox("Generate synthesized answer", value=True)
            
            if st.button("🚀 Search & Generate", type="primary"):
                if not query.strip():
                    st.warning("Please enter a question.")
                else:
                    with st.spinner("Searching documents and generating answer..."):
                        try:
                            # Get LLM if needed
                            llm = None
                            if use_llm and ensure_api_key(st.session_state.llm_provider):
                                llm = get_cached_llm(
                                    st.session_state.llm_provider,
                                    st.session_state.llm_model,
                                    st.session_state.llm_temperature
                                )
                            
                            # Query RAG
                            result = query_rag(
                                query=query,
                                vectorstore=st.session_state.vectorstore,
                                llm=llm,
                                k=num_sources
                            )
                            
                            # Display answer
                            if "answer" in result:
                                st.markdown("### 💡 Answer")
                                st.markdown(result["answer"])
                            
                            # Display sources
                            st.markdown("### 📄 Sources")
                            for i, source in enumerate(result["sources"], 1):
                                with st.expander(f"Source {i}: {source['metadata'].get('filename', 'Unknown')}"):
                                    st.markdown(f"**Chunk {source['metadata'].get('chunk_index', '?')}**")
                                    st.markdown(source["content"][:500] + "..." if len(source["content"]) > 500 else source["content"])
                        
                        except Exception as e:
                            st.error(f"Query failed: {e}")
