from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..db.database import get_db
from ..schemas.restaurant import RestaurantOut, RestaurantUpdate, AvailabilityUpdate
from ..crud import restaurant as crud_restaurant

router = APIRouter()

@router.get("/", response_model=list[RestaurantOut])
def list_restaurants(db: Session = Depends(get_db)):
    return crud_restaurant.get_restaurants(db)

@router.get("/{restaurant_id}", response_model=RestaurantOut)
def get_restaurant(restaurant_id: int, db: Session = Depends(get_db)):
    restaurant = crud_restaurant.get_restaurant(db, restaurant_id)
    if restaurant is None:
        raise HTTPException(status_code=404, detail="restaurant introuvable")
    return restaurant

@router.patch("/{restaurant_id}", response_model=RestaurantOut)
def update_restaurant(restaurant_id: int, data: RestaurantUpdate, db: Session = Depends(get_db)):
    restaurant = crud_restaurant.update_restaurant(db, restaurant_id, data)
    if restaurant is None:
        raise HTTPException(status_code=404, detail="restaurant introuvable")
    return restaurant

@router.patch("/{restaurant_id}/availability", response_model=RestaurantOut)
def update_availability(restaurant_id: int, data: AvailabilityUpdate, db: Session = Depends(get_db)):
    restaurant = crud_restaurant.update_availability(db, restaurant_id, data)
    if restaurant is None:
        raise HTTPException(status_code=404, detail="restaurant introuvable")
    return restaurant