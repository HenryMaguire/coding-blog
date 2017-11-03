import sys, os
from flask import Flask, render_template, Markup, url_for, request
from flask_flatpages import FlatPages, pygments_style_defs
from flask_frozen import Freezer
from flask.ext.misaka import Misaka, markdown
#import markdown

app = Flask(__name__)
Misaka(app)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from init_database import Story, Base
DEBUG = True
FLATPAGES_AUTO_RELOAD = DEBUG
FLATPAGES_EXTENSION = '.md'
FLATPAGES_ROOT = 'content'
POST_DIR = 'posts'
#FLATPAGES_MARKDOWN_EXTENSIONS = ['codehilite', 'toc']


#md = Misaka(math=True, math_explicit=True)
#md.init_app(app)
app.static_folder = 'static'
flatpages = FlatPages(app)
freezer = Freezer(app)
app.config.from_object(__name__)

engine = create_engine('sqlite:///stories.db')
Base.metadata.bind=engine
DBSession = sessionmaker(bind = engine)
session = DBSession()

try:
    session.rollback()
    testStory = Story(id = 6, story_text='Hello world')
    session.add(testStory)
    session.commit()
except:
    print "already in database"

@app.context_processor
def override_url_for():
    # any time you use url_for in your templates to render a static resource
    #it will use dated_url_for instead
    return dict(url_for=dated_url_for)

def dated_url_for(endpoint, **values):
    # resource name appended with a last modified time stamp parameter
    if endpoint == 'static':
        filename = values.get('filename', None)
        if filename:
            file_path = os.path.join(app.root_path,
                                     endpoint, filename)
            values['q'] = int(os.stat(file_path).st_mtime)
    return url_for(endpoint, **values)



@app.route("/")
@app.route("/home/")
def index():
    return render_template('index.html')

@app.route("/blog/")
def posts():
    posts = [p for p in flatpages if p.path.startswith(POST_DIR)]
    posts.sort(key=lambda item:item['date'], reverse=False)
    return render_template('blog.html', posts=posts)

@app.route("/about/")
def about():
    return render_template('about.html')


s = ''
@app.route("/one-word-story/", methods=['GET', 'POST'])
def ows_game():
    global s
    if request.method == 'POST':
        # If POST, take new word and add it to the database
        # Eventually, the bot will also make a word
        new_word = request.form['new_word']
        s+= new_word+' '
        # Pass the text to the AI which generates two words - if the 2nd is punctuation pass both to HTML.
        return render_template('one-word-story.html', generated_story=s)
    else:
        # If GET, create new database with something like a session_ID and then the story
        # Query the stories database to find all story IDs then make a new one
        s = ''
        return render_template('one-word-story.html')

@app.route('/<name>/')
def post(name):
    path = '{}/{}'.format(POST_DIR, name)
    post = flatpages.get_or_404(path)
    text = post.html # Passing HTML is destroying the latex math
    text=markdown(text, math=True)
    print text
    return render_template('post.html', post=post, text=text)


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "build":
        freezer.freeze()
    else:
        app.run(host='0.0.0.0', debug=True)
