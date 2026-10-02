from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import date

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///jobs.db'

db = SQLAlchemy(app)


class Application(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company = db.Column(db.String(100), unique=False, nullable=False)
    position = db.Column(db.String(100), unique=False, nullable=False)
    status = db.Column(db.String(20), default="applied")
    date_applied = db.Column(db.Date, default=date.today)
    url = db.Column(db.String(300))
    notes = db.Column(db.Text)

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    apl = db.session.execute(db.select(Application)).scalars().all()
    return render_template("index.html", applications=apl)

@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        company = request.form["company"]
        position = request.form["position"]
        status = request.form["status"]
        url = request.form.get("url")
        notes = request.form.get("notes")

        new_application = Application(company=company, position=position, status=status, date_applied=date.today(), url=url, notes=notes)
        db.session.add(new_application)
        db.session.commit()
        return redirect("/")
    return render_template("add.html")

if __name__ == '__main__':
   app.run()