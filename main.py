from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:blog@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)


class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(1000))

    def __init__(self, title, body):
        self.title = title
        self.body = body



@app.route('/blog', methods=['POST', 'GET'])
def index():

    posts = Blog.query.all()
    return render_template('mainblog.html',posts=posts)


@app.route('/', methods=['POST','GET'])
def single_blog():
    id = request.args.get('id')
    post = Blog.query.filter_by(id=id).first()
    return render_template('indblogview.html',post=post)



@app.route('/newpost', methods=['POST', 'GET'])
def add_post():

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']

        title_error = ''
        body_error = ''
        
        if not title:
            title_error = "Empty title field"
    

        if not body:
            body_error = "Empty body field"

        if not body or not title:
            return render_template('newpost.html', title = title, body = body, title_error = title_error, body_error = body_error)
    


        new_entry = Blog(title,body)
        db.session.add(new_entry)
        db.session.commit()

    
        return redirect('/blog')

    return render_template('newpost.html')




if __name__ == '__main__':
    app.run()