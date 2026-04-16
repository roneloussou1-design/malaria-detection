from sqlalchemy import create_engine, Column, String, Float, DateTime
from sqlalchemy.orm import DeclarativeBase, Session
from datetime import datetime
import uuid
import os

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "sqlite:///./malaria.db"
)

engine = create_engine(DATABASE_URL)

class Base(DeclarativeBase):
    pass

class Prediction(Base):
    __tablename__ = "predictions"

    id          = Column(String, primary_key=True,
                         default=lambda: str(uuid.uuid4()))
    type        = Column(String)
    result      = Column(String)
    confidence  = Column(Float)
    patient_id  = Column(String, nullable=True)
    agent_id    = Column(String, nullable=True)
    region      = Column(String, nullable=True)
    created_at  = Column(DateTime, default=datetime.utcnow)

def init_db():
    Base.metadata.create_all(engine)

def save_prediction(**kwargs) -> str:
    pred_id = str(uuid.uuid4())
    kwargs["id"] = pred_id
    with Session(engine) as session:
        session.add(Prediction(**kwargs))
        session.commit()
    return pred_id