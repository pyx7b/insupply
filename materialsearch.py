import numpy as np
from sentence_transformers import SentenceTransformer
from scipy.spatial.distance import cdist
import json

# Load data and model
class SemanticSearch:
    def __init__(self, data_file, model_name='all-MiniLM-L6-v2'):
        self.data = self._load_data(data_file)
        self.model = SentenceTransformer(model_name)
        self.embeddings = self._generate_embeddings()

    def _load_data(self, data_file):
        """Load material data from a JSON file."""
        import json
        with open(data_file, 'r') as f:
            return json.load(f)

    def _generate_embeddings(self):
        """Generate embeddings for all descriptions."""
        descriptions = [item['description'] for item in self.data]
        return self.model.encode(descriptions)

    def _cosine_similarity_to_percentage(self, cosine_similarity):
        """Convert cosine similarity score to a percentage (0-100%)."""
        return round(((1-cosine_similarity) * 100),2)

    def search(self, queries, top_k=5):
        """Perform semantic search for a list of queries."""
        query_embeddings = self.model.encode(queries)
        distances = cdist(query_embeddings, self.embeddings, metric='cosine')
        results = []

        for i, query in enumerate(queries):
            ranked_indices = np.argsort(distances[i])[:top_k]
            matches = [
                {
                    "material_number": self.data[idx]['material_number'],
                    "description": self.data[idx]['description'],
                    "score": 1 - distances[i, idx],  # Cosine similarity (1 - distance)
                    "percent": self._cosine_similarity_to_percentage(distances[i, idx])
                }
                for idx in ranked_indices
            ]
            results.append({"query": query, "matches": matches})

        json_results = json.dumps(results)
        return json_results