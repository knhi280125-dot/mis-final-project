import os
from flask import Flask, render_template, request
import firebase_admin
from firebase_admin import credentials, firestore

# Khởi tạo Flask
app = Flask(__name__)

# Đường dẫn file chứng chỉ Firebase
cred_path = os.path.join(os.path.dirname(__file__), "serviceAccountKey.json")

if not firebase_admin._apps:
    cred = credentials.Certificate(cred_path)
    firebase_admin.initialize_app(cred)

db = firestore.client()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/search', methods=['GET', 'POST'])
def search():
    teachers = []
    keyword = ""
    if request.method == 'POST':
        keyword = request.form.get('keyword')
        # Tìm kiếm trong database của Nhi
        docs = db.collection("靜宜資管").stream()
        for doc in docs:
            data = doc.to_dict()
            if keyword and keyword in data.get("name", ""):
                teachers.append(data)
    return render_template('search.html', teachers=teachers, keyword=keyword)

# Biến để Vercel chạy app
app = app
