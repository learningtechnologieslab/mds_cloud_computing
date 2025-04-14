from flask import Flask, jsonify, request

app = Flask(__name__)

# Sample data: list of books
books = [
    {"id": 1, "title": "To Kill a Mockingbird", "author": "Harper Lee", "genre": "Fiction", "year": 1960},
    {"id": 2, "title": "1984", "author": "George Orwell", "genre": "Dystopian", "year": 1949},
    {"id": 3, "title": "Pride and Prejudice", "author": "Jane Austen", "genre": "Romance", "year": 1813}
]

# Route to get all books
@app.route('/books', methods=['GET'])
def get_books():
    return jsonify(books)

# Route to get a single book by ID
@app.route('/books/<int:book_id>', methods=['GET'])
def get_book(book_id):
    book = next((b for b in books if b["id"] == book_id), None)
    if book:
        return jsonify(book)
    return jsonify({"error": "Book not found"}), 404

# Route to add a new book
@app.route('/books', methods=['POST'])
def add_book():
    new_book = request.get_json()
    if "title" not in new_book or "author" not in new_book or "genre" not in new_book or "year" not in new_book:
        return jsonify({"error": "Missing required fields"}), 400
    
    new_book["id"] = max(book["id"] for book in books) + 1 if books else 1
    books.append(new_book)
    return jsonify(new_book), 201

# Route to update a book by ID
@app.route('/books/<int:book_id>', methods=['PUT'])
def update_book(book_id):
    book = next((b for b in books if b["id"] == book_id), None)
    if not book:
        return jsonify({"error": "Book not found"}), 404
    
    updated_data = request.get_json()
    book.update(updated_data)
    return jsonify(book)

# Route to delete a book by ID
@app.route('/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    global books
    books = [b for b in books if b["id"] != book_id]
    return jsonify({"message": "Book deleted successfully"})

if __name__ == '__main__':
    app.run(debug=True)
