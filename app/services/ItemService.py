from sys import stderr

from flask import session
from app.models.Item import Item
from app import db
import bcrypt

class ItemService():

    def findAll(self):
        return Item.query.all()

    def findOne(self, dataId: int):
        return Item.query.get(dataId)

    def findOneBy(self, **kwargs):
        return Item.query.filter_by(**kwargs).first()

    def insert(self, data: Item):
        db.session.add(data)
        db.session.commit()