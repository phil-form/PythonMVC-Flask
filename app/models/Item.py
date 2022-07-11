from app import db
from sqlalchemy.sql import func


class Item(db.Model):
    itemid = db.Column(db.Integer, primary_key=True)
    itemname = db.Column(db.String(255), nullable=False)
    itemdescription = db.Column(db.Text, nullable=False)
    createdate = db.Column(db.DateTime, nullable=False, default=func.now())
    updatedate = db.Column(db.DateTime, nullable=True, onupdate=func.now())
    deletedate = db.Column(db.DateTime, nullable=True)
    active = db.Column(db.Boolean, nullable=False, default=True)
