from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session

from ..crud import product as crud_product
from ..db.database import get_db
from ..security import verifier_droits_produit
from ..models.user import User
from ..schemas.product import (
    DisponibiliteProduit, CreationProduit, ProduitReponse, ModificationProduit,
)


router = APIRouter(responses={
    400: {"description": "Opération incompatible avec les données existantes"},
    401: {"description": "Authentification absente ou invalide"},
    403: {"description": "Rôle ou restaurant non autorisé"},
    404: {"description": "Produit ou restaurant introuvable"},
})


def verifier_ingredients(ingredients: list[str]):
    for ingredient in ingredients:
        if len(ingredient) < 1 or len(ingredient) > 255:
            raise HTTPException(
                status_code=422,
                detail="Chaque ingrédient doit contenir entre 1 et 255 caractères",
            )


def verifier_champs_null(champs: dict):
    for nom, valeur in champs.items():
        if nom != "image" and valeur is None:
            raise HTTPException(
                status_code=422,
                detail=f"Le champ {nom} ne peut pas être null",
            )


@router.get("", response_model=list[ProduitReponse])
def lister_produits(
    category: str | None = None,
    q: str | None = None,
    restaurant_id: int | None = None,
    is_available: bool | None = None,
    db: Session = Depends(get_db),
):
    return crud_product.lister_produits(db, category, q, restaurant_id, is_available)


@router.get("/{product_id}", response_model=ProduitReponse)
def recuperer_produit(product_id: int, db: Session = Depends(get_db)):
    return crud_product.recuperer_produit(db, product_id)


@router.post("", response_model=ProduitReponse, status_code=201)
def creer_produit(
    data: CreationProduit,
    db: Session = Depends(get_db),
    user: User = Depends(verifier_droits_produit),
):
    verifier_ingredients(data.ingredients)
    return crud_product.creer_produit(db, data, user)


@router.patch("/{product_id}", response_model=ProduitReponse)
def modifier_produit(
    product_id: int,
    data: ModificationProduit,
    db: Session = Depends(get_db),
    user: User = Depends(verifier_droits_produit),
):
    champs = data.model_dump(exclude_unset=True)
    verifier_champs_null(champs)
    if "ingredients" in champs:
        verifier_ingredients(champs["ingredients"])
    return crud_product.modifier_produit(db, product_id, data, user)


@router.patch("/{product_id}/availability", response_model=ProduitReponse)
def modifier_disponibilite(
    product_id: int,
    data: DisponibiliteProduit,
    db: Session = Depends(get_db),
    user: User = Depends(verifier_droits_produit),
):
    return crud_product.modifier_produit(
        db, product_id, ModificationProduit(is_available=data.is_available), user,
    )


@router.delete("/{product_id}", status_code=204, response_class=Response)
def supprimer_produit(
    product_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(verifier_droits_produit),
):
    crud_product.supprimer_produit(db, product_id, user)
    return Response(status_code=204)
