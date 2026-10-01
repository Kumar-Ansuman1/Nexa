from src.embeddings.models.jina import embed_text


vector = embed_text("revenue")

print("Dimensions:", len(vector))
print("First 5 values:", vector[:5])
