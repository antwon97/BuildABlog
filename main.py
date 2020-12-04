from flask import Flask, request, redirect, render_template, url_for
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)

#user:password@server:portNumber/databaseName
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://buildblog:buildblog@localhost:3306/buildblog'

#Not for deployment
app.config['SQLALCHEMY_ECHO'] = True
app.config['DEBUG'] = True

db = SQLAlchemy(app)

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    content = db.Column(db.String(120))

    def __init__(self, name, content):
        self.name = name
        self.content = content

def get_blog_ids():
    ids = db.session.query(Blog.id).all()
    ids=[i[0] for i in ids]

    return ids

def get_blog_names():
    names = db.session.query(Blog.name).all()
    names=[i[0] for i in names]

    return names

def get_blog_contents():
    contents = db.session.query(Blog.content).all()
    contents=[i[0] for i in contents]

    return contents

@app.route('/blog')
def blog():

    id = request.args.get('id')

    currBlog = db.session.query(Blog).get(id)

    return render_template('blog.html', name=currBlog.name, content=currBlog.content)


@app.route('/newpost', methods=['POST', 'GET'])
def newpost():
    
    if request.method == 'POST':
        title = request.form['blogTitle']

        content = request.form['blogContent']

        new_blog = Blog(title, content)
        db.session.add(new_blog)
        db.session.commit()

        redir_url = "/blog?id=" + str(new_blog.id)

        return redirect(redir_url)

    return render_template('newpost.html')


@app.route("/")
def index():

    return render_template('index.html', ids=get_blog_ids(), names=get_blog_names(), contents=get_blog_contents())


if __name__ == '__main__':
    app.run()