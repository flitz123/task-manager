def get_user_email(db, email):
    return db.query(User).filter(User.email == email).first()
