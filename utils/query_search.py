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
            You are Lee, a chatbot that can answer queries and questions from users.
            You have a database of documents that you can search through to find the answer.
            The user can also ask question that are not in the database of documents.
            If the question is not clear, you can ask for more information.
            User asks: "{}"
            In your response, you can include headings, page number, figures, and references if available.
            Use html tags to make the response more readable.
            If the answer is long, you can answer point by point using the html tags.
            There is no need to reply with a "Response:" or "Answer:" prefix.

        """

        template = template.format(self.query)

        query_engine = self.index.as_query_engine(similarity_top_k=5, verbose=True)
        reponse = query_engine.query(template)
        return reponse
