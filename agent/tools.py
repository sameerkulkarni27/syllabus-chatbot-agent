from langchain_core.tools import tool


def initialize_tools(vector_store):
    """
    Initialize tools for the syllabus agent. Provide the query_syllabus_info()
    function with the vector_store as well.
    
    Args:
        vector_store: FAISS vector store containing syllabus chunks
        
    Returns:
        List of tools
    """

    @tool
    def query_syllabus_info(query):
        """
        Retrieve relevant information from the syllabus.
        
        Args:
            query: The question or topic to search for in the syllabus
            
        Returns:
            Tuple of (serialized context, retrieved documents)
        """


        retrieved_docs = vector_store.similarity_search(query, k=4)

        serialized = "\n\n".join(
            (f"Source: {doc.metadata}\nContent: {doc.page_content}")
            for doc in retrieved_docs
        )

        return serialized, retrieved_docs

    return [query_syllabus_info]