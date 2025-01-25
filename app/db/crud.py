from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.db.model import WhiteListUser


def add_user_to_white_list(db: Session, user_id: int, username: str):
    new_user = WhiteListUser(user_id=user_id, username=username)

    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    except IntegrityError:
        db.rollback()
        raise ValueError("User with this user_id already exists.")

def get_all_white_list_users(db: Session):
    """
    Возвращает список всех пользователей в белом списке.
    """
    return db.query(WhiteListUser).all()