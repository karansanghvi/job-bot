# graphs.py

import matplotlib.pyplot as plt
import io
import base64

# Converts Matplotlib figure to base64 string for embedding in HTML
def fig_to_base64(fig):
    buf = io.BytesIO()
    fig.tight_layout()
    fig.savefig(buf, format="png")
    buf.seek(0)
    image_base64 = base64.b64encode(buf.read()).decode("utf-8")
    plt.close(fig)
    return f"data:image/png;base64,{image_base64}"

# Generates a bar chart showing matched vs missing keywords
def generate_keyword_bar_chart(matched_keywords, missing_keywords):
    labels = ['Matched Keywords', 'Missing Keywords']
    counts = [len(matched_keywords), len(missing_keywords)]
    colors = ['#4CAF50', '#F44336']  # Green and Red

    fig, ax = plt.subplots()
    ax.bar(labels, counts, color=colors)
    ax.set_ylabel('Count')
    ax.set_title('Keyword Match Overview')

    return fig_to_base64(fig)

# Generates a line graph of multiple resume quality metrics
def generate_resume_quality_line_chart(tfidf_score, bert_score, keyword_score, verb_score, bullet_score):
    metrics = ['TF-IDF', 'BERT', 'Keyword Coverage', 'Action Verbs', 'Bullet Clarity']
    scores = [tfidf_score, bert_score, keyword_score, verb_score, bullet_score]

    fig, ax = plt.subplots()
    ax.plot(metrics, scores, marker='o', linestyle='-', color='#1f77b4')
    ax.set_ylim(0, 100)
    ax.set_ylabel('Score (%)')
    ax.set_title('Resume Quality Score Overview')

    return fig_to_base64(fig)
