from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("pages/index.html")

@app.route("/about")
def about():
    return render_template("pages/about.html")

@app.route("/services")
def services():
    return render_template("pages/services.html")

@app.route("/portfolio")
def portfolio():
    return render_template("pages/portfolio.html")

@app.route("/contact")
def contact():
    return render_template("pages/contact.html")

@app.route("/analyzer")
def analyzer():
    return render_template("pages/analyzer.html")

if __name__ == "__main__":
    app.run(debug=True)



    


