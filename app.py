from flask import Flask, render_template, request, jsonify

from analyzer.seo_analyzer import analyze_website, SEOAnalyzerError
from config import Config
from database import db
from models import User, SEOAnalysis, ContactMessage


app = Flask(__name__)

app.config.from_object(Config)
db.init_app(app)


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


@app.route("/api/analyze", methods=["POST"])
def analyze():
    try:
        data = request.get_json(silent=True)

        if not data:
            return jsonify({
                "success": False,
                "error": "Invalid request."
            }), 400

        url = data.get("url", "").strip()

        if not url:
            return jsonify({
                "success": False,
                "error": "Please enter a website URL."
            }), 400

        result = analyze_website(url)

        return jsonify({
            "success": True,
            "data": result
        }), 200

    except SEOAnalyzerError as error:
        return jsonify({
            "success": False,
            "error": str(error)
        }), 400

    except Exception as error:
        print("Analyzer error:", error)

        return jsonify({
            "success": False,
            "error": "Something went wrong while analyzing the website."
        }), 500


with app.app_context():
    db.create_all()


if __name__ == "__main__":
    app.run(debug=True)
    