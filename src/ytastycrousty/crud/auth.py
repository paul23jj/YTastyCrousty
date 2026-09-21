from sqlalchemy.orm import Session
from ..models.user import User
from ..security import verify_password


def authentifier_user(db: Session, username: str, password: str):
    #on cherche si un utiliser avec ce nom existe
    user = db.query(User).filter(User.username == username).first()
    if user is None:
        return None

    #on vérifie le mdp
    if not verify_password(password, user.password):
        return None
    
    #si les 2 tests bons alors on renvoit la connexion de l'utilisateur
    return user
        