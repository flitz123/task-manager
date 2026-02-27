from app.core.security import hash_password, verify_password
from app.models.user import User
from app.models.role import Role


def registered_user(db, email, password):
    role = db.query(Role).filter(Role.name == "user").first()
    user = User(email=email, hash_password=hash_password(password), role=role)
    db.add(User)
    db.commit
    db.refresh(User)
    return user
