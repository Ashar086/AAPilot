from core.database import db
from datetime import datetime

class UserAnswer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(50), nullable=False)
    page_number = db.Column(db.Integer, nullable=False)
    answers = db.Column(db.JSON, nullable=False)
    embeddings = db.Column(db.JSON, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
