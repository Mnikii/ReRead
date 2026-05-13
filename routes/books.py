from flask import Blueprint, jsonify, request, make_response, session
from app import create_session
from models import Books

books_bp = Blueprint('books', __name__)


@books_bp.route('/books/<int:id>', methods=['GET'])
def get_book(id):
    db_sess = create_session()
    book = db_sess.get(Books, id)
    db_sess.close()

    if book is None:
        return jsonify({'error': 'Not found'}), 404

    return jsonify({
        'id':          book.id,
        'title':       book.title,
        'author':      book.author,
        'condition':   book.condition,
        'owner_id':    book.owner_id,
        'location_id': book.location_id,
        'is_reserved': book.is_reserved,
    })



@books_bp.route('/books', methods=['POST'])
def create_book():
    user_id = session.get('user_id') #  проверка что пользователь залогинен

    if not request.json:
        return make_response(jsonify({'error': 'Empty request'}), 400)

    elif not all(key in request.json for key in
                 ['title', 'author', 'condition', 'location_id']):
        return make_response(jsonify({'error': 'Bad request'}), 400)

    if not user_id:
        return make_response(jsonify({'error': 'Unauthorized'}), 401)

    db_sess = create_session()
    book = Books(
        title=request.json['title'],
        author=request.json['author'],
        condition=request.json['condition'],
        owner_id=user_id,
        location_id=request.json['location_id']
    )
    db_sess.add(book)
    db_sess.commit()
    book_id = book.id
    db_sess.close()
    return jsonify({'id': book_id})


@books_bp.route('/books/<int:id>', methods=['DELETE'])
def delete_book(id):
    db_sess = create_session()
    book = db_sess.get(Books, id)

    if book is None:
        db_sess.close()
        return jsonify({'error': 'Not found'}), 404

    if book.owner_id != session.get('user_id'):
        db_sess.close()
        return jsonify({'error': 'Forbidden'}), 403

    db_sess.delete(book)
    db_sess.commit()
    db_sess.close()
    return jsonify({'success': 'OK'})


@books_bp.route('/my-books', methods=['GET'])
def my_books():
    user_id = session.get('user_id')
    if not user_id:
        return make_response(jsonify({'error': 'Unauthorized'}), 401)

    db_sess = create_session()
    books = db_sess.query(Books).filter(Books.owner_id == user_id).all()
    db_sess.close()

    return jsonify([{
        'id':          book.id,
        'title':       book.title,
        'author':      book.author,
        'condition':   book.condition,
        'location_id': book.location_id,
        'is_reserved': book.is_reserved,
    } for book in books])