from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:blog@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)




class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    body = db.Column(db.String(1000))

    def __init__(self, title, body):
        self.title = title
        self.body = body


@app.route('/', methods=['POST', 'GET'])
def index()

    return render_template('mainblog.html')



@app.route('/newpost', methods=['POST', 'GET'])
def add_post():
     
      if request.method == 'POST':
        blog_title = request.form['title']
        new_title = Task(blog_title)
        blog_body = request.form['body']
        new_body = Task(blog_body)
        db.session.add(new_title)
        db.session.add(new_body)
        db.session.commit()
     
     
     return render_template('newpost.html', title = "Add a Blog", )






if __name__ == '__main__':
app.run()