from app import create_app
from app.extensions import db
from app.models.location import Location

app = create_app()

with app.app_context():
    # Точки обмена
    locations = [
        Location(name='Библиотека №1', address='ул. Ленина, 10'),
        Location(name='Кофейня Bookmate', address='пр. Мира, 25'),
        Location(name='Коворкинг "Точка"', address='ул. Садовая, 5'),
    ]

    db.session.add_all(locations)
    db.session.commit()
