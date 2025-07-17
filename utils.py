import os
import re
import spacy
from sentence_transformers import SentenceTransformer, util

# ✅ Load NLP models once
nlp = spacy.load("en_core_web_sm")
model = SentenceTransformer("all-MiniLM-L6-v2")

def clean_text(text):
    """Remove extra spaces and newlines."""
    text = re.sub(r'\n+', ' ', text)
    text = re.sub(r'\s+', ' ')
    return text.strip()

def is_allowed_file(filename):
    allowed_extensions = {'.pdf', '.txt'}
    ext = os.path.splitext(filename)[1].lower()
    return ext in allowed_extensions

def get_file_extension(filename):
    return os.path.splitext(filename)[1].lower()

# ✅ Load strong verbs from resources folder
def load_strong_verbs(filepath="resources/strong_verbs.txt"):
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            return set([line.strip().lower() for line in f if line.strip()])
    else:
        return set()

# ✅ Suggest improvements based on semantic similarity to strong verbs
def extract_weak_verbs_and_suggestions(text, strong_verbs_set):
    doc = nlp(text)
    suggestions = []

    for token in doc:
        # ✅ Focus only on verbs and auxiliary verbs
        if token.pos_ in ["VERB", "AUX"]:
            word = token.text.lower()
            lemma = token.lemma_.lower()

            # ✅ Skip if the word is already strong
            if lemma in strong_verbs_set or word in strong_verbs_set:
                continue

            # ✅ Encode the weak verb using MiniLM
            token_embedding = model.encode(word, convert_to_tensor=True)

            # ✅ List to store (strong_verb, similarity_score) tuples
            top_matches = []

            # ✅ Compare with all strong verbs using semantic similarity
            for strong_verb in strong_verbs_set:
                strong_embedding = model.encode(strong_verb, convert_to_tensor=True)
                sim = util.pytorch_cos_sim(token_embedding, strong_embedding).item()
                top_matches.append((strong_verb, sim))

            # ✅ Sort strong verbs by similarity (highest first)
            top_matches.sort(key=lambda x: x[1], reverse=True)

            # ✅ Extract top 3 most similar strong verbs
            best_3 = [match[0] for match in top_matches[:3]]

            # ✅ Get similarity score of the most similar verb
            best_sim = top_matches[0][1] if top_matches else 0

            # ✅ Suggest alternatives only if top similarity is below threshold (weak verb)
            if best_sim < 0.75:
                suggestions.append({
                    "original": token.text,         # weak verb in resume
                    "suggested": best_3             # top 3 strong alternatives
                })

    return suggestions


    return suggestions

