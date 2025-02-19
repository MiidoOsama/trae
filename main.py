from fastapi import FastAPI
from items import Item
from uuid import UUID , uuid4
from pydantic import BaseModel
from database import Database


app = FastAPI()
db = Database.get_db()
collection  = db.get_collection('items')
@app.on_event("startup")
def startup_db_client():
    Database.connect_db()

@app.on_event("shutdown")
def shutdown_db_client():
    Database.close_db()

items = []
@app.get("/")
def index ():
    return {'message': 'API is running'}


@app.get('/items')
def get_items ():
    db = Database.get_db()
    item = list(db.items.find({}, {'_id': 0}))
    return items


@app.get('/items/{item_id}')
def get_item (item_id: UUID ):
    db = Database.get_db()
    item = db.items.find_one({'id': str(item_id)}, {'_id': 0})
    if item:
        return item
    return {'message': 'Item not found'}


@app.post('/items')
def create_item (item: Item):
    item_dict = item.model_dump()
    item_dict['id'] = str(uuid4())
    collection.insert_one(item_dict)
    return {'message': 'Item created'}


@app.delete('/items/{item_id}')
def delete_item (item_id: UUID ):
    result = collection.delete_one({'id': str(item_id)})
    if result.deleted_count == 1:
        return {'message': 'Item deleted'}
    return {'message': 'Item not found'}

@app.put('/items/{item_id}')
def update_item(item_id: UUID, item: Item):
    item_dict = item.model_dump()
    result = collection.update_one({'id': str(item_id)}, {'$set': item_dict})
    if result.modified_count == 1:
        return {'message': 'Item updated'}
    return {'message': 'Item not found'}