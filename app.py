import streamlit as st
from groq import Groq

# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Lakshmi Groq AI Chatbot",
    page_icon="🤖",
    layout="centered"
)

# =========================================================
# GROQ API KEY
# =========================================================

GROQ_API_KEY = "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"

# Create Groq client
client = Groq(api_key=GROQ_API_KEY)

# =========================================================
# MODEL
# =========================================================

MODEL_NAME = "openai/gpt-oss-120b"

# =========================================================
# INITIALIZE CHAT HISTORY
# =========================================================

if "messages" not in st.session_state:

    st.session_state.messages = [
        {
            "role": "system",
            "content": (
                "You are a helpful and friendly AI assistant. "
                "Give clear, simple and accurate answers. "
                "Explain difficult topics in an easy-to-understand way."
            )
        }
    ]

# =========================================================
# HEADER
# =========================================================

st.title("🤖 Lakshmi Groq AI Chatbot")

st.write(
    "Chat with an AI assistant powered by Groq."
)

st.divider()

# =========================================================
# DISPLAY CHAT HISTORY
# =========================================================

for message in st.session_state.messages:

    # Do not display system message
    if message["role"] == "system":
        continue

    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# =========================================================
# USER INPUT
# =========================================================

user_message = st.chat_input(
    "Type your message here..."
)

# =========================================================
# HANDLE USER MESSAGE
# =========================================================

if user_message:

    # -----------------------------------------------------
    # Display user's message
    # -----------------------------------------------------

    with st.chat_message("user"):
        st.markdown(user_message)

    # -----------------------------------------------------
    # Save user's message
    # -----------------------------------------------------

    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_message
        }
    )

    # -----------------------------------------------------
    # Generate Groq response
    # -----------------------------------------------------

    with st.chat_message("assistant"):

        with st.spinner("Thinking..."):

            try:

                response = client.chat.completions.create(
                    model=MODEL_NAME,
                    messages=st.session_state.messages,
                    temperature=0.7,
                    max_completion_tokens=1024
                )

                assistant_message = response.choices[0].message.content

                # Display AI response
                st.markdown(assistant_message)

                # Save AI response
                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": assistant_message
                    }
                )

            except Exception as e:

                st.error(
                    "Something went wrong. Please check your "
                    "API key, internet connection, and Groq model access."
                )

                st.code(str(e))

# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.header("⚙️ Chat Settings")

    st.write("### 🤖 Model")

    st.code(MODEL_NAME)

    st.divider()

    st.write("### ✨ Features")

    st.write("✅ Groq API")
    st.write("✅ Streamlit Chat Interface")
    st.write("✅ Conversation History")
    st.write("✅ Multi-turn Conversation")
    st.write("✅ Clear Chat")

    st.divider()

    # =====================================================
    # CLEAR CHAT
    # =====================================================

    if st.button("🗑️ Clear Chat", use_container_width=True):

        st.session_state.messages = [
            {
                "role": "system",
                "content": (
                    "You are a helpful and friendly AI assistant. "
                    "Give clear, simple and accurate answers. "
                    "Explain difficult topics in an easy-to-understand way."
                )
            }
        ]

        st.rerun()