from flask import Blueprint, jsonify
from models import db, Book, Location

exchange_bp = Blueprint('exchange', __name__)

# POST /books/<id>/request — забронировать книгу
@exchange_bp.route('/books/<int:book_id>/request', methods=['POST'])
def request_book(book_id):
    book = Book.query.get(book_id)

    # Если книга не найдена
    if book is None:
        return jsonify({'error': 'Книга не найдена'}), 404

    # Если книга уже забронирована
    if book.is_reserved:
        return jsonify({'error': 'Книга уже забронирована'}), 400

    # Меняем статус и сохраняем
    book.is_reserved = True
    db.session.commit()

    return jsonify({'message': 'Книга успешно забронирована', 'book_id': book.id})


# GET /locations список всех точек обмена
@exchange_bp.route('/locations', methods=['GET'])
def get_locations():
    locations = Location.query.all()

    result = []
    for loc in locations:
        result.append({
            'id': loc.id,
            'name': loc.name,
            'address': loc.address
        })

    return jsonify(result)