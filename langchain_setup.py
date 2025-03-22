from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from mistral_client import get_mistral_response

# Define the prompt template
prompt = PromptTemplate(
    input_variables=["context", "query"],
    template="""
    You are an AI assistant for Hôtel California. Use the provided context to answer the query:
    Context: {context}
    Query: {query}
    """
)

# Set up the LangChain
def create_chain():
    def mistral_llm(query):
        return get_mistral_response(query)

    chain = LLMChain(llm=mistral_llm, prompt=prompt)
    return chain