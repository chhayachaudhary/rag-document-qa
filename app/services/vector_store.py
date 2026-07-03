import chromadb
from chromadb.utils import embedding_functions

chroma_client =chromadb.PersistentClient(path="./chroma_db")

embedding_functions =embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="all-MiniLM-L6-v2"
)

def get_collection(collection_name: str):
    return chroma_client.get_or_create_collection(
        name= collection_name,
        embedding_function=embedding_functions
    )

def store_chunks(chunks: list[str], filename: str)-> int:
    collection_name = filename.replace(".pdf","").replace(" ","_").lower()
    collection= get_collection(collection_name)
    ids =[f"{collection_name}_chunk_{i}" for i in range(len(chunks))]

    collection.add(
        documents =chunks,
        ids =ids
    )

    return len(chunks)

def search_chunks(query: str, filename: str, n_results: int = 3) -> list[str]:
    collection_name = filename.replace(".pdf", "").replace(" ", "_").lower()
    collection = get_collection(collection_name)
    results = collection.query(query_texts=[query], n_results=n_results)
    return results["documents"][0]

def search_all_chunks(query: str, filenames: list[str], n_results_per_file: int = 3) -> list[str]:
    all_chunks = []
    for filename in filenames:
        try:
            chunks = search_chunks(query, filename, n_results_per_file)
            all_chunks.extend(chunks)
        except Exception:
            continue
    return all_chunks