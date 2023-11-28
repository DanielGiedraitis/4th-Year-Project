from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import openpyxl

nltk.download('punkt')
nltk.download('stopwords')

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Gied@localhost/DiversityDB'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_secret_key'  # Change to different secret key

db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


# Load Lemmas from Excel File
def load_lemmas():
    workbook = openpyxl.load_workbook('Lemmas.xlsx', read_only=True)

    educational_lemmas = set(row[0].value.lower() for row in workbook['Educational'].iter_rows(min_row=2, max_col=1))
    social_lemmas = set(row[0].value.lower() for row in workbook['Social'].iter_rows(min_row=2, max_col=1))
    technical_lemmas = set(row[0].value.lower() for row in workbook['Technical'].iter_rows(min_row=2, max_col=1))

    return educational_lemmas, social_lemmas, technical_lemmas

educational_lemmas, social_lemmas, technical_lemmas = load_lemmas()

stop_words = set(stopwords.words('english'))
porter = PorterStemmer()


def preprocess_and_tokenize(text):
    words = word_tokenize(text.lower())
    words = [porter.stem(word) for word in words if word.isalpha() and word not in stop_words]
    return words


def analyze_text(text):
    words = preprocess_and_tokenize(text)

    educational_lemmas_lower = {lemma.lower() for lemma in educational_lemmas}
    social_lemmas_lower = {lemma.lower() for lemma in social_lemmas}
    technical_lemmas_lower = {lemma.lower() for lemma in technical_lemmas}

    educational_count = sum(1 for word in words if word.lower() in educational_lemmas_lower)
    social_count = sum(1 for word in words if word.lower() in social_lemmas_lower)
    technological_count = sum(1 for word in words if word.lower() in technical_lemmas_lower)

    total_words = len(words)

    educational_score = educational_count / total_words
    social_score = social_count / total_words
    technological_score = technological_count / total_words

    modified_text = f"Original Text:\n{text}\n\nRecommendations:\nPrint Recommendations."

    return educational_score, social_score, technological_score, modified_text


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        print(f"Received username: {username}, password: {password}")

        user = User.query.filter_by(username=username).first()

        if user:
            print(f"Retrieved user: {user.username}, {user.password_hash}")

            # Verify the password using check_password_hash
            if check_password_hash(user.password_hash, password):
                session['user_id'] = user.id
                return redirect(url_for('index'))
        
        print("Invalid username or password.")
        error = 'Invalid username or password.'
        return render_template('login.html', error=error)

    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        new_user = User(username=username, email=email, password_hash=hashed_password)

        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('login'))

    return render_template('register.html')


@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('login'))


@app.route('/')
def index():
    if 'user_id' in session:
        return render_template('index.html')
    else:
        return redirect(url_for('login'))


@app.route('/analyze', methods=['POST'])
def analyze():
    text_to_analyze = request.form['text']

    educational_score, social_score, technological_score, modified_text = analyze_text(text_to_analyze)

    return render_template('result.html', text=text_to_analyze, edu_score=educational_score,
                           social_score=social_score, tech_score=technological_score,
                           modified_text=modified_text)


if __name__ == '__main__':
    db.create_all()
    app.run(debug=True, use_reloader=True)











