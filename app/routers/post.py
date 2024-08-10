from fastapi import FastAPI, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from app import models, schemas
from app.database import get_db
from typing import List



router = APIRouter()



@router.get("/posts", response_model=List[schemas.PostResponse])
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    if not posts:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="There is no any posts")        
    return posts



@router.post("/posts", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db)):
    new_post = models.Post(**post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post
        


@router.get("/posts/{id}",response_model=schemas.PostResponse)
def find_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post not found")
    return post



@router.delete("/posts/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id)
    if not post.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No posts with id:{id}")
    post.delete(synchronize_session=False)
    db.commit()



@router.put('/posts/{id}',response_model=schemas.PostResponse)
def update_post(id: int, updatedPost: schemas.PostCreate, db: Session = Depends(get_db)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    if not post_query.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No posts found with id:{id}")
    post_query.update(updatedPost.model_dump(),synchronize_session=False)
    db.commit()
    return post_query.first()