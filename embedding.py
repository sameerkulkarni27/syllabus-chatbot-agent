from langchain_openai import OpenAIEmbeddings
import faiss
from langchain_community.docstore.in_memory import InMemoryDocstore
from langchain_community.vectorstores import FAISS
from config import EMBEDDING_MODEL

class Embedding:
    def __init__(self):
        print(f"Initializing embeddings model: {EMBEDDING_MODEL}")
        self.embeddings = OpenAIEmbeddings(model=EMBEDDING_MODEL)
        self.vector_store = None

    def create_vector_store(self, split_chunks):
        embedding_dim = len(self.embeddings.embed_query("hello world"))
        index = faiss.IndexFlatL2(embedding_dim)

        self.vector_store = FAISS(
            embedding_function=self.embeddings,
            index=index,
            docstore=InMemoryDocstore(),
            index_to_docstore_id={},
        )

        self.vector_store.add_texts(split_chunks)

        print(f"Vector store created with {len(split_chunks)} embeddings")
        return self.vector_store