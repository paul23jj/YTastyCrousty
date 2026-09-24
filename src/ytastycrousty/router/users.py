from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy.orm import Session

from ..crud import user as crud_user
from ..db.database import get_db
from ..security import verifier_admin
from ..schemas.user import UserCreate, UserOut


router = APIRouter()

@router.post("", response_model=UserOut, status_code=201, dependencies=[Depends(verifier_admin)])
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    return crud_user.create_user(db, user)
