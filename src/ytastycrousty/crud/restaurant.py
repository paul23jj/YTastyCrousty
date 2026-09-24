from sqlalchemy.orm import Session

from ..models.restaurant import Restaurant
from ..schemas.restaurant import RestaurantUpdate, AvailabilityUpdate

def get_restaurants(db: Session):
    return db.query(Restaurant).all()

def get_restaurant(db: Session, restaurant_id: int):
    return db.get(Restaurant, restaurant_id)

def update_restaurant(db: Session, restaurant_id: int, data: RestaurantUpdate):
    restaurant = db.get(Restaurant, restaurant_id)
    if restaurant is None:
        return None
    update_data = data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(restaurant, field, value)
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