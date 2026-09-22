from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template("home.html")

@app.route("/profile")
def profile():
    hobbies = ["음악 감상", "사진 촬영", "여행"]
    return render_template("profile.html", hobbies=hobbies)