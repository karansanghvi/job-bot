import os
# from flask import session
from flask import Flask, request, render_template
from parser import parse_resume
from matcher import compute_bert_similarity, compute_tfidf_similarity, get_feedback
from utils import is_allowed_file, clean_text, load_strong_verbs, extract_weak_verbs_and_suggestions
from graphs import generate_keyword_bar_chart, generate_resume_quality_line_chart



UPLOAD_FOLDER = 'uploads'
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        jd = request.form['jobdesc']
        file = request.files['resume']

        if not is_allowed_file(file.filename):
            return "Unsupported file type. Only PDF and TXT are allowed.", 400

        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)

        resume = parse_resume(filepath)
        resume_text_to_compare = " ".join(resume['skills']) if resume['skills'] else resume['text']

        tfidf_score, keywords = compute_tfidf_similarity(resume_text_to_compare, jd)
        bert_score = compute_bert_similarity(resume_text_to_compare, jd)
        matched, missing = get_feedback(resume, jd, keywords)

        # ✅ Load strong verbs from resources and extract weak verb suggestions
        strong_verbs_set = load_strong_verbs("resources/strong_verbs.txt")
        weak_verb_suggestions = extract_weak_verbs_and_suggestions(resume['text'], strong_verbs_set)

        def get_match_level(bert, tfidf):
            if bert >= 65 or tfidf >= 30:
                return "🔥 Excellent Match"
            elif bert >= 50 or tfidf >= 25:
                return "✅ Good Match"
            elif bert >= 35 or tfidf >= 15:
                return "⚠️ Moderate Match"
            else:
                return "❌ Weak Match"

        match_level = get_match_level(bert_score * 100, tfidf_score * 100)

        # session['matched_keywords'] = matched
        # session['missing_keywords'] = missing
        # session['tfidf_score'] = round(tfidf_score * 100, 2)
        # session['bert_score'] = round(bert_score * 100, 2)
        # session['keyword_score'] = round(len(matched) / max(1, len(matched) + len(missing)) * 100, 2)
        # session['verb_score'] = round(100 - (len(weak_verb_suggestions) / max(1, len(resume_text_to_compare.split('.'))) * 100), 2)
        # session['bullet_score'] = 50  # Or calculate dynamically


        return render_template(
            'result.html',
            tfidf_score=round(tfidf_score * 100, 2),
            bert_score=round(bert_score * 100, 2),
            matched=matched,
            missing=missing,
            email=resume.get('email', 'Not found'),
            match_level=match_level,
            weak_verb_suggestions=weak_verb_suggestions  # ✅ passed to HTML
        )

    uploaded_files = os.listdir(app.config['UPLOAD_FOLDER'])
    return render_template('index.html', uploaded_files=uploaded_files)


@app.route("/graphs")
def show_graphs():
    pass
    # These values should be passed using session or from result page if needed
    # from flask import session

    # matched_keywords = session.get('matched_keywords', [])
    # missing_keywords = session.get('missing_keywords', [])
    # tfidf_score = session.get('tfidf_score', 0)
    # bert_score = session.get('bert_score', 0)
    # keyword_score = session.get('keyword_score', 0)
    # verb_score = session.get('verb_score', 0)
    # bullet_score = session.get('bullet_score', 0)

    # bar_chart = generate_keyword_bar_chart(matched, missing)
    # line_chart = generate_resume_quality_line_chart(tfidf_score, bert_score, keyword_score, verb_score, bullet_score)

    # return render_template("graphs.html", bar_chart=bar_chart, line_chart=line_chart)



@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == "__main__":
    app.run(debug=True)






