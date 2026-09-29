from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return 'Index Page'

@app.route('/hello')
def hello():
    return 'Hello, World'

@app.route("/about")
def about():
    return "About us"

@app.route("/test/<text>")
def route_sample(text):
    return f"<h1>{text}</h1>"

@app.route("/hi/<name>")
def h1_template_render(name):
    return render_template("hi.html", name=name)

@app.route('/user/<username>')
def show_user_profile(username):
    return f"User: {username}"

@app.route('/blog/<int:year>/<int:month>/<int:day>')
def show_blog_post(year, month, day):
    # 월, 일은 2자리로 맞추기 위해 :02d 포맷을 사용합니다.
    return f"Blog Post from: {year}-{month:02d}-{day:02d}"