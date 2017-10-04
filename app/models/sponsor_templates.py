from datetime import datetime, timedelta
from app.models.base_model import BaseModel
from app.models import db

class SponsorTemplate(db.Model, BaseModel):
    
    __tablename__ = 'sponsor_templates'

    visible = ['id', 'sponsor_id', 'message', 'attachment', 'redirect_url', 'created_at', 'updated_at']

    id = db.Column(db.Integer, primary_key=True)
    sponsor_id = db.Column(
        db.Integer,
        db.ForeignKey('sponsors.id'),
        nullable=False
    )
    message = db.Column(db.Text)
    attachment = db.Column(db.String)
    redirect_url = db.Column(db.String)
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)

    def __init__(self):
        self.message = "insert message here"
        self.redirect_url = "insert web promo here"
        self.created_at = datetime.now()
        self.updated_at = datetime.now()