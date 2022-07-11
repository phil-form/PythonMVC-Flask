from sys import stderr

from app import db
from app.models.Item import Item
from flask import session


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
