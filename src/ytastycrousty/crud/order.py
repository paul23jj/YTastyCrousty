from decimal import Decimal

from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from ..models.order import Order, OrderItem
from ..models.product import Product
from ..models.restaurant import Restaurant
from ..models.user import User
from ..schemas.order import OrderCreate, OrderStatusUpdate


def enregistrer_modifications(db: Session) -> None:
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail="Opération incompatible avec les données de commande",
        ) from None


def verifier_acces_restaurant(user: User, restaurant_id: int) -> None:
    if user.role == "staff" and user.restaurant_id != restaurant_id:
        raise HTTPException(
            status_code=403,
            detail="Accès interdit à ce restaurant",
        )


def recuperer_restaurant(db: Session, restaurant_id: int) -> Restaurant:
    restaurant = db.get(Restaurant, restaurant_id)
    if restaurant is None:
        raise HTTPException(status_code=404, detail="Restaurant introuvable")
    return restaurant


def recuperer_commande_par_numero(db: Session, order_number: str) -> Order:
    order = db.query(Order).filter(Order.order_number == order_number).first()
    if order is None:
        raise HTTPException(status_code=404, detail="Commande introuvable")
    return order


def creer_commande(db: Session, data: OrderCreate) -> Order:
    restaurant = recuperer_restaurant(db, data.restaurant_id)

    if not restaurant.is_open:
        raise HTTPException(
            status_code=400,
            detail="Le restaurant est fermé",
        )

    order = Order()
    order.restaurant_id = data.restaurant_id
    order.status = "pending"
    order.pickup_mode = data.pickup_mode
    order.customer = data.customer.model_dump()

    total_price = Decimal("0")

    for item_data in data.items:
        product = db.get(Product, item_data.product_id)

        if product is None:
            raise HTTPException(status_code=404, detail="Produit introuvable")

        if product.restaurant_id != data.restaurant_id:
            raise HTTPException(
                status_code=400,
                detail="Le produit appartient à un autre restaurant",
            )

        if not product.is_available:
            raise HTTPException(
                status_code=400,
                detail="Le produit est indisponible",
            )

        order_item = OrderItem()
        order_item.product_id = product.id
        order_item.quantity = item_data.quantity
        order_item.unit_price = product.price

        order.items.append(order_item)

        total_price += product.price * item_data.quantity

    order.total_price = total_price

    db.add(order)
    enregistrer_modifications(db)
    db.refresh(order)

    return order


def lister_commandes_restaurant(
    db: Session,
    restaurant_id: int,
    user: User,
    status: str | None = None,
) -> list[Order]:
    recuperer_restaurant(db, restaurant_id)
    verifier_acces_restaurant(user, restaurant_id)

    query = db.query(Order).filter(Order.restaurant_id == restaurant_id)

    if status is not None:
        query = query.filter(Order.status == status)

    return query.all()


def modifier_statut_commande(
    db: Session,
    order_number: str,
    data: OrderStatusUpdate,
    user: User,
) -> Order:
    order = recuperer_commande_par_numero(db, order_number)
    verifier_acces_restaurant(user, order.restaurant_id)

    order.status = data.status

    enregistrer_modifications(db)
    db.refresh(order)

    return order


def annuler_commande(db: Session, order_number: str, user: User) -> Order:
    order = recuperer_commande_par_numero(db, order_number)
    verifier_acces_restaurant(user, order.restaurant_id)

    if order.status in {"collected", "cancelled"}:
        raise HTTPException(
            status_code=400,
            detail="Cette commande ne peut plus être annulée",
        )

    order.status = "cancelled"

    enregistrer_modifications(db)
    db.refresh(order)

    return order