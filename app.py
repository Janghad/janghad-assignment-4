from flask import Flask, render_template, request, jsonify
from sklearn.datasets import fetch_20newsgroups
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import nltk
from nltk.corpus import stopwords


nltk.download('stopwords')

app = Flask(__name__)


newsgroups = fetch_20newsgroups(subset='all')
documents = newsgroups.data


stop_words = stopwords.words('english')
vectorizer = TfidfVectorizer(stop_words=stop_words)
tfidf_matrix = vectorizer.fit_transform(documents)


lsa = TruncatedSVD(n_components=100)
lsa_matrix = lsa.fit_transform(tfidf_matrix)

def search_engine(query):
    """
    Function to search for top 5 similar documents given a query
    Input: query (str)
    Output: documents (list), similarities (list), indices (list)
    """

    query_vec = vectorizer.transform([query])
    query_lsa = lsa.transform(query_vec)

    similarities = cosine_similarity(query_lsa, lsa_matrix).flatten()
    
    ranked_indices = np.argsort(similarities)[::-1]
    
    top_5_indices = ranked_indices[:5]
    top_5_documents = []
    
    for i in top_5_indices:
        full_content = documents[i]
        lines = documents[i].split("\n")
        author = next((line for line in lines if line.lower().startswith("from:")), "Unknown Author")
        subject = next((line for line in lines if line.lower().startswith("subject:")), "No Subject")
        organization = next((line for line in lines if line.lower().startswith("organization:")), "No Organization")
        top_5_documents.append({
            "content": full_content,
            "author": author,
            "subject": subject,
            "organization": organization
        })
    
    top_5_similarities = similarities[top_5_indices].tolist()
    
    return top_5_documents, top_5_similarities, top_5_indices.tolist()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    query = request.json['query']  # Extract query from request
    documents, similarities, indices = search_engine(query)  # Perform search
    return jsonify({'documents': documents, 'similarities': similarities, 'indices': indices})

if __name__ == '__main__':
    app.run(debug=True)
