import sys, os
from flask import Flask, render_template, Markup, url_for
from flask_flatpages import FlatPages, pygments_style_defs
from flask_frozen import Freezer
from flask.ext.misaka import Misaka
import markdown

DEBUG = True
FLATPAGES_AUTO_RELOAD = DEBUG
FLATPAGES_EXTENSION = '.md'
FLATPAGES_ROOT = 'content'
POST_DIR = 'posts'

app = Flask(__name__)
md = Misaka(math=True, math_explicit=True)
md.init_app(app)
app.static_folder = 'static'
flatpages = FlatPages(app)
freezer = Freezer(app)
app.config.from_object(__name__)

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
    return render_template('posts.html', posts=posts)

@app.route("/about/")
def about():
    return render_template('about.html')

@app.route("/one-word-story/")
def ows_game():
    return render_template('one-word-story.html')

@app.route('/<name>/')
def post(name):
    path = '{}/{}'.format(POST_DIR, name)
    post = flatpages.get_or_404(path)
    #post = Markup(markdown.markdown(post)) # Passing HTML is destroying the latex math
    return render_template('post.html', post=post)


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "build":
        freezer.freeze()
    else:
        app.run(host='0.0.0.0', debug=True)
