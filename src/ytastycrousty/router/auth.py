from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from ..db.database import get_db
from ..schemas.user import LoginRequest, TokenResponse
from ..crud import user as crud_user
from ..security import verify_password, create_access_token

router = APIRouter()

@router.post('/login', response_model=TokenResponse)
async def login(credentials: LoginRequest, db: AsyncSession = Depends(get_db)):
    user = await crud_user.get_user_by_identifiant(db, credentials.identifiant)
    if user is None or not verify_password(credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='identifiant ou mot de passe incorrect')
    access_token = create_access_token({'sub': str(user.user_id), 'role': user.role})
    return TokenResponse(access_token=access_token)