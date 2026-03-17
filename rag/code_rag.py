from openai import OpenAI

class CodeRAG:

    def __init__(self, index):

        self.index = index

        self.client = OpenAI(
            #api_key=os.environ["GROQ_API_KEY"],
            api_key="",
            base_url="https://api.groq.com/openai/v1"
        )

    def build_context(self, chunks):

        context = ""

        for c in chunks:

            context += f"""
    File: {c['file']}
    Lines: {c['start_line']} - {c['end_line']}
    Type: {c['type']}

    Code:
    {c['code']}

    -------------------
    """

        return context

    def ask(self, question):

        retrieved_chunks = self.index.search(question, k=5)

        """print("\nRetrieved chunks:\n")

        for c in retrieved_chunks:
            print(f"{c['file']}:{c['start_line']}-{c['end_line']}") """

        context = self.build_context(retrieved_chunks)

        prompt = f"""
You are an expert software engineer.

Use the following code snippets to answer the question.

{context}

Question:
{question}

Explain clearly how the code works.
"""

        response = self.client.chat.completions.create(

            model="llama-3.3-70b-versatile",

            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        return response.choices[0].message.content
