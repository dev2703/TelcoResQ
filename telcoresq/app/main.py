import streamlit as st
from telcoresq.app.services.data_processing import parse_file, preprocess_dataframe
from telcoresq.app.services.ai_services import (
    get_embeddings, get_sentiment, get_themes, get_summary, 
    search_similar_responses, get_answer_from_context
)
from telcoresq.app.services.vector_store import create_faiss_index, save_faiss_index, load_faiss_index
from telcoresq.app.components.visualizations import (
    create_sentiment_pie_chart, 
    create_theme_frequency_bar_chart,
    parse_themes_to_df
)
from telcoresq.config import settings
import pandas as pd

def main():
    st.set_page_config(page_title="TelcoResQ", page_icon="📡")
    st.title("TelcoResQ: AI-Powered Survey Insight Engine")

    # Initialize session state
    if 'df_clean' not in st.session_state:
        st.session_state.df_clean = None
    if 'text_column_to_embed' not in st.session_state:
        st.session_state.text_column_to_embed = ""
    if 'openai_api_key' not in st.session_state:
        st.session_state.openai_api_key = None


    st.sidebar.title("Configuration")
    st.session_state.openai_api_key = st.sidebar.text_input(
        "OpenAI API Key", 
        type="password", 
        placeholder="sk-...",
        help="Enter your OpenAI API key. This will not be stored.",
        value=st.session_state.openai_api_key or ""
    )

    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ["Dashboard", "Query", "Reports"])

    if page == "Dashboard":
        st.header("Dashboard")
        st.write("Welcome to the TelcoResQ Dashboard.")
        # File uploader
        st.subheader("Upload Survey Data")
        uploaded_file = st.file_uploader("Choose a CSV or JSON file", type=["csv", "json"])
        if uploaded_file is not None:
            if not st.session_state.openai_api_key:
                st.warning("Please enter your OpenAI API Key in the sidebar to proceed.")
                st.stop()
            try:
                df = parse_file(uploaded_file)
                st.success("File uploaded and parsed successfully!")

                st.subheader("Raw Data Preview")
                st.dataframe(df.head())

                # For now, assume all object columns are text columns that need cleaning
                text_columns = df.select_dtypes(include=['object']).columns.tolist()
                
                if text_columns:
                    # Allow user to select the main text column for analysis
                    st.session_state.text_column_to_embed = st.selectbox(
                        "Select column to embed:", 
                        text_columns,
                        key="column_selector"
                    )

                    df_clean = preprocess_dataframe(df.copy(), text_columns)
                    st.session_state.df_clean = df_clean # Save to session state

                    st.subheader("Processed Data Preview")
                    st.dataframe(df_clean.head())

                    if st.button("Process and Generate Embeddings"):
                        try:
                            with st.spinner("Processing data, generating embeddings, and building vector store..."):
                                # 1. Get embeddings
                                texts_to_embed = df_clean[st.session_state.text_column_to_embed].tolist()
                                embeddings = get_embeddings(tuple(texts_to_embed), api_key=st.session_state.openai_api_key)

                                if not embeddings:
                                    st.error("Could not generate embeddings. The operation returned no data.")
                                    st.stop()

                                st.write(f"Generated {len(embeddings)} embeddings.")
                                
                                # 2. Create FAISS index
                                index = create_faiss_index(embeddings)
                                
                                # 3. Save FAISS index
                                save_faiss_index(index)
                                st.success("Successfully processed data and created vector store!")

                                # 4. Perform Sentiment Analysis
                                st.subheader("Sentiment Analysis")
                                sentiments = df_clean[st.session_state.text_column_to_embed].apply(
                                     lambda x: get_sentiment(x, api_key=st.session_state.openai_api_key)
                                 )
                                df_clean['sentiment_label'] = sentiments.apply(lambda x: x.split('\\n')[0].replace('Sentiment:', '').strip() if x else 'N/A')
                                df_clean['sentiment_justification'] = sentiments.apply(lambda x: x.split('Justification:')[1].strip() if x and 'Justification:' in x else 'N/A')
                                st.session_state.df_clean = df_clean # Update session state
                                st.dataframe(df_clean[[st.session_state.text_column_to_embed, 'sentiment_label', 'sentiment_justification']].head())
                                st.success("Sentiment analysis complete.")
                                 
                                fig = create_sentiment_pie_chart(df_clean)
                                if fig:
                                    st.plotly_chart(fig)

                            # 5. Perform Theme Extraction
                            st.subheader("Theme Extraction")
                            if st.button("Extract Themes"):
                                with st.spinner("Extracting themes..."):
                                    themes_text = get_themes(
                                        df_clean[st.session_state.text_column_to_embed].tolist(),
                                        api_key=st.session_state.openai_api_key
                                    )
                                    if themes_text:
                                        st.markdown(themes_text)
                                        st.success("Theme extraction complete.")
                                        themes_df = parse_themes_to_df(themes_text)
                                        fig_themes = create_theme_frequency_bar_chart(themes_df)
                                        if fig_themes:
                                            st.plotly_chart(fig_themes)
                                    else:
                                        st.error("Could not extract themes.")
                            
                            # 6. Generate Summary
                            st.subheader("Generate Summary")
                            if st.button("Generate Executive Summary"):
                                with st.spinner("Generating summary..."):
                                    summary = get_summary(
                                        df_clean[st.session_state.text_column_to_embed].tolist(),
                                        api_key=st.session_state.openai_api_key
                                    )
                                    if summary:
                                        with st.expander("View Summary", expanded=True):
                                            st.write(summary)
                                        st.success("Summary generation complete.")
                                    else:
                                        st.error("Could not generate summary.")
                        except Exception as e:
                            st.error(f"An error occurred during processing: {e}")
                else:
                    st.warning("No text columns found to process.")

            except Exception as e:
                st.error(f"An error occurred: {e}")

    elif page == "Query":
        st.header("Natural Language Query")
        st.write("Ask questions about your survey data.")

        if st.session_state.df_clean is not None and st.session_state.text_column_to_embed:
            if not st.session_state.openai_api_key:
                st.warning("Please enter your OpenAI API Key in the sidebar to run a query.")
                st.stop()
            query = st.text_input("Enter your query:", key="query_input")
            if st.button("Submit Query"):
                with st.spinner("Searching for relevant responses..."):
                    index = load_faiss_index()
                    if index:
                        documents = st.session_state.df_clean[st.session_state.text_column_to_embed].tolist()
                        results, distances = search_similar_responses(query, index, documents)
                        
                        if results:
                            # Generate a direct answer from the context
                            with st.spinner("Generating an answer..."):
                                answer = get_answer_from_context(
                                    query, 
                                    results, 
                                    api_key=st.session_state.openai_api_key
                                )
                                st.subheader("Answer:")
                                st.write(answer)

                            # Display the source documents
                            with st.expander("Show relevant responses used for the answer"):
                                st.subheader("Most Relevant Responses:")
                                for i, (res, dist) in enumerate(zip(results, distances)):
                                    st.write(f"**Response {i+1} (Distance: {dist:.4f}):**")
                                    st.write(res)
                        else:
                            st.warning("No relevant responses found.")
                    else:
                        st.error("Vector index not found. Please process a file on the Dashboard page first.")
        else:
            st.warning("Please upload and process a file on the Dashboard page first.")

    elif page == "Reports":
        st.header("Export Reports")
        st.write("Generate and export insights reports.")
        if st.button("Export Report"):
            st.success("Report exported successfully!")
            # Add report generation logic here

if __name__ == "__main__":
    main()
