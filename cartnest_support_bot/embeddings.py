import os
import pickle
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD
from sklearn.preprocessing import normalize

MODEL_SAVE_PATH = "data/embedding_model.pkl"


class TFIDFEmbedder:
    # Uses TF-IDF + SVD (LSA) — no PyTorch needed, works well for FAQ-style docs
    def __init__(self, n_components=384):
        self.n_components = n_components
        self.vectorizer = TfidfVectorizer(
            max_features=10000,
            ngram_range=(1, 2),
            sublinear_tf=True,
            strip_accents='unicode',
            analyzer='word',
            token_pattern=r'\w{2,}',
            min_df=1
        )
        self.svd = TruncatedSVD(n_components=min(n_components, 100), random_state=42)
        self.fitted = False

    def fit(self, corpus):
        print(f"Fitting TF-IDF on {len(corpus)} chunks...")
        tfidf_matrix = self.vectorizer.fit_transform(corpus)
        max_comp = min(tfidf_matrix.shape[0] - 1, tfidf_matrix.shape[1] - 1, self.n_components)
        self.svd.n_components = max_comp
        self.svd.fit(tfidf_matrix)
        self.fitted = True
        print(f"SVD fitted. Variance explained: {self.svd.explained_variance_ratio_.sum():.2%}")

    def embed(self, texts):
        if not self.fitted:
            raise RuntimeError("Call fit() before embed()")
        tfidf = self.vectorizer.transform(texts)
        reduced = self.svd.transform(tfidf)
        return normalize(reduced, norm='l2').astype(np.float32)

    def embed_one(self, text):
        return self.embed([text])[0].tolist()

    def embed_batch(self, texts):
        return self.embed(texts).tolist()

    def save(self, path=MODEL_SAVE_PATH):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'wb') as f:
            pickle.dump({'vectorizer': self.vectorizer, 'svd': self.svd, 'fitted': self.fitted}, f)

    def load(self, path=MODEL_SAVE_PATH):
        with open(path, 'rb') as f:
            state = pickle.load(f)
        self.vectorizer = state['vectorizer']
        self.svd = state['svd']
        self.fitted = state['fitted']
        return self


def get_embedder(corpus=None, force_refit=False):
    embedder = TFIDFEmbedder()
    if not force_refit and os.path.exists(MODEL_SAVE_PATH):
        embedder.load(MODEL_SAVE_PATH)
    elif corpus:
        embedder.fit(corpus)
        embedder.save(MODEL_SAVE_PATH)
    else:
        raise ValueError("No saved model and no corpus provided.")
    return embedder
