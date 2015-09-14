#!/usr/bin/env bash

usage() {
    echo "Usage $0 keyword parser"
    exit 1
}

[ $# -lt 2 ] && usage

keyword=$1
parser=$2

sqlite3 watchlist.db "insert into watchlist(keyword, parser) values('$keyword', '$parser')"
