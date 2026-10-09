from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
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