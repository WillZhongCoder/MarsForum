from flask import *
from flask_login import login_required
from pygments import highlight
from pygments.formatters import HtmlFormatter

from admininstration import _admin, _delete_user, _make_admin, _remove_admin
from ai import _gpt_api
from auth import _register, _login, _logout
from comment import _comment, _delete_comment
from extensions import db, bcrypt, login_manager
from file import _upload_file, _delete_file, _download_file, _files
from index import _search, _home
from models import User, File
from post import _new_post, _view_post, _delete_post, _edit_post
from forumProfile import _change_profile, _profile_show


def code_block(lexer, text, lang):
    return highlight(text, lexer, HtmlFormatter())


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your_secret_key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    @app.route("/")
    @app.route("/home")
    def home():
        return _home()

    @app.route("/register", methods=['GET', 'POST'])
    def register():
        return _register()

    @app.route("/login", methods=['GET', 'POST'])
    def login():
        return _login()

    @app.route("/logout")
    def logout():
        return _logout()

    @app.route("/post/new", methods=['GET', 'POST'])
    @login_required
    def new_post():
        return _new_post()

    @app.route("/view/<int:post_id>", methods=['GET', 'POST'])
    def view_post(post_id):
        return _view_post(post_id)

    @app.route("/search")
    def search():
        return _search()

    @app.route("/profile")
    def profile_show():
        return _profile_show()
    @app.route("/admin")
    @login_required
    def admin():
        return _admin()

    @app.route("/delete_user/<int:user_id>")
    @login_required
    def delete_user(user_id):
        return _delete_user(user_id)

    @app.route("/delete_post/<int:post_id>")
    @login_required
    def delete_post(post_id):
        return _delete_post(post_id)

    @app.route("/admin/make_admin/<int:user_id>")
    @login_required
    def make_admin(user_id):
        return _make_admin(user_id)

    @app.route("/admin/remove_admin/<int:user_id>")
    @login_required
    def remove_admin(user_id):
        return _remove_admin(user_id)

    @app.route("/comment/<int:post_id>", methods=['POST'])
    @login_required
    def comment(post_id):
        return _comment(post_id)

    @app.route("/delete_comment/<int:comment_id>")
    @login_required
    def delete_comment(comment_id):
        return _delete_comment(comment_id)

    @app.route("/post/edit/<int:post_id>", methods=['GET', 'POST'])
    @login_required
    def edit_post(post_id):
        return _edit_post(post_id)

    @app.route("/upload", methods=['GET', 'POST'])
    @login_required
    def upload_file():
        return _upload_file()

    @app.route("/delete_file/<file_id>")
    @login_required
    def delete_file(file_id):
        return _delete_file(file_id=file_id)

    @app.route("/dl/<filename>")
    def download_file(filename):
        return _download_file(filename)

    @app.route("/change_profile/<int:user_id>/<string:type>", methods=['GET', 'POST'])
    @login_required
    def change_profile(user_id, type):
        return _change_profile(user_id, type)

    @app.route("/aichat")
    def aichat():
        return render_template("aichat.html")

    @app.route("/api/gpt", methods=["POST"])
    def gpt_api():
        return _gpt_api()

    @app.route("/files", methods=["GET", "POST"])
    def files():
        return _files()

    @app.route("/no_permission")
    def no_permission():
        return render_template("no_permission.html")

    return app

app = create_app()

if __name__ == '__main__':
    app.run(host="127.0.0.1", port=8080)