from sentence_transformers import SentenceTransformer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import spacy
from spacy.lang.en.stop_words import STOP_WORDS

# ✅ MODIFIED: Added for fuzzy keyword matching
from difflib import SequenceMatcher

# ✅ Initialize spaCy and BERT model once
nlp = spacy.load("en_core_web_sm")
model = SentenceTransformer('all-MiniLM-L6-v2')

# ✅ TF-IDF similarity function
def compute_tfidf_similarity(resume_text, jd_text):
    tfidf = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf.fit_transform([resume_text, jd_text])
    score = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
    keywords = tfidf.get_feature_names_out()
    return score, keywords

# ✅ BERT similarity function
def compute_bert_similarity(resume_text, jd_text):
    embeddings = model.encode([resume_text, jd_text])
    score = cosine_similarity([embeddings[0]], [embeddings[1]])[0][0]
    return score

# ✅ Extract clean keywords from job description text
def get_keywords(text):
    doc = nlp(text.lower())
    return set([
        token.lemma_ for token in doc
        if token.is_alpha and token.lemma_ not in STOP_WORDS
        and token.pos_ in ['NOUN', 'ADJ', 'VERB']
    ])

# ✅ MODIFIED: Added helper to compare similarity between words
def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

# ✅ FINAL FIX: Better fuzzy keyword matching using full resume content + filtered JD terms
def get_feedback(resume, jd_text, keywords):
    jd_keywords = get_keywords(jd_text)

    # ✅ NEW: Keep only keywords that are nouns, verbs, or important tech terms
    important_keywords = {kw for kw in jd_keywords if len(kw) > 2 and kw.lower() not in ['good', 'end', 'join', 'look', 'use', 'like', 'want']}

    # ✅ Combine resume skills and tokenized resume text
    resume_skills = resume.get('skills', [])
    resume_text = resume.get('text', '')
    resume_tokens = get_keywords(resume_text)
    all_resume_terms = set(resume_skills) | resume_tokens

    matched = set()

    # ✅ NEW: Match JD keywords against resume content using fuzzy match
    for kw in important_keywords:
        for term in all_resume_terms:
            if similar(kw.lower(), term.lower()) >= 0.85:
                matched.add(kw)
                break

    # ✅ Limit to most meaningful missing keywords
    missing = sorted(list(important_keywords - matched))[:30]  # Top 30 only

    return sorted(matched), missing
