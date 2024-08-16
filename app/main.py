from fastapi import FastAPI
from . import models
from .database import engine
from .routers import post, user


models.Base.metadata.create_all(bind=engine) # This line is typically executed to create database tables based on the models defined in your application.


app = FastAPI() # creates an object


app.include_router(post.router) # include routers of posts
app.include_router(user.router) # include routers of users


# Root
@app.get("/")
def root():
    return {"message":"Welcome to my API!!!"}