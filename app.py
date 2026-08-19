from flask import (
    Flask,
    render_template,
    request,
    jsonify,
    redirect,
    url_for,
    flash,
)

from flask_login import (
    LoginManager,
    login_user,
    logout_user,
    login_required,
    current_user,
)

from analyzer.seo_analyzer import analyze_website, SEOAnalyzerError
from config import Config
from database import db
from models import User, SEOAnalysis, ContactMessage


app = Flask(__name__)

app.config.from_object(Config)

db.init_app(app)


# =========================================================
# FLASK-LOGIN SETUP
# =========================================================

login_manager = LoginManager()
login_manager.init_app(app)

login_manager.login_view = "login"
login_manager.login_message = "Please log in to access this page."
login_manager.login_message_category = "error"


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))


# =========================================================
# PUBLIC PAGE ROUTES
# =========================================================

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


# =========================================================
# AUTHENTICATION — REGISTER
# =========================================================

@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("home"))

    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        confirm_password = request.form.get("confirm_password", "")

        if not name or not email or not password or not confirm_password:
            flash(
                "Please fill in all required fields.",
                "error",
            )
            return redirect(url_for("register"))

        if password != confirm_password:
            flash(
                "Passwords do not match.",
                "error",
            )
            return redirect(url_for("register"))

        if len(password) < 8:
            flash(
                "Password must be at least 8 characters long.",
                "error",
            )
            return redirect(url_for("register"))

        existing_user = User.query.filter_by(
            email=email
        ).first()

        if existing_user:
            flash(
                "An account with this email already exists.",
                "error",
            )
            return redirect(url_for("register"))

        try:
            user = User(
                name=name,
                email=email,
            )

            user.set_password(password)

            db.session.add(user)
            db.session.commit()

            login_user(user)

            flash(
                "Your ZOVO SEARCH account has been created successfully.",
                "success",
            )

            return redirect(url_for("home"))

        except Exception as error:
            db.session.rollback()

            print("Register error:", error)

            flash(
                "Unable to create your account right now.",
                "error",
            )

            return redirect(url_for("register"))

    return render_template("pages/register.html")


# =========================================================
# AUTHENTICATION — LOGIN
# =========================================================

@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("home"))

    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        if not email or not password:
            flash(
                "Please enter your email and password.",
                "error",
            )
            return redirect(url_for("login"))

        user = User.query.filter_by(email=email).first()

        if not user or not user.check_password(password):
            flash(
                "Invalid email or password.",
                "error",
            )
            return redirect(url_for("login"))

        login_user(user)

        flash(
            f"Welcome back, {user.name}!",
            "success",
        )

        return redirect(url_for("home"))

    return render_template("pages/login.html")


# =========================================================
# AUTHENTICATION — LOGOUT
# =========================================================

@app.route("/logout")
@login_required
def logout():
    logout_user()

    flash(
        "You have been logged out successfully.",
        "success",
    )

    return redirect(url_for("home"))


# =========================================================
# CONTACT
# =========================================================

@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        try:
            name = request.form.get("name", "").strip()
            email = request.form.get("email", "").strip()
            website = request.form.get("website", "").strip()
            service = request.form.get("service", "").strip()
            message = request.form.get("message", "").strip()

            if not name or not email or not service or not message:
                return jsonify({
                    "success": False,
                    "error": "Please fill in all required fields."
                }), 400

            contact_message = ContactMessage(
                name=name,
                email=email,
                website=website or None,
                service=service,
                message=message
            )

            db.session.add(contact_message)
            db.session.commit()

            return jsonify({
                "success": True,
                "message": "Your enquiry has been sent successfully."
            }), 201

        except Exception as error:
            db.session.rollback()

            print("Contact form error:", error)

            return jsonify({
                "success": False,
                "error": "Unable to send your enquiry right now."
            }), 500

    return render_template("pages/contact.html")


# =========================================================
# SEO ANALYZER
# =========================================================

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


# =========================================================
# DATABASE INITIALIZATION
# =========================================================

with app.app_context():
    db.create_all()


# =========================================================
# RUN APPLICATION
# =========================================================

if __name__ == "__main__":
    app.run(debug=True)