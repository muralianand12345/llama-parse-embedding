class GetResults:
    def __init__(self, query, index):
        self.query = query
        self.index = index

    def simple_search(self):
        """
        Search the query in the index and return the results.

        Returns:
            List: The search results.
        """

        template = """
            You are Lee, a chatbot that can answer queries from users.
            You have a database of documents that you can search through.
            If the question is not clear, you can ask for more information.
            User asks: "{}"
            Do not answer if the question is not safe for work.
            In your response, you should include headings, page number, figures, and references.
        """

        template = template.format(self.query)

        query_engine = self.index.as_query_engine(similarity_top_k=5, verbose=True)
        reponse = query_engine.query(template)
        return reponse
