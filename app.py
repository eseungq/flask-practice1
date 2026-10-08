from flask import Flask, url_for, request, render_template, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(100), nullable=False)
    done = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f'<Todo {self.id} {self.text}>'

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        new_todo = Todo(text=request.form['text'])
        db.session.add(new_todo)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('index.html', todos=Todo.query.all())

@app.route('/about')
def about():
    return '소개 페이지'

@app.route('/user/<username>')
def profile(username):
    return render_template('profile.html', 
                           username=username,
                           post=['첫 글', '두 번째 글'])

@app.route('/post/<int:pid>')
def post(pid):
    return f'{pid}번 글 (자료형: {type(pid).__name__})'

@app.route('/notes/')           # 끝에 슬래시
def notes():
    return '메모 목록'

@app.route('/search')
def search():
    query = request.args.get('q', '')  # 쿼리 문자열을 가져옵니다
    page = request.args.get('page', 1)
    if not query:
        return '검색어를 입력하세요'
    return f'"{query}" 검색 결과 ({page} 페이지)'

@app.route('/write', methods=['GET', 'POST'])
def write():
    if request.method == 'POST':
        banana = request.form['banana']
        melon = request.form['melon']
        return (f'banana = {banana} ({type(banana).__name__}) / '
                f'melon = {melon} ({type(melon).__name__})')
    return '''
    <form method="post">
      <input type="text" name="banana">
      <input type="number" name="melon">
      <button type="submit">보내기</button>
    </form>'''


@app.route('/attach', methods=['GET', 'POST'])
def attach():
    if request.method == 'POST':
        f = request.files.get('cherry')
        if f is None:
            return 'cherry 가 files 에 없습니다'
        return f'{f.filename} / {len(f.read())} 바이트'
    return '''
    <form method="post">
      <input type="text" name="banana">
      <input type="file" name="cherry">
      <button type="submit">보내기</button>
    </form>'''

@app.route('/hello/<name>')
def hello(name=None):
    return render_template('hello.html', name=name)

@app.route('/newuser/<username>')
def new_user(username):
    return render_template('profile.html',
                           username=username,
                           post=[])

with app.app_context():
    db.create_all()