from pinecone import Pinecone, ServerlessSpec
from langchain_pinecone import PineconeVectorStore
from langchain_openai import OpenAIEmbeddings
from config import PINECONE_API_KEY, PINECONE_INDEX_NAME, EMBEDDING_MODEL
import time

class PineconeClient:
    """Initialize Pinecone vector store to store"""

    def __init__(self):
        """Initialize a Pinecone client with your API key"""
        self.pc = Pinecone(api_key=PINECONE_API_KEY)
        self.index_name = PINECONE_INDEX_NAME
        self.embeddings = OpenAIEmbeddings(model=EMBEDDING_MODEL)

        if self.index_name not in self.pc.list_indexes().names():
            print(f"📝 Creating index '{self.index_name}'...")
            self.pc.create_index(
                name=self.index_name,
                dimension=3072,
                metric="cosine",
                spec=ServerlessSpec(
                    cloud="aws",
                    region="us-east-1"
                )
            )

            # Wait for the upserted vectors to be indexed
            while not self.pc.describe_index(self.index_name).status['ready']:
                time.sleep(1)
            print("✅ Index created")
        else:
            print(f"✅ Using existing index '{self.index_name}'")

        self.index = self.pc.Index(self.index_name)

    def upload_chunks(self, chunks, namespace):
        """Upload chunks to Pinecone with namespace ID"""

        vector_store = PineconeVectorStore.from_texts(
            texts=chunks,
            embedding=self.embeddings,
            index_name=self.index_name,
            namespace=namespace
        )

        return vector_store

    def get_vectorstore(self, namespace):
        """Load vectorstore in Pinecone using namespace"""

        vector_store = PineconeVectorStore(
            index_name=self.index_name,
            embedding=self.embeddings,
            namespace=namespace
        )
        
        return vector_store

    def list_namespaces(self):
        """List all stored syllabi"""
        stats = self.index.describe_index_stats()
        
        return list(stats.get('namespaces', {}).keys())
            
