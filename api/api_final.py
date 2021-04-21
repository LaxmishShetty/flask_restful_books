from flask import Flask,request,jsonify
import sqlite3
app = Flask(__name__)


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


@app.route('/', methods=['GET'])
def home():
    return "An api for all the books "


@app.route('/api/v1/resources/books/all', methods=['GET'])
def api_all():
    conn = sqlite3.connect('books.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()
    all_books = cur.execute('SELECT * FROM books;').fetchall()
    return jsonify(all_books)

@app.route('/api/v1/resources/books')
def api_filter():
    query_parameters = request.args
    id = query_parameters.get('id')
    published = query_parameters.get('published')
    author = query_parameters.get('author')

    query = 'SELECT * FROM books WHERE '
    to_filter = []
    if id:
        query = query + 'id=? AND '
        to_filter.append(id)

    if published:
        query = query + 'published=? AND '
        to_filter.append(published)

    if author:
        query = query + 'author=? AND '
        to_filter.append(author)

    query = query[:-4] + ';'

    conn = sqlite3.connect('books.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()
    result = cur.execute(query,to_filter).fetchall()

    return jsonify(result)





app.run()
