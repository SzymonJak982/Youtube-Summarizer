from sqlalchemy.orm import Session
from fastapi import HTTPException, status
# from . import model, prompts_and_schemas


from .model import Summary
from .schema import Item


def get_summaries(db: Session, skip: int = 0, limit: int = 20):
    # TODO: Add 'if None' return None condition
    # TODO: Sort so the newest would be on top
    return db.query(Summary).offset(skip).limit(limit).all()


def get_summary_by_id(db: Session, summ_id: int):
    return db.query(Summary).filter(Summary.id == summ_id).first()


# TODO: Add option for deleting duplicates used in dev and testing
# ### specific for search/get operations:
# def get_summary_by_title(db:Session, title: str):
#     return db.query(Summary).filter(Summary.video_title.like(title))


def get_summary_by_url(db:Session, url: str):
    return db.query(Summary).filter(Summary.video_url == url).first()
###


def add_summary(db: Session,  summary: Item):
    with db as db:
        try:
            db_summary = Summary(**summary.dict())
            db.add(db_summary)
            db.commit()
            db.refresh(db_summary)
            print("successfully created summary")
            return db_summary
        except Exception as e:
            print(f"Exception happened: {e}")



# def delete_summary(db: Session, summary:int):
#     with db as db:
#         try:
#             if summary is None:
#                 raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                                     detail=f"post with id: {id} does not exist")
#
#             summary.delete(synchronize_session=False)
#             db.commit()
#             db.refresh(db)
#
#         except Exception as e:
#             print(f"Exception happened: {e}")
