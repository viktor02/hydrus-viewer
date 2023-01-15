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
logging.basicConfig(level=logging.INFO)
logging.getLogger("werkzeug").setLevel(logging.ERROR)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

hydrus = Hydrus(args.access_key)


@app.route('/')
def index():
    """ main search page """
    return render_template("main_page.html")


@app.route("/search", methods=["POST"])
@app.route("/search/<int:page>", methods=["POST"])
def search(page=1):
    query = request.form["tags"]

    logger.info(f"Query: {query}")

    results = hydrus.get_page(query, page)
    return render_template("search_results.html", file_ids=results, query=query, current_page=page)


@app.route("/thumb/<int:file_id>")
def get_thumbnail(file_id):
    return hydrus.get_thumbnail(file_id)


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


logger.info(f"Server starting on {args.bind}:{args.port}")
app.run(host=args.bind, port=args.port)
