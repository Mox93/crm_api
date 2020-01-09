from flask import Blueprint, render_template, url_for


web = Blueprint("site", __name__, template_folder="templates", static_folder="static",
                static_url_path="/web/static")


@web.route("/")
def root():
    return render_template("index.html")


@web.route("/<path:url>")
def any_endpoint(url):
    return render_template("index.html")

