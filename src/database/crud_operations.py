from sqlalchemy.orm import Session
from fastapi import HTTPException, status
# from . import model, prompts_and_schemas


from .model import Summary
from .schema import Item


def get_summaries(db: Session, skip: int = 0, limit: int = 20):
    # TODO: Add 'if None' return None condition
    # TODO: Sort so the latest would be on top
    return db.query(Summary).offset(skip).limit(limit).all()


def get_summary_by_id(db: Session, summ_id: int):
    return db.query(Summary).filter(Summary.id == summ_id).first()


def check_if_exists(db: Session, vid_id: str):
    """Checking if summary with given URL identifier (vid_id) already exists in db"""
    record = db.query(Summary).filter(Summary.video_id == vid_id).first()
    return record


def add_summary(db: Session,  summary: Item):
    with db as db:
        try:
            # check if summary exists here.
            db_summary = Summary(**summary.dict())
            db.add(db_summary)
            db.commit()
            db.refresh(db_summary)
            print("successfully created summary")
            return db_summary
        except Exception as e:
            print(f"Exception happened: {e}")


def update_existing_summary(db:Session, id, summary: Item):
    with db:
        try:
            record = db.query(Summary).filter(Summary.id == id).first()

            updated_data = summary.dict(exclude_unset=True)
            for key, value in updated_data.items():
                setattr(record, key, value)

            db.commit()
            db.refresh(record)
            print("Summary successfully updated.")
            return record
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
