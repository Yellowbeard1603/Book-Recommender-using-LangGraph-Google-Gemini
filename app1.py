import streamlit as st
import os
from core_logic1 import app, BookState, set_llm 
from langchain.chat_models import init_chat_model

st.set_page_config(page_title="Book Recommender", page_icon="📚")
st.title("📚 Book Recommender using LangGraph")

api_key = st.text_input("🔐 Enter your Google Generative AI API Key:", type="password")

if api_key:
    os.environ["GOOGLE_API_KEY"] = api_key

    try:
        # ✅ Initialize the LLM instance
        llm1 = init_chat_model(
            model="gemini-2.0-flash",
            model_provider="google_genai",
            temperature=0.0
        )

        # ✅ Inject the model into the core logic module
        set_llm(llm1)

        user_query = st.text_input("📘 What kind of book do you want?", "Suggest the best science fiction book")

        if st.button("Generate Recommendation"):
            with st.spinner("Thinking..."):
                initial_state: BookState = {"user_query": user_query}
                final_state = app.invoke(initial_state)

            st.subheader("📖 Top Book Recommendations")
            if "presentation" in final_state:
                st.write("✅", final_state["presentation"])
            else:
                st.warning("No recommendations found.")
    except Exception as e:
        st.error(f"❌ Could not initialize model: {e}")
else:
    st.info("🔑 Please enter your API key to start.")
