from app import db

class Item(db.Item):
    itemid = db.Column(db.Integer, primary_key=True)
    itemname = db.Column(db.String(100), unique=True, nullable=False)
    itemdescription = db.Column(db.String(255), nullable=True)