from flask import render_template, Blueprint, redirect, url_for, request
from src.service.logic.user_logic import user_details
from src.service.logic.dictionary_logic import DictionaryLogic, WordListFilter
import re
from flask_login import login_required
from src.service.util.logger import *
import jinja2

home_blueprint = Blueprint('home', __name__)
content_blueprint = Blueprint('content', __name__)
"""
admin_blueprint = Blueprint(
    'admin',
    __name__,
    template_folder='templates/admin',
    url_prefix=""
)
"""


@home_blueprint.route('/home')
def home(page=1):
    return render_template('content/base.html')


@home_blueprint.route('/user/<string:post_id>')
def user(post_id):
    print('user1')
    user_detail, post = user_details(post_id)
    if not user_detail:
        print(user_detail.username)

    return render_template(
        'content/user.html',
        user=user_detail,
        posts=post,
        recent={},
        top_tags={}
    )


@home_blueprint.route('/admin')
@login_required
def admin(page=1):
    return redirect('http://127.0.0.1:1058/admin/')


# Content Blue Print
@content_blueprint.route('/')
def home(page=1):
    user_detail, post = user_details(page)
    print(user_details)
    return render_template(
        'content/home.html',
        posts={},
        recent={},
        top_tags={}
    )


@content_blueprint.route('/<int:page>')
def article(page=1):
    return render_template('content/base.html')


# /content/deutsch/list?srch=b
@content_blueprint.route('/deutsch/list')
@content_blueprint.route('/deutsch/list&channel=<channel>')
def deutsch(channel=None):
    _word_filter = None

    rule = re.split('\?srch=', request.full_path, 1)
    if len(rule) > 1:
        channel = rule[1]
        print(channel)

    if channel is not None:
        _filters = {'letter': channel, 'sape': 4139, 'page_size': 100}
        _word_filter = WordListFilter()
        _word_filter.parse(_filters)

    _logic = DictionaryLogic()
    try:
        _word_list, _page = _logic.get_list(_word_filter)
    except Exception as ex:
        log_traceback(ex)

    return render_template(
        'content/deutsch.html',
        words=_word_list,
        recent={},
        top_tags={}
    )


"""
# Admin Blue Print
@admin_blueprint.route('/')
def home(page=1):
    return "Hello Joe"


@admin_blueprint.route('/<int:page>')
def admin(page=1):
    return render_template('content/base.html')
"""


# Public Register def
def register_blueprint(app):
    @app.route('/react')
    def test():
        return render_template('react/index.html')

    @app.route('/')
    def index():
        url = url_for('content.deutsch')  # content_blueprint - home(def)
        print(url)
        return redirect(url)

    app.register_blueprint(home_blueprint, url_prefix='')
    app.register_blueprint(content_blueprint, url_prefix='/content')
    # app.register_blueprint(admin_blueprint, url_prefix='/admin')

    register_add_url_rule(app)
    register_error_handlers(app)
    register_templates_and_static(app)


def register_error_handlers(app):
    def render_error(error):
        error_code = getattr(error, 'code', 500)
        return render_template("{0}.html".format(error_code)), error_code

    for errcode in [500]:
        app.errorhandler(errcode)(render_error)
    return None


def register_add_url_rule(app):
    @app.route("/hello/<username>")
    def hello_user(username):
        return 'Hello: %s' % username

    @app.route('/post/<int:post_id>', methods=('GET', 'POST'))
    def post(post_id):
        return {"": "gfdgdfg"}


def register_templates_and_static(app):
    _template_path = jinja2.ChoiceLoader([
        app.jinja_loader,
        jinja2.FileSystemLoader('www/templates'),
    ])
    app.jinja_loader = _template_path
