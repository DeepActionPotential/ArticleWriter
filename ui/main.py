import streamlit as st
from crewai import LLM
from core.article_manger import ArticleMaker

from crewai import LLM



from config import DefaultCFG

llm = LLM(
    model=DefaultCFG.llm_model,
    api_key=DefaultCFG.api_key
)


maker = ArticleMaker(llm)


# Page config
st.set_page_config(
    page_title="AI Article Writer",
    page_icon="📝",
    layout="wide"
)

# Initialize session state
if 'generated_article' not in st.session_state:
    st.session_state.generated_article = None


def main():
    st.title("🤖 AI Article Writer")
    st.markdown("""
    Generate well-structured, engaging blog articles using AI. 
    Just enter your topic and let the AI do the work!
    """)

    # Topic input
    topic = st.text_area(
        "Enter your article topic:",
        placeholder="e.g., '3 AI Websites That Will Blow Your Mind!'",
        help="Be specific and descriptive for better results"
    )

    # Generate button
    if st.button("Generate Article", type="primary", disabled=not topic):
        try:
            with st.spinner("🤖 Generating your article... This might take a few minutes."):
                # Initialize ArticleMaker
                
                # Generate article
                result = maker.make(topic)
                
                # Store in session state
                st.session_state.generated_article = result

        except Exception as e:
            st.error(f"Error generating article: {str(e)}")
            return

    # Display generated article
    if st.session_state.generated_article:
        st.success("✅ Article generated successfully!")
        
        # Create tabs for different views
        tab1, tab2 = st.tabs(["📝 Article Preview", "🔍 Structure Details"])
        
        with tab1:
            st.markdown(st.session_state.generated_article.pydantic.article)
            
            # Download button
            st.download_button(
                label="Download Article (Markdown)",
                data=st.session_state.generated_article.pydantic.article,
                file_name="generated_article.md",
                mime="text/markdown"
            )
        
        with tab2:
            st.json(st.session_state.generated_article.pydantic.model_dump())

if __name__ == "__main__":
    main()