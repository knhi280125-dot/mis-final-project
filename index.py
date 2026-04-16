import os
from flask import Flask, render_template, request, jsonify
import firebase_admin
from firebase_admin import credentials, firestore

app = Flask(__name__)

# Cấu hình lỗi để dễ bắt bệnh nếu có sự cố
app.config['PROPAGATE_EXCEPTIONS'] = True

# Kết nối Firebase (Đảm bảo tên file JSON đúng 100% với file trên GitHub)
cred_path = os.path.join(os.path.dirname(__file__), "serviceAccountKey.json")
if not firebase_admin._apps:
    cred = credentials.Certificate(cred_path)
    firebase_admin.initialize_app(cred)

db = firestore.client()

@app.route('/')
def home():
    # File này phải nằm trong thư mục templates
    return render_template('index.html')

@app.route('/search', methods=['GET', 'POST'])
def search():
    results = []
    if request.method == 'POST':
        teacher_name = request.form.get('teacher_name')
        if teacher_name:
            # Tìm kiếm trong collection 'teachers' trên Firebase
            docs = db.collection('teachers').where('name', '==', teacher_name).stream()
            for doc in docs:
                results.append(doc.to_dict())
    return render_template('search.html', results=results)

# Biến quan trọng để Vercel nhận diện
app = app
