from flask import Flask, redirect, render_template, request, url_for
app = Flask(__name__)
import os
from flask_sqlalchemy import SQLAlchemy

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] =\
        'sqlite:///' + os.path.join(basedir, 'database.db')

db = SQLAlchemy(app)

class Letter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    to = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(100), nullable=False)
    text = db.Column(db.String(100), nullable=False)
    image_url = db.Column(db.String(10000), nullable=False)

    def __repr__(self):
        return f'{self.to} {self.text} {self.username}'
with app.app_context():
    db.create_all()
    
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/post')
def post():
    return render_template('post.html')

@app.route('/letter')
def letter():    
    letter_list = Letter.query.all()
    
    return render_template('letter.html', data=letter_list)
    
@app.route("/letter/create/")
def letter_create():
    #form에서 데이터 받아오기
    to_receive = request.args.get("to")
    text_receive = request.args.get("text")
    username_receive = request.args.get("username")
    image_receive = request.args.get("image_url")
    
    #데이터를 DB에 저장하기
    song = Letter(to=to_receive, text=text_receive, username=username_receive, image_url=image_receive)
    db.session.add(song)
    db.session.commit()
    
    return redirect(url_for('letter'))

if __name__ == '__main__':  
    app.run(debug=True)