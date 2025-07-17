
## 📂 Directory Structure

See full directory structure 


```
JD_Resume_Matcher/
├── app.py                  # Main Flask app
├── matcher.py              # TF-IDF & BERT-based similarity and keyword feedback
├── parser.py               # Resume parsing using spaCy
├── utils.py                # Utility functions like cleaning, file type check
├── graph_generator.py      # Generates bar and line graphs using matplotlib
├── requirements.txt        # Python dependencies
├── README.md               # Project documentation (you’re reading this)

├── uploads/                # Uploaded resumes (PDF/TXT)

├── templates/              # Jinja2 HTML templates
│   ├── index.html          # Homepage - Resume upload + JD input
│   ├── result.html         # Result page - scores, keywords, suggestions
│   ├── graphs.html         # Graphs page - visual insights
│   └── about.html          # About project and usage

├── static/
│   └── style.css           # Custom CSS (including background animation)
```
