from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from ..security import verifier_droits_restaurant
from ..models.product import Product
from ..models.restaurant import Restaurant
from ..models.user import User
from ..schemas.product import CreationProduit, ModificationProduit


def recuperer_produit(db: Session, product_id: int) -> Product:
    product = db.get(Product, product_id)
    if product is None:
        raise HTTPException(status_code=404, detail="Produit introuvable")
    return product


def verifier_restaurant(db: Session, restaurant_id: int) -> None:
    if db.get(Restaurant, restaurant_id) is None:
        raise HTTPException(status_code=404, detail="Restaurant introuvable")


def enregistrer_modifications(db: Session) -> None:
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail="Opération incompatible avec les données liées au produit",
        ) from None


def creer_produit(db: Session, data: CreationProduit, user: User) -> Product:
    verifier_droits_restaurant(user, data.restaurant_id)
    verifier_restaurant(db, data.restaurant_id)
    product = Product()
    product.name = data.name
    product.image = None
    if data.image is not None:
        product.image = str(data.image)
    product.description = data.description
    product.category = data.category
    product.price = data.price
    product.is_available = data.is_available
    product.restaurant_id = data.restaurant_id
    product.ingredients = data.ingredients
    db.add(product)
    enregistrer_modifications(db)
    db.refresh(product)
    return product


def modifier_produit(
    db: Session, product_id: int, data: ModificationProduit, user: User,
) -> Product:
    product = recuperer_produit(db, product_id)
    verifier_droits_restaurant(user, product.restaurant_id)
    changes = data.model_dump(exclude_unset=True)
    if "restaurant_id" in changes:
        verifier_droits_restaurant(user, changes["restaurant_id"])
        verifier_restaurant(db, changes["restaurant_id"])
    if "name" in changes:
        product.name = changes["name"]
    if "image" in changes:
        if changes["image"] is None:
            product.image = None
        else:
            product.image = str(changes["image"])
    if "description" in changes:
        product.description = changes["description"]
    if "category" in changes:
        product.category = changes["category"]
    if "price" in changes:
        product.price = changes["price"]
    if "is_available" in changes:
        product.is_available = changes["is_available"]
    if "restaurant_id" in changes:
        product.restaurant_id = changes["restaurant_id"]
    if "ingredients" in changes:
        product.ingredients = changes["ingredients"]
    enregistrer_modifications(db)
    db.refresh(product)
    return product


def supprimer_produit(db: Session, product_id: int, user: User) -> None:
    product = recuperer_produit(db, product_id)
    verifier_droits_restaurant(user, product.restaurant_id)
    db.delete(product)
    enregistrer_modifications(db)
