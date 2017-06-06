# -*- coding: utf-8 -*-
from pymongo import MongoClient
from bson.objectid import ObjectId
import datetime
from helper import *
from settings import *
from pprint import pprint

"""
    Creating a new table representing the summary
"""

# Connection
client = MongoClient(DATABASE_NAME, DATABASE_PORT)
db = client.sb_db

summary_collection = db.summary
orders_collection = db.orders
customers_collection = db.customers
carts_collection = db.carts
products_collection = db.products

for order in orders_collection.find():
    order_products = []
    cart_document = carts_collection.find({"_id": ObjectId(order['cart_id'])}).limit(1)
    for cart_items in cart_document:
        for item in cart_items['products']:
            product_document = products_collection.find({"product_id": item['product_id']}).limit(1)
            for product in product_document:
                order_product_data = {
                    "order_date": str(order['created_at'].year) + str(order['created_at'].month),
                    "order_id": str(order['_id']),
                    "product_id": product['product_id'],
                    "quantity": item['quantity'],
                    "price": item['price'],
                    "categories": product['categories'],
                    "total": round(item['quantity'] * item['price'], 2)
                }
                order_products.append(order_product_data.copy())

    # Checking if the summary tables needs an update, or a write action
    # Verify if user exists in summary table
    customer_document = summary_collection.find({"customer_id": order['customer_id']}).limit(1)    
    if customer_document.count():
        # Update orders list for customer
        for customer in customer_document:
            print customer['_id']
            summary_collection.update({"customer_id": customer['customer_id']}, { "$push": { "orders": { "$each": order_products } }})
    else:
        # Create user and insert into summary
        data = {
            "customer_id": order['customer_id'],
            "orders": order_products
        }
        summary_id = summary_collection.insert_one(data).inserted_id


## Upsert method - Create if not exists, otherwise, update it