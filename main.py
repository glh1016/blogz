from flask import Flask, request, redirect, render_template, flash, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:blogs@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'y337kGcys&zP3B'


class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(1000))
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, title, body, owner):
        self.title = title
        self.body = body
        self.owner = owner


class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))
    blogs = db.relationship('Blog', backref='owner')

    def __init__(self, username, password):
        self.username = username
        self.password = password


@app.route('/blog', methods=['POST','GET'])
def blog():
    id = request.args.get('id')
    username = request.args.get('user')

    if id:
        post = Blog.query.filter_by(id=id).first()
        return render_template('indblogview.html',post=post)
    if username:
        user = User.query.filter_by(username=username).first()
        return render_template('singleuser.html',user=user)

   
    posts = Blog.query.all()
    return render_template('mainblog.html',posts=posts)
 



@app.route('/newpost', methods=['POST', 'GET'])
def add_post():

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        owner= User.query.filter_by(username=session['username']).first()

        title_error = ''
        body_error = ''
        
        if not title:
            title_error = "Empty title field"
    

        if not body:
            body_error = "Empty body field"

        if not body or not title:
            return render_template('newpost.html', title = title, body = body, title_error = title_error, body_error = body_error)
    


        new_entry = Blog(title,body,owner)
        db.session.add(new_entry)
        db.session.commit()

    
        return redirect('/blog?id={0}'.format(new_entry.id))

    return render_template('newpost.html')


@app.before_request
def require_login():
    allowed_routes = ['login', 'signup', 'index','blog']
    if request.endpoint not in allowed_routes and 'username' not in session:
        return redirect('/login')





@app.route('/login', methods=['POST', 'GET'])
def login():

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            session['username'] = username
            flash("Logged in")
            return redirect('/newpost')
        
        if user and user.password != password:
            #TODO keep username populated
            flash('User password incorrect', 'error')

        if not user:
            flash('Username does not exist', 'error')

    return render_template('login.html')


@app.route('/logout')
def logout():
    del session['username']
    flash("Logged out")
    return redirect('/blog')


@app.route('/signup', methods=['POST', 'GET'])
def signup(): 

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        verify = request.form['verify']


        existing_user = User.query.filter_by(username=username).first()
        if not existing_user:
        
            if not username:
                flash('Username field empty', 'error')
                return render_template('signup.html')

            if not password:
                flash('Password field empty', 'error')
                return render_template('signup.html')

            if not verify:
                flash('Must verify password', 'error')
                return render_template('signup.html')

            if password != verify:
                flash('Passwords must match','error')
                return render_template('signup.html')

            if len(username) < 3 or len(password) < 3:
                flash('Username and password must each be 3 characters or more','error')
                return render_template('signup.html')

            new_user = User(username, password)
            db.session.add(new_user)
            db.session.commit()
            session['username'] = username
            return redirect('/newpost')
             
        
        else: 
            flash('Existing user', 'error')
            return redirect('/login')

    

    return render_template('signup.html')


@app.route('/', methods=['POST', 'GET'])
def index():
    users= User.query.all()
    return render_template('index.html',users=users)
    
    
    
    
    #if request.method == 'POST':
        #blog_title = request.form['title']
        #blog_body = request.form['body']
        #wner= User.query.filter_by(username=session['username']).first()
        #new_blog_entry = Blog(blog_title,blog_body,owner)
        #db.session.add(new_blog_entry)
        #db.session.commit()

    #return render_template('index.html')
    
    









if __name__ == '__main__':
    app.run()




