from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from app import models, schemas
from app.database import get_db
from typing import List 


# Router creates routes to all apis of a kind
router = APIRouter(
    prefix="/posts", #add prefix to all routes
    tags=['Posts'] #creates a group in swaggerui
)



# API fetches all the entries from database and return. 
@router.get("/", response_model=List[schemas.PostResponse]) # "List" in this statement unpacks those objects as dictionaries and returns list of dictionaries.
def get_posts(db: Session = Depends(get_db)): # db: Session = Depends(get_db) creates a session for database query.
    posts = db.query(models.Post).all() # .all() return all posts as list of objects.
    if not posts: # checks if there is no post found
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="There is no any posts") # raise an error.     
    return posts



# API creates new entry and writes to database
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db)): #This creates a new post, which need user input thus stores the input in 'post' variable according to schema.
    new_post = models.Post(**post.model_dump()) # **post.model_dump() gets the post and converts it into dictionary then unpacks (**) and passedto models.Post().
    db.add(new_post) # adds new post
    db.commit() # writes data to database, Note: All write operations need to be commited.
    db.refresh(new_post) # refetches the added post to return result.
    return new_post
        


# API fetches an entry by its 'id'.
@router.get("/{id}",response_model=schemas.PostResponse)
def find_post(id: int, db: Session = Depends(get_db)): # pass an 'id' argument
    post = db.query(models.Post).filter(models.Post.id == id).first() # .filter() allows condition and .first() fetches first entry.
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post not found")
    return post



# API deletes entry with respect to 'id'
@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id) # this returns only query
    if not post.first(): # .first() cuz 'post' has query not data.
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No posts with id:{id}")
    post.delete(synchronize_session=False) #check documentation
    db.commit()
    # delete operation does not return anything



# API updates an entry with respect to 'id'
@router.put('/{id}',response_model=schemas.PostResponse)
def update_post(id: int, updatedPost: schemas.PostCreate, db: Session = Depends(get_db)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    if not post_query.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No posts found with id:{id}")
    post_query.update(updatedPost.model_dump(),synchronize_session=False)
    db.commit()
    return post_query.first()