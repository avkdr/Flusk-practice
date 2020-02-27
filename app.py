from flask import Flask, jsonify, request, Response, json

app = Flask(__name__)

books = [
    {
        'name': 'Green Eggs and Ham',
        'price': 7.99,
        'isbn': 100
    },
    {
        'name': 'The Cat in the Hat',
        'price': 6.99,
        'isbn': 200
    }
]


def valid_book_object(book_object):
    if 'name' in book_object and 'price' in book_object and 'isbn' in book_object:
        return True
    else:
        return False


# GET /store
@app.route('/books')
def get_books():
    return jsonify({'books': books})


# POST /books
@app.route('/books', methods=['POST'])
def add_book():
    request_data = request.get_json()
    if valid_book_object(request_data):
        new_book = {
            'name': request_data['name'],
            'price': request_data['price'],
            'isbn': request_data['isbn']
        }
        books.insert(0, new_book)
        response = Response('', 201, mimetype='application/json')
        response.headers['Location'] = '/books/' + str(new_book['isbn'])
        return response
    else:
        invalid_book_object_error_msg = {
            'error': 'Invalid book object passed in request',
            'helpString': "Data passed in similar to this {'name':'bookname', 'price':'5.5', 'isbn':'777'}"
        }
        response = Response(json.dumps(invalid_book_object_error_msg), status=400, mimetype='application/json')
        return response


# GET /books/100
@app.route('/books/<int:isbn>')
def get_book_by_isbn(isbn):
    return_value = {}
    for book in books:
        if book['isbn'] == isbn:
            return_value = {
                'name': book['name'],
                'price': book['price']
            }
    return jsonify(return_value)


# PUT
@app.route('/books/<int:isbn>', methods=['PUT'])
def replace_book(isbn):
    request_data = request.get_json()
    new_book = {
        'name': request_data['name'],
        'price': request_data['price'],
        'isbn': isbn
    }
    i = 0;
    for book in books:
        current_isbn = book['isbn']
        if current_isbn == isbn:
            books[i] = new_book
        i += 1
    response = Response()


app.run(port=5000)
