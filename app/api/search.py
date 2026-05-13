from flask import Blueprint, request, jsonify

from ..models.books import Book

search_bp = Blueprint('search', __name__)


# GET /books список всех книг с фильтрами
@search_bp.route('/books', methods=['GET'])
def get_books():
    """
    Search books by title, author, or city.
    ---
    tags:
      - search
    parameters:
      - in: query
        name: title
        type: string
      - in: query
        name: author
        type: string
      - in: query
        name: city
        type: string
    responses:
      200:
        description: List of books
    """
    # Берём параметры из строки запроса
    # например /books?title=гарри&author=роулинг
    title = request.args.get('title')
    author = request.args.get('author')
    city = request.args.get('city')

    query = Book.query

    # Применяем запрошенные фильтры
    if title:
        query = query.filter(Book.title.like(f'%{title}%'))
    if author:
        query = query.filter(Book.author.like(f'%{author}%'))
    if city:
        query = query.filter(Book.city.like(f'%{city}%'))

    books = query.all()

    # Делаем из списка объектов в список словарей
    result = []
    for book in books:
        result.append({
            'id': book.id,
            'title': book.title,
            'author': book.author,
            'condition': book.condition,
            'is_reserved': book.is_reserved,
            'owner_id': book.owner_id
        })

    return jsonify(result)

