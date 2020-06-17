#from flask import request
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
        type=float,
        required=True,
        help="This field can not be blank."
    )
    parser.add_argument('store_id',
        type=int,
        required=True,
        help="Every item needs a store ID."        
    )

    @jwt_required()
    def get(self, item_name):
        item = ItemModel.find_by_name(item_name)

        if item:
            return item.json()
        return {'message': f"{item_name} is not existed in database."}, 404        

    def post(self, item_name):
        if ItemModel.find_by_name(item_name):
            return {'message': f"An item with name '{item_name}' already exist."}, 400

        item_data = Item.parser.parse_args()
        item = ItemModel(item_name, **item_data)

        try:
            item.save_to_db()
        except:
            return {'message':'An error occured while inserting the item'}, 500 
        
        return item.json(), 201

    def delete(self, item_name):
        item = ItemModel.find_by_name(item_name)
        if item:
            item.delete_from_db()
            
        return {'message':'Item deleted'}

    def put(self, item_name):        
        item_data = Item.parser.parse_args()
        item = ItemModel.find_by_name(item_name)
        if item is None:
            item = ItemModel(item_name, **item_data)
        else:
            item.price = item_data['price']
        
        item.save_to_db()
        return item.json()

class ItemList(Resource):
    def get(self):
        return {'items':list(map(lambda x: x.json(), ItemModel.query.all()))}
        #or
        #return {'items':[x.json() for x in ItemModel.query.all()]}
        