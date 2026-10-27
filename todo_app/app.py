from flask import Flask, Blueprint, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_restx import Api, Resource, fields

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://flask_user:password@localhost/flask_todo_db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
# 404 에 "did you mean ...?" 라는 긴 안내가 따라붙는 것을 끕니다.
app.config["ERROR_404_HELP"] = False
# 한글을 \uc6b0\uc720 처럼 바꾸지 않고 그대로 내보냅니다.
app.config["RESTX_JSON"] = {"ensure_ascii": False}
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(100), nullable=False)
    done = db.Column(db.Boolean, default=False)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # session은 아직 저장되지 않은 변경을 모아두는 곳
        # add는 새 줄을 그 곳에 담음. 이때는 아직 파일에 안 써짐
        # commit은 한꺼번에 파일에 씀.
        db.session.add(Todo(text=request.form['todo']))
        db.session.commit()
        return redirect(url_for('index'))
    todos = Todo.query.all()
    return render_template('index.html', todos=todos)

@app.route('/toggle/<int:id>')
def toggle(id):
    todo = db.get_or_404(Todo, id)
    todo.done = not todo.done
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/delete/<int:id>')
def delete(id):
    todo = db.get_or_404(Todo, id)
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)


with app.app_context():
    db.create_all()