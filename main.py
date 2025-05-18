from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os
import webbrowser
import threading

app = Flask(__name__)

# Ensure instance folder exists
if not os.path.exists(app.instance_path):
    os.makedirs(app.instance_path)

db_path = os.path.join(app.instance_path, 'reviews.db')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_path
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(300), nullable=False)
    rate = db.Column(db.Integer, nullable=False)

with app.app_context():
    db.create_all()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        text = request.form.get('text', '').strip()
        rate = request.form.get('rate', type=int)
        if text and 1 <= rate <= 5:
            db.session.add(Review(text=text, rate=rate))
            db.session.commit()
        return redirect(url_for('index'))

    reviews = Review.query.all()
    return render_template('index.html', reviews=reviews)

@app.route('/clear', methods=['POST'])
def clear():
    db.session.query(Review).delete()
    db.session.commit()
    return redirect(url_for('index'))

# Автоматическое открытие браузера
def open_browser():
    webbrowser.open_new('http://127.0.0.1:5000')

if __name__ == '__main__':
    threading.Timer(1.0, open_browser).start()
    app.run(debug=True)
