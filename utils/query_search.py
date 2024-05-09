class QuerySearch:
    def __init__(self, query, index):
        self.query = query
        self.index = index

    def simple_search(self):
        """
        Search the query in the index and return the results.

        Returns:
            List: The search results.
        """
        query_engine = self.index.as_query_engine()
        reponse = query_engine.query(self.query)
        return reponse
