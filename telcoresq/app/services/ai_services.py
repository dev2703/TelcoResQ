from openai import OpenAI
from telcoresq.config import settings
import functools
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from telcoresq.config import prompts
import numpy as np
from langchain.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain_openai import OpenAIEmbeddings

@functools.lru_cache(maxsize=None)
def get_embeddings(texts, model=settings.EMBEDDING_MODEL, api_key=None):
    """
    Generates embeddings for a list of texts using OpenAI.
    The `texts` parameter is a tuple to be hashable for caching.
    """
    if not texts:
        return []

    # Use the key from the function argument if provided, otherwise from settings
    final_api_key = api_key or settings.OPENAI_API_KEY
    if not final_api_key:
        raise ValueError("OpenAI API key is not set. Please provide it in the sidebar.")

    # Note: The underlying `openai` library automatically uses the OPENAI_API_KEY
    # environment variable if the api_key argument is not provided.
    # We are being explicit here to allow for UI-based key entry.
    client = OpenAI(api_key=final_api_key)
    
    # Replace newlines with spaces as recommended by OpenAI for embedding models.
    processed_texts = [str(text).replace("\\n", " ") for text in texts if text]

    if not processed_texts:
        return []

    response = client.embeddings.create(input=processed_texts, model=model)
    return [item.embedding for item in response.data]

def get_sentiment(text, model=settings.LLM_MODEL, api_key=None):
    """
    Analyzes the sentiment of a single text string using an LLM.
    """
    if not text:
        return None
    
    final_api_key = api_key or settings.OPENAI_API_KEY
    if not final_api_key:
        raise ValueError("OpenAI API key is not set.")

    try:
        llm = ChatOpenAI(temperature=0, model_name=model, api_key=final_api_key)
        prompt = PromptTemplate(
            input_variables=["response"],
            template=prompts.SENTIMENT_ANALYSIS_PROMPT,
        )
        chain = LLMChain(llm=llm, prompt=prompt)
        result = chain.run(response=text)
        return result
    except Exception as e:
        print(f"An error occurred during sentiment analysis: {e}")
        return None

def get_themes(responses, model=settings.LLM_MODEL, api_key=None):
    """
    Extracts themes from a list of survey responses.
    """
    if not responses:
        return None
    
    final_api_key = api_key or settings.OPENAI_API_KEY
    if not final_api_key:
        raise ValueError("OpenAI API key is not set.")

    # Simple batching to handle large number of responses
    # In a real app, this would be more sophisticated
    batched_responses = "\n".join(responses[:50]) # Limit to 50 for now

    try:
        llm = ChatOpenAI(temperature=0.7, model_name=model, api_key=final_api_key)
        prompt = PromptTemplate(
            input_variables=["responses"],
            template=prompts.THEME_EXTRACTION_PROMPT,
        )
        chain = LLMChain(llm=llm, prompt=prompt)
        result = chain.run(responses=batched_responses)
        return result
    except Exception as e:
        print(f"An error occurred during theme extraction: {e}")
        return None

def get_summary(responses, model=settings.LLM_MODEL, api_key=None):
    """
    Generates a summary from a list of survey responses.
    """
    if not responses:
        return None

    final_api_key = api_key or settings.OPENAI_API_KEY
    if not final_api_key:
        raise ValueError("OpenAI API key is not set.")

    batched_responses = "\n".join(responses[:50])

    try:
        llm = ChatOpenAI(temperature=0.7, model_name=model, api_key=final_api_key)
        prompt = PromptTemplate(
            input_variables=["responses"],
            template=prompts.SUMMARY_GENERATION_PROMPT,
        )
        chain = LLMChain(llm=llm, prompt=prompt)
        result = chain.run(responses=batched_responses)
        return result
    except Exception as e:
        print(f"An error occurred during summary generation: {e}")
        return None

def search_similar_responses(query, index, documents, k=3):
    """
    Searches for the most similar responses to a query using a FAISS index.
    """
    if index is None:
        return None, None

    query_embedding = get_embeddings([query])[0]
    distances, indices = index.search(np.array([query_embedding]).astype('float32'), k)

    results = [documents[i] for i in indices[0]]
    return results, distances[0] 

def get_rag_chain(index, documents):
    """
    Creates a Retrieval-Augmented Generation (RAG) chain.
    """
    if index is None or not documents:
        return None

    # This is a hack. LangChain's FAISS wrapper needs a way to map
    # the index back to the text. We create a temporary mapping.
    # A real implementation would use a more robust VectorStore that stores metadata.
    doc_mapping = {i: doc for i, doc in enumerate(documents)}
    
    # We need to re-create the index with the document mapping for LangChain
    # This is inefficient but necessary for this simplified setup.
    # The embeddings function should be compatible with LangChain's expectations.
    embeddings_func = OpenAIEmbeddings(api_key=settings.OPENAI_API_KEY)

    # To use LangChain's FAISS, we need to provide it with texts and an embedding function.
    # Since we already have the index, this is not ideal. We will wrap the raw FAISS index.
    # This requires a bit of a workaround since LangChain wants to build it from texts.
    # A proper solution would use a LangChain-compatible vector store from the beginning.
    
    # Let's try to wrap the existing index. This part is tricky.
    # The FAISS wrapper in LangChain expects to be created with `from_texts`.
    # Let's see if we can manually construct it.
    
    # For simplicity, we'll stick to a simpler RAG implementation for now without the full chain.
    # We will get the results from our search and then feed them to a separate LLM call.
    return None # Placeholder for now

def get_answer_from_context(query, context_documents, model=settings.LLM_MODEL, api_key=None):
    """
    Generates an answer to a query based on a list of context documents.
    """
    if not context_documents:
        return "Could not find any relevant information."

    final_api_key = api_key or settings.OPENAI_API_KEY
    if not final_api_key:
        raise ValueError("OpenAI API key is not set.")

    context = "\n---\n".join(context_documents)
    
    template = f"""
    Answer the following query based on the provided context of survey responses.
    If the context does not contain the answer, say so.

    Query: {query}

    Context:
    {context}

    Answer:
    """

    try:
        llm = ChatOpenAI(temperature=0, model_name=model, api_key=final_api_key)
        response = llm.invoke(template)
        return response.content
    except Exception as e:
        print(f"An error occurred during answer generation: {e}")
        return "There was an error generating the answer." 