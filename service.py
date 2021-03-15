# from sqlalchemy.orm import Session
# from .main import Products, ProductIn
#
# def get_post_list(db: Session):
#     return db.query(Post).all()
#
# def create_post(db: Session, item: PostCreate):
#     post = Post(**item.dict())
#     db.add(post)
#     db.commit()
#     db.refresh(post)
#     return post