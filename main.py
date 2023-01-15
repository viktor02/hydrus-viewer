import io

from flask import Flask, render_template, request, send_file
from hydrus import Hydrus
import argparse
import logging


parser = argparse.ArgumentParser(prog='HydrusViewer')
parser.add_argument('access_key')
parser.add_argument('--bind', default="127.0.0.1")
parser.add_argument('--port', default=8020)
args = parser.parse_args()

app = Flask(__name__)
app.logger = None
hydrus = Hydrus(args.access_key)


@app.route('/')
def index():
    """ main search page """
    return render_template("main_page.html")


@app.route("/search", methods=["POST"])
def search():
    query = request.form["tags"]

    logging.info(f"Query: {query}")

    results = hydrus.search_tag(query)
    return render_template("search_results.html", file_ids=results)


@app.route("/thumb/<int:file_id>")
def get_thumbnail(file_id):
    return hydrus.load_thumbnail(file_id)


@app.route("/view/<int:file_id>")
def view_full(file_id):
    metadata = hydrus.get_metadata(file_id)
    tags = set()
    for service in metadata["tags"]:
        tags = metadata["tags"][service]["display_tags"]['0']
        break

    source = metadata["known_urls"]
    mimetype = metadata["mime"]

    return render_template("view_page.html", file_id=file_id, tags=tags, source=source, mime_type=mimetype)


@app.route("/get_fullsize/<int:file_id>")
def get_fullsize(file_id):
    image = hydrus.full_size(file_id)
    metadata = hydrus.get_metadata(file_id)
    mimetype = metadata["mime"]

    return send_file(io.BytesIO(image), mimetype=mimetype)


app.run(host=args.bind, port=args.port)
