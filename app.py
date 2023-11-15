from flask import Flask, render_template, request
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import openpyxl

nltk.download('punkt')
nltk.download('stopwords')

app = Flask(__name__)

# Load Lemmas from Excel File
def load_lemmas():
    workbook = openpyxl.load_workbook('Lemmas.xlsx', read_only=True)

    educational_lemmas = set(row[0].value for row in workbook['Educational'].iter_rows(min_col=1, max_col=1))
    social_lemmas = set(row[0].value for row in workbook['Social'].iter_rows(min_col=1, max_col=1))
    technical_lemmas = set(row[0].value for row in workbook['Technical'].iter_rows(min_col=1, max_col=1))

    return educational_lemmas, social_lemmas, technical_lemmas

educational_lemmas, social_lemmas, technical_lemmas = load_lemmas()

# NLTK resources
stop_words = set(stopwords.words('english'))
porter = PorterStemmer()

# Function to preprocess and tokenize text
def preprocess_and_tokenize(text):
    words = word_tokenize(text.lower())
    # Remove stop words and non-alphabetic words
    words = [porter.stem(word) for word in words if word.isalpha() and word not in stop_words]
    return words

def analyze_text(text):
    words = preprocess_and_tokenize(text)

    # Count occurrences of lemmas from each category
    educational_count = sum(1 for word in words if word in educational_lemmas)
    social_count = sum(1 for word in words if word in social_lemmas)
    technological_count = sum(1 for word in words if word in technical_lemmas)

    total_words = len(words)

    # Calculate scores
    educational_score = educational_count / total_words
    social_score = social_count / total_words
    technological_score = technological_count / total_words

    return educational_score, social_score, technological_score

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    text_to_analyze = request.form['text']
    
    educational_score, social_score, technological_score = analyze_text(text_to_analyze)

    return render_template('result.html', text=text_to_analyze, edu_score=educational_score,
                            social_score=social_score, tech_score=technological_score)

if __name__ == '__main__':
    app.run(debug=True)



