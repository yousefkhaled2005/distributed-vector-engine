"""
High-Throughput Vector Ingestion for Arabic Legal Corpus
Architect: Yousef Khaled (Senior AI Systems Architect)
"""

import chromadb
from chromadb.config import Settings
import time

def ingest_legal_corpus():
    print("Initializing high-performance distributed vector engine...")
    client = chromadb.PersistentClient(path="./legal_chroma_db")
    
    collection = client.get_or_create_collection(
        name="egyptian_legal_corpus",
        metadata={"hnsw:space": "cosine", "hnsw:construction_ef": 200, "hnsw:M": 32}
    )

    documents = [
        "عقد العمل الفردي هو اتفاق بين صاحب العمل والعامل يتعهد فيه الأخير بالعمل تحت إشراف صاحب العمل.",
        "ساعات العمل اليومية الفعلية لا يجوز أن تتجاوز 8 ساعات يومياً مع وجوب منح ساعة راحة لتناول الطعام.",
        "مكافأة نهاية الخدمة تُصرف بواقع أجر نصف شهر عن كل سنة من السنوات الخمس الأولى، وأجر شهر عن السنوات اللاحقة.",
        "الإجازة السنوية بأجر كامل مدتها 21 يوماً عن كل سنة خدمة كاملة وتزاد إلى 30 يوماً بعد 10 سنوات."
    ]
    ids = [f"statute_{i+1}" for i in range(len(documents))]
    metadatas = [{"category": "Labor_Law", "jurisdiction": "Egypt"} for _ in range(len(documents))]

    start = time.time()
    collection.add(documents=documents, ids=ids, metadatas=metadatas)
    print(f"Successfully indexed {len(documents)} Arabic legal statutes in {time.time() - start:.3f}s")

    # Semantic Query
    results = collection.query(query_texts=["ما هي ساعات العمل المقررة قانوناً؟"], n_results=1)
    print("Top matched statute:", results["documents"][0][0])

if __name__ == "__main__":
    ingest_legal_corpus()
