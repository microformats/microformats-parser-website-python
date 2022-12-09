import json
import traceback
from collections import OrderedDict
from optparse import OptionParser

import mf2py
import mf2util
from flask import Flask, jsonify, make_response, render_template, request

parser = OptionParser()

parser.add_option(
    "-d",
    "--debug",
    action="store_true",
    default=False,
    help="Run application in debug mode",
)

parser.add_option(
    "-p",
    "--port",
    action="store",
    type="int",
    dest="port",
    default="8080",
    help="Change dev server port (default is 8080)",
)

(options, args) = parser.parse_args()

app = Flask(__name__)

mf2py.Parser.user_agent = "python.microformats.io (mf2py/" + mf2py.__version__ + ") Mozilla/5.0 Chrome/29.0.1547.57 Safari/537.36"
mf2py.Parser.dict_class = OrderedDict

@app.route("/", methods=["GET", "POST"])
def index():
    try:
        util = request.args.get("util") or request.form.get("util")
        url = request.args.get("url") or request.form.get("url")
        doc = request.args.get("doc") or request.form.get("doc")
        parser = request.args.get("parser") or request.form.get("parser")
        callback = request.args.get("callback") or request.form.get("callback")

        cached_mf2 = {}

        def fetch_mf2(url):
            if url in cached_mf2:
                return cached_mf2[url]
            p = mf2py.parse(url=url, html_parser=parser or None, img_with_alt = True)
            cached_mf2[url] = p
            return p

        if url or doc:
            p = mf2py.parse(
                url=url or None, doc=doc or None, html_parser=parser or None, img_with_alt = True
            )
            if util:
                if any("h-feed" in item["type"] for item in p["items"]):
                    p = mf2util.interpret_feed(
                        p, url, want_json=True, fetch_mf2_func=fetch_mf2
                    )
                else:
                    p = mf2util.interpret(
                        p, url, want_json=True, fetch_mf2_func=fetch_mf2
                    )
            if callback:
                response = make_response("{}({})".format(callback, json.dumps(p)), 200)
                response.headers["Content-Type"] = "text/javascript"
            else:
                response = make_response(json.dumps(p, indent=True), 200)
                response.headers["Content-Type"] = "application/json"
            return response

        return render_template("index.jinja2", mf2py_version=mf2py.__version__)
    except BaseException as e:
        traceback.print_exc()
        return jsonify(error="%s: %s" % (type(e).__name__, e)), 400


if options.debug:
    app.run(debug=True, port=options.port)
