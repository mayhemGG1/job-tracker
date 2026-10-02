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
def hello_world():
    return "Hello World"

if __name__ == '__main__':
    app.run()