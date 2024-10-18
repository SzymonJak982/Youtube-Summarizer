from sqlalchemy.orm import Session
# from src.database.model import Summary
from fastapi import FastAPI, Depends, HTTPException, Response, status
from typing import Dict, List
from src.database import schema, crud_operations
from src.database.database import SessionLocal
from src.database.database import get_db
import uvicorn
import logging
# import json

logging.basicConfig(level=logging.INFO)


app = FastAPI()


@app.post("/summaries/", response_model=schema.Item)
def add_summary2history(summary: schema.Item, db: Session = Depends(get_db)):
    logging.info(f"Received summary: {summary}")
    # TODO: Create separate schema for checking in db for same title and video_url- handle specific scenarios: as user may want to generate summary again
    # if_exists = operations.get_summary_by_title(db, )

    # if db_summary:
    #     return None
        # raise HTTPException(status_code=400, detail="")
    return crud_operations.add_summary(db, summary)


# TODO: Debug the issue with correct schema
@app.get("/summaries/", response_model=List[schema.Item])
def read_summaries_history(skip: int = 0, limit: int = 20, db: Session = Depends(get_db)):
    summaries = crud_operations.get_summaries(db, skip=skip, limit=limit)
    return summaries


@app.get("/summaries/{summ_id}", response_model=schema.Item)
def get_summary(summ_id: int, db: Session = Depends(get_db)):
    summary = crud_operations.get_summary_by_id(db, summ_id)
    if summary is None:
        raise HTTPException(status_code=404, detail="Summary for given ID not found")
    return summary
# check what kind of output we want:List?

@app.get("/summaries/check/{vid_id}", response_model=schema.UpdateItem)
def check_if_summary_exists(vid_id: str, db: Session = Depends(get_db)):
    summary = crud_operations.check_if_exists(db, vid_id)
    if summary is None:
        # raise HTTPException(status_code=404, detail="Summary not found")
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    return summary

# @app.get("/summaries/by_title/{summ_title}", response_model=schema.Item)
# def get_summary(summ_title: str, db: Session = Depends(get_db)):
#     summary = crud_operations.get_summary_by_title(db, summ_title)
#     if summary is None:
#         raise HTTPException(status_code=404, detail="Summary for given title not found")
#     return summary


@app.put("/summaries/{summ_id}", response_model=schema.UpdateItem)
def update_summary(summ_id: int, summary: schema.UpdateItem, db: Session = Depends(get_db)):
    summary = crud_operations.update_existing_summary(db, summ_id, summary)
    return summary


@app.delete("/summaries/{summ_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_summary(summ_id: int, db: Session = Depends(get_db)):

    summary = crud_operations.get_summary_by_id(db, summ_id)

    if summary is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")

    db.delete(summary)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


if __name__ == "__main__":
    uvicorn.run("endpoints:app", host="0.0.0.0", port=8000, reload=True)
