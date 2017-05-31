from pymongo import MongoClient
# import datetime
import csv
import sys
sys.path.insert(0, '../')

from helper import *
from settings import *

"""
Create random products, following the collection pattern given 
"""

# Connection
client = MongoClient(DATABASE_NAME, DATABASE_PORT)
db = client.sb_db
products_collection = db.products

client_id = createHash()

# Generate products via csv
with open('global.csv', 'rb') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        if not row[4]:
            row[4] = row[5]
        if checkIfRepresentsFloat(row[5]):
            data = {
                "client_id": client_id,
                "product_id": createHash(),
                "title": row[8],
                "description": row[8],
                "categories": [row[0],row[1]],
                "subcategories": [row[0], row[1]],
                "price": row[5],
                "normal_price": row[4],
                "active": True,
                "updated_at": datetime.utcnow(),
                "created_at": datetime.utcnow(),
                "synced" : True
            }
            product_id = products_collection.insert_one(data).inserted_id
            print product_id