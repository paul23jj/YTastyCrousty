from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..db.database import get_db
from ..schemas.restaurant import RestaurantOut, RestaurantUpdate, AvailabilityUpdate
from ..crud import restaurant as crud_restaurant
from ..crud import order as crud_order
from ..models.user import User
from ..schemas.order import OrderOut
from ..security import recuperer_utilisateur

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

@router.get("/{restaurant_id/orders", response_model=list[OrderOut])
def list_restaurant_orders(restaurant_id: int, status: str | None = None, db: Session = Depends(get_db), user: User = Depends(recuperer_utilisateur) ):
    return crud_order.lister_commandes_restaurant(db, restaurant_id, user, status)

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