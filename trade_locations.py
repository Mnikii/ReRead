from app import app
from models import db, Location

with app.app_context():
    # Точки обмена
    locations = [
        Location(name='Библиотека №1', address='ул. Ленина, 10'),
        Location(name='Кофейня Bookmate', address='пр. Мира, 25'),
        Location(name='Коворкинг «Точка»', address='ул. Садовая, 5'),
    ]

    db.session.add_all(locations)
    db.session.commit()