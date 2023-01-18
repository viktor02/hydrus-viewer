import argparse
import logging
import io

import flask
from flask import Flask, render_template, request, send_file, abort
import importlib.metadata


from .hydrus import Hydrus

app = Flask(__name__)

parser = argparse.ArgumentParser(prog='hydrus-viewer')
parser.add_argument('access_key')
parser.add_argument('--bind', default="127.0.0.1")
parser.add_argument('--port', default=8020)
parser.add_argument('-v', '--version', action='version', version=importlib.metadata.version("hydrus_viewer"))
args = parser.parse_args()

logging.basicConfig(level=logging.INFO)
logging.getLogger("werkzeug").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

hydrus = Hydrus(args.access_key)


@app.route('/')
def index():
    """ main search page """
    return render_template("main_page.html")


@app.route("/search/<int:page>", methods=["POST", "GET"])
def search(page=1):
    """ page with found content """
    if flask.request.method == 'POST':
        query = request.form["tags"]
    else:
        query = request.args.get('tags')

    if query is "":
        abort(404)

    logger.info(f"Query: {query}")

    results = hydrus.get_page(query, page)
    return render_template("search_results.html", file_ids=results, query=query, current_page=page)


@app.route("/view/<int:file_id>")
def view_full(file_id):
    """ page with viewing full-sized content"""
    try:
        metadata = hydrus.get_metadata(file_id)

        if metadata is None:
            abort(404)

        tags = set()
        for service in metadata["tags"]:
            tags = metadata["tags"][service]["display_tags"]['0']
            break

        return render_template("view_page.html", file_id=file_id, tags=tags, metadata=metadata)
    except KeyError:
        return abort(404)


@app.route("/thumb/<int:file_id>")
def get_thumbnail(file_id):
    """ returns thumbnails """
    return hydrus.get_thumbnail(file_id)


@app.route("/full/<int:file_id>")
def get_fullsize(file_id):
    """ returns full-sized images """
    image = hydrus.full_size(file_id)
    metadata = hydrus.get_metadata(file_id)
    mimetype = metadata["mime"]

    return send_file(io.BytesIO(image), mimetype=mimetype)


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html', title='404'), 404


def main():
    logger.info(f"Server starting on {args.bind}:{args.port}")
    app.run(host=args.bind, port=args.port)


if __name__ == "__main__":
    main()
