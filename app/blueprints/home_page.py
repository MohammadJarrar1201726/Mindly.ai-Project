from flask import Blueprint, render_template

home_page_bp = Blueprint("home_page", __name__)

@home_page_bp.route('/')
def home():
    # TODO: commint to `comment`
    return render_template('homePage.html', commint="example")
