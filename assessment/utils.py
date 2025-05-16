import openai
from os import environ

def generate_embeddings(answers):
    """
    Generate embeddings for user answers using OpenAI's embedding model.
    """
    try:
        formatted_text = ' '.join([f'Q{q}: {a}' for q, a in answers.items()])
        response = openai.Embedding.create(
            input=formatted_text,
            model="text-embedding-ada-002"
        )
        embedding = response['data'][0]['embedding']
        return embedding
    except Exception as e:
        print(f'Error generating embeddings: {e}')
        return None
