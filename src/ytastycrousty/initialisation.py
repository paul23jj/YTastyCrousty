from sqlalchemy.orm import Session

from .models.restaurant import Restaurant


def initialiser_restaurants(db: Session):
    restaurants = [
        {
            "name": "Ytasty Crousty Aix",
            "city": "Aix-en-Provence",
            "address": "10 cours Mirabeau",
            "opening_hours": "11:30-22:30 du lundi au dimanche",
            "contact": "04 42 00 00 00",
        },
        {
            "name": "Ytasty Crousty Lyon",
            "city": "Lyon",
            "address": "8 rue Victor Hugo",
            "opening_hours": "11:30-22:00 du lundi au dimanche",
            "contact": "04 72 00 00 00",
        },
        {
            "name": "Ytasty Crousty Paris",
            "city": "Paris",
            "address": "12 rue de la Republique",
            "opening_hours": "11:30-22:30 du lundi au dimanche",
            "contact": "01 42 00 00 00",
        },
    ]

    for informations in restaurants:
        restaurant = db.query(Restaurant).filter(Restaurant.name == informations["name"]).first()
        if restaurant is None:
            restaurant = Restaurant()
            restaurant.name = informations["name"]
            restaurant.city = informations["city"]
            restaurant.address = informations["address"]
            restaurant.is_open = True
            restaurant.opening_hours = informations["opening_hours"]
            restaurant.contact = informations["contact"]
            db.add(restaurant)
    db.commit()
