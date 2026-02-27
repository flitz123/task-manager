def get_tasks(db, user_id, skip=0, limit=10):
    return db.query(Task)\
        .filter(Task.owner_id == user_id)\
        .offset(skip).limit(limit).all()
