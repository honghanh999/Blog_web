from flask import Flask, redirect, render_template, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Setting up a database: download it, create a model

app = Flask(__name__)
# just a path that database is stored
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
# There have a database and Sqlacademy tool our flask app, and now linked them together
db = SQLAlchemy(app)

# Model is just a way to structure the data in your database
# Create some models
class BlogPost(db.Model):
    # data type, primary_key: the ID is going to be the main distinguisher between the BlogPost
    id = db.Column(db.Integer, primary_key= True)
    # this filed cannot be null, can not be nothing
    title = db.Column(db.String(100), nullable= False)
    content = db.Column(db.Text, nullable= False)
    author = db.Column(db.String(20), nullable= False, default= 'N/A')
    # utc = time zone
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    # This function is going to print out whenever we create a new blog post (reprint)
    # def __repr__(self):
    #     return 'Blog post'+ str(self.id)


# dummy data here
all_posts = [
    {
        'title': 'Post 1',
        'content': 'This is the content of post 1',
        'author': 'Hanh'
    },
    {
        'title':'Post 2',
        'content': 'This is the content of post 2'
    }
]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/posts', methods=['GET', 'POST'])
def posts():
    # check
    # request.form: wanting to retrieve the values for the form that was posted.
    if request.method == 'POST':
        post_title = request.form['title']
        post_content = request.form['content']
        post_author= request.form['author']
        new_post = BlogPost(title=post_title, content=post_content, author=post_author)
        db.session.add(new_post)
        # commit: saved here permanently, move to other computer or restart or bla bla, then it'll still be there
        db.session.commit()
        # redirect back to the same page
        return redirect('/posts')
    else:
        all_posts = BlogPost.query.all()
        return render_template('posts.html', posts = all_posts)

@app.route('/posts/new', methods=['GET', 'POST'])
def new_post():
    if request.method == 'POST': 
        post_title = request.form['title']
        post_content = request.form['content']
        post_author= request.form['author']
        new_post = BlogPost(title=post_title, content=post_content, author=post_author)
        db.session.add(new_post)
        db.session.commit()
        return redirect('/posts')
    else:
        return render_template('new_post.html')

@app.route('/posts/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    # we can call it to any class object and return the object or raise a 404 error if the object is not found.
    post = BlogPost.query.get_or_404(id)
    if request.method == 'POST':
        post.title = request.form['title']
        post.content = request.form['content']
        post.author = request.form['author']
        db.session.commit()
        return redirect('/posts')
    else:
        return render_template('edit.html', post=post)

@app.route('/posts/delete/<int:id>')
def delete(id):
    post = BlogPost.query.get_or_404(id)
    db.session.delete(post)
    db.session.commit()
    return redirect('/posts')

@app.route('/home/<string:name>')
def hello(name):
    return "Hello, " + name

@app.route('/onlyget', methods=['POST'])
def get_req():
    return 'You can only get this webpage  3'


if __name__ == "__main__":
    app.run(debug=True)