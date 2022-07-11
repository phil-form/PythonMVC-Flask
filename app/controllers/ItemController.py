from sys import stderr

from app import app
from app.services.ItemService import ItemService
from flask import redirect, render_template, request, session, url_for

itemService = ItemService()


class ItemController:
    @app.route('/items', methods=["GET"])
    def getItemList():
        items = itemService.findAll()

        return render_template('items/list.html', items=items)

    @app.route('/items/<int:itemid>', methods=["GET"])
    def getOneItem(itemid: int):
        item = itemService.findOne(itemid)

        return render_template('items/item.html', item=item)
