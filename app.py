from flask import Flask, flash, redirect, render_template, request, session
from flask.templating import render_template
app = Flask(__name__)

@app.route("/")
def home():
    return render_template("mainpage.html")

@app.route("/cafeattribute")
def cafeattribute():
    return render_template("cafeattribute.html")

# admin paneli
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        if not request.form.get("username"):
            # flash("Kullanıcı Adı Giriniz!")
            return render_template("/login.html") 

        elif not request.form.get("password"):
            # flash("Şifrenizi Giriniz!")
            return render_template("/login.html")
        
        return render_template("/index.html")
    return render_template("/login.html")




if __name__ == '__main__':
    app.run(debug=True)
