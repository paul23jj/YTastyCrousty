from fastapi import HTTPException
from sqlalchemy.orm import Session

from ..models.restaurant import Restaurant
from ..schemas.restaurant import RestaurantUpdate, AvailabilityUpdate, CreationRestaurant

def get_restaurants(db: Session):
    return db.query(Restaurant).all()

def get_restaurant(db: Session, restaurant_id: int):
    return db.get(Restaurant, restaurant_id)

def update_restaurant(db: Session, restaurant_id: int, data: RestaurantUpdate):
    restaurant = db.get(Restaurant, restaurant_id)
    if restaurant is None:
        return None
    update_data = data.model_dump(exclude_unset=True)
    for nom, valeur in update_data.items():
        if valeur is None:
            raise HTTPException(status_code=422, detail=f"Le champ {nom} ne peut pas être null")
    if "name" in update_data:
        restaurant.name = update_data["name"]
    if "city" in update_data:
        restaurant.city = update_data["city"]
    if "address" in update_data:
        restaurant.address = update_data["address"]
    if "opening_hours" in update_data:
        restaurant.opening_hours = update_data["opening_hours"]
    if "contact" in update_data:
        restaurant.contact = update_data["contact"]
    db.commit()
    db.refresh(restaurant)
    return restaurant

def update_availability(db: Session, restaurant_id: int, data: AvailabilityUpdate):
    restaurant = db.get(Restaurant, restaurant_id)
    if restaurant is None:
        return None
    restaurant.is_open = data.is_open
    db.commit()
    db.refresh(restaurant)
    return restaurant


def creer_restaurant(db: Session, data: CreationRestaurant):
    restaurant = db.query(Restaurant).filter(Restaurant.name == data.name).first()
    if restaurant is not None:
        raise HTTPException(status_code=400, detail="Ce restaurant existe déjà")
    restaurant = Restaurant()
    restaurant.name = data.name
    restaurant.city = data.city
    restaurant.address = data.address
    restaurant.is_open = data.is_open
    restaurant.opening_hours = data.opening_hours
    restaurant.contact = data.contact
    db.add(restaurant)
    db.commit()
    db.refresh(restaurant)
    return restaurant
