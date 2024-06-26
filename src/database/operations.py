from sqlalchemy.orm import Session

# from . import model, schemas


from .model import Summary
from .schema import Item


def get_summaries(db: Session, skip: int = 0, limit: int = 20):
    return db.query(Summary).offset(skip).limit(limit).all()


def add_summary(db:Session,  summary):
    with db as db:
        try:
            db.add(summary)
            db.commit()
            print("successfully created summary")
            return summary
        except Exception as e:
            print(f"Exception happened: {e}")