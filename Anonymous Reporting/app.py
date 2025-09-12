from flask import Flask, render_template, request, redirect, url_for
from models import db, Report
from datetime import datetime

app = Flask(__name__)
app.config["SECRET_KEY"] = "your_secret_key"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///corruption.db"
db.init_app(app)

with app.app_context():
    db.create_all()

@app.route("/")
def home():
    reports = Report.query.order_by(Report.date.desc()).all()
    return render_template("home.html", reports=reports)

@app.route("/report", methods=["GET", "POST"])
def report():
    if request.method == "POST":
        title = request.form["title"]
        description = request.form["description"]
        category = request.form["category"]

        new_report = Report(
            title=title,
            description=description,
            category=category,
            date=datetime.now()
        )
        db.session.add(new_report)
        db.session.commit()
        return redirect(url_for("home"))
    
    return render_template("report.html")

if __name__ == "__main__":
    app.run(debug=True)
