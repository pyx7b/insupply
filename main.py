from materialsearch import SemanticSearch

# Example Usage
if __name__ == "__main__":
    # Initialize search engine
    search_engine = SemanticSearch(data_file='materials.json')

    # Example search queries
    queries = ["metal pole", "engine oil"]
    results = search_engine.search(queries)

    # Print results
    for result in results:
        print(f"Query: {result['query']}")
        for match in result['matches']:
            print(f"  - {match}")