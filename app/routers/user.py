from fastapi import status, HTTPException, Depends, APIRouter 
from sqlalchemy.orm import Session
from app import models, schemas, utils
from app.database import get_db



router = APIRouter(
    prefix="/users",
    tags=['Users']
)



@router.post('/',status_code=status.HTTP_201_CREATED)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    user.password = utils.hash(user.password) # passes user.password to utils.hash to perform hashing.
    new_user = models.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"msg":"Success"}



@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=schemas.UserOut)
def get_user(id : int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No User Found")
    return user