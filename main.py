import os

from ingestion.repo_ingestor import RepoIngestor, list_code_files
from rag.chunker import chunk_files
from embeddings.embedding_index import CodeEmbeddingIndex
from rag.code_rag import CodeRAG

repo_url = "https://github.com/keycloak/keycloak"

index_dir = "vector_indexes"
os.makedirs(index_dir, exist_ok=True)
index_path = os.path.join(
    index_dir,
    f"{repo_url.split('.com/')[-1].replace('/', '-')}.pkl"
)

index = CodeEmbeddingIndex()
# se índice já existir → carregar
if os.path.exists(index_path):

    print("Loading existing index...")

    index.load(index_path)

else:

    print("Building index (first run only)...")

    ingestor = RepoIngestor(repo_url)

    repo_path = ingestor.clone_repo()

    files = list_code_files(repo_path)

    chunks = chunk_files(files)

    index.build_index(chunks)

    index.save(index_path)

rag = CodeRAG(index)

question = "Como eu executo a principal funcionalidade deste código?"

answer = rag.ask(question)

print("\nANSWER:\n")

print(answer)