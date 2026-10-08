from flask import Flask, render_template, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import date
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL" , "sqlite:///jobs.db")
app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY", "dev-only-change-me")

db = SQLAlchemy(app)


class Application(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company = db.Column(db.String(100), unique=False, nullable=False)
    position = db.Column(db.String(100), unique=False, nullable=False)
    status = db.Column(db.String(20), default="applied")
    date_applied = db.Column(db.Date, default=date.today)
    url = db.Column(db.String(300))
    notes = db.Column(db.Text)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    status = request.args.get("status")
    query = db.select(Application)
    if status:
        query = query.where(Application.status == status)
    
    applications = db.session.execute(query).scalars().all()
    return render_template("index.html", applications=applications, current_status=status)

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

@app.route("/delete/<int:id>", methods=["POST"])
def delete(id):
    application = db.get_or_404(Application, id)
    db.session.delete(application)
    db.session.commit()
    return redirect("/")

@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit(id):
    application = db.get_or_404(Application, id)
    if request.method == "POST":
        application.company = request.form["company"]
        application.position = request.form["position"]
        application.status = request.form["status"]
        application.url = request.form["url"]
        application.notes = request.form["notes"]
        db.session.commit()
        return redirect("/")
    return render_template("edit.html", application=application)

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        email = request.form["email"].strip().lower()
        password = request.form["password"]

        if len(password) < 8:
            flash("Пароль має містити щонайменше 8 символів")
            return redirect("/register")
        
        if db.session.execute(db.select(User).where(User.email == email)).scalar_one_or_none() is not None:
            flash("Користувач з таким email уже є")
            return redirect("/register")

        u = User(email=email)
        u.set_password(password)
        db.session.add(u)
        db.session.commit()
        return redirect("/")
    return render_template("register.html")

if __name__ == '__main__':
   app.run()