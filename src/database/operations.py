from sqlalchemy.orm import Session

# from . import model, schemas


from .model import Summary
from .schema import Item


def get_summaries(db: Session, skip: int = 0, limit: int = 20):
    # TODO: Add 'if None' return None condition
    return db.query(Summary).offset(skip).limit(limit).all()


def get_summary_by_title(db:Session, title: str):
    return db.query(Summary).filter(Summary.video_title == title).first()


def get_summary_by_url(db:Session, url: str):
    return db.query(Summary).filter(Summary.video_url == url).first()


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