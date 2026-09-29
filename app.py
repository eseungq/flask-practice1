from flask import Flask, url_for
app = Flask(__name__)

@app.route('/')
def index():
    return f"<a href='{url_for('about')}'>소개로</a>"

@app.route('/about')
def about():
    return '소개 페이지'

@app.route('/user/<username>')
def profile(username):
    return f'{username} 님의 프로필'

@app.route('/post/<int:pid>')
def post(pid):
    return f'{pid}번 글 (자료형: {type(pid).__name__})'