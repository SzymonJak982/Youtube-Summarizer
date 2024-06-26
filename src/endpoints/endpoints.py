from sqlalchemy.orm import Session
from src.database.model import Summary
from fastapi import FastAPI, Depends
from typing import Dict, List
from src.database import schema, operations
from src.database.database import SessionLocal

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/summaries/", response_model=List[schema.Item])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = operations.get_summaries(db, skip=skip, limit=limit)
    return users


# @app.post("/summaries/")
# def add_summary(db:Session,  summary):
#     with db as db:
#         try:
#             db.add(summary)
#             db.commit()
#             print("successfully created summary")
#             return summary
#         except Exception as e:
#             print(f"Exception happened: {e}")

