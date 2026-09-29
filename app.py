from flask import Flask, url_for
app = Flask(__name__)

@app.route('/')
def index():
    return f"<a href='/about'>소개로</a>"

@app.route('/info')
def about_page():
    return '소개 페이지'

@app.route('/user/<username>')
def profile(username):
    return f'{username} 님의 프로필'

@app.route('/post/<int:pid>')
def post(pid):
    return f'{pid}번 글 (자료형: {type(pid).__name__})'

@app.route('/notes/')           # 끝에 슬래시
def notes():
    return '메모 목록'

@app.route('/hello')            # 주소 둘을
@app.route('/hello/<name>')     # 한 함수에
def hello(name=None):           # 기본값이 있어야 합니다
    if name:
        return f'안녕하세요, {name} 님'
    return '안녕하세요'