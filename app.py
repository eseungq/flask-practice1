from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def hello_world():
    return "<h1>메인 페이지</h1>"

@app.route("/about")
def about():
    return "<h1>소개 페이지</h1>"

@app.route("/test/<text>")
def route_sample(text):
    return f"<h1>{text}</h1>"

@app.route("/hi/<name>")
def h1_template_render(name):
    return render_template("hi.html", name=name)
