from sqlalchemy.orm import Session
from src.database.model import Summary
from fastapi import FastAPI, Depends, HTTPException
from typing import Dict, List
from src.database import schema, operations
from src.database.database import SessionLocal
import uvicorn
import logging
import json

logging.basicConfig(level=logging.INFO)


app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/summaries/", response_model=schema.Item)
def add_summary2history(summary: schema.Item, db: Session = Depends(get_db)):
    logging.info(f"Received summary: {summary}")
    # TODO: Create separate schema for checking in db for same title and video_url- handle specific scenarios: as user may want to generate summary again
    # if_exists = operations.get_summary_by_title(db, )

    # if db_summary:
    #     return None
        # raise HTTPException(status_code=400, detail="")
    return operations.add_summary(db, summary)


# TODO: Debug the issue with correct schema
# check what kind of output we want:List?
@app.get("/summaries/", response_model=List[schema.Item])
def read_summaries_history(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    summaries = operations.get_summaries(db, skip=skip, limit=limit)
    return summaries



if __name__ == "__main__":
    uvicorn.run("endpoints:app", host="0.0.0.0", port=8000, reload=True)
