#!/usr/bin/env python

import webbrowser
import keyword2magnet as k2m
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=["GET", "POST"])
def root():
    maxn = 5
    all_parsers = dict([ (p[0].replace("Parser", ''), p[1]) for p in k2m.getAllParserClass() ])
    all_parsers.pop("any", None)
    all_parser_names = all_parsers.keys()

    if request.method == "POST":
        search_word  = request.form["sw"]
        parser_used = request.form["parser"]

        check_src = dict([ (p, parser_used in p) for p in all_parsers.keys() ])
        selected_parser = [ k for k, v in check_src.items() if v == True][0]
        parser = all_parsers[selected_parser](search_word)
        tlist = parser.getTorrentInfo()[:maxn]
        # tlist = ["No matching result."] if not len(tlist) else tlist
        return render_template("index.html", all_parsers=all_parser_names, results=tlist, parser=parser)
    else:
        return render_template("index.html", all_parsers=all_parser_names)

if __name__ == "__main__":
    app.debug = True
    port = 5000
    url = 'http://127.0.0.1:%s' % port
    webbrowser.open_new(url)
    app.run()
