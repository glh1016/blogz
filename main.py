from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:blogs@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)


class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(1000))

    def __init__(self, title, body):
        self.title = title
        self.body = body



@app.route('/blog', methods=['POST','GET'])
def blog():
    id = request.args.get('id')

    if id:
        post = Blog.query.filter_by(id=id).first()
        return render_template('indblogview.html',post=post)
   
    posts = Blog.query.all()
    return render_template('mainblog.html',posts=posts)
 



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

    
        return redirect('/blog?id={0}'.format(new_entry.id))

    return render_template('newpost.html')




if __name__ == '__main__':
    app.run()