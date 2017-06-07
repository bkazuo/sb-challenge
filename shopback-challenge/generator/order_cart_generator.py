from pymongo import MongoClient
import time
import sys
sys.path.insert(0, '../')

from helper import *
from settings import *

"""
Create random orders based on users and products
"""

# Connection
client = MongoClient(DATABASE_NAME, DATABASE_PORT)
db = client.sb_db
customer_collection = db.customers
products_collection = db.products
carts_collection = db.carts
orders_collection = db.orders

total_customers = customer_collection.count()
total_products = products_collection.count()

start_time = time.time()
for count in range(NUMBER_OF_ORDERS):
    random_customer = customer_collection.find().limit(-1).skip(createRandomIntBetween(total_customers-1)).next()

    products = []
    total_amount = 0
    for cart_items in range(createPositiveInt(MAX_ITEMS_CART_QTY)):
        random_product = products_collection.find().limit(-1).skip(createRandomIntBetween(total_products-1)).next()
        if checkIfRepresentsFloat(random_product['price']):
            product = {
                "product_id": random_product['product_id'],
                "price": round(float(random_product['price']), 2),
                "quantity": createPositiveInt(MAX_QTY)
            }
            products.append(product.copy())
            total_amount = round(total_amount + (product['price'] * product['quantity']), 2)
            pass

    random_data = randomDate(INITAL_DATE, FINAL_DATE)

    # Cart pattern colletion
    cart_data = {
        "client_id": random_product['client_id'],
        "customer_id": random_customer['customer_id'],
        "products": products,
        "amount": total_amount,
        "anonymous" : False,
        "complete" : False,
        "recovered" : False,
        "updated_at": random_data,
        "created_at": random_data
    }    

    cart_id = carts_collection.insert_one(cart_data).inserted_id
    
    # Order pattern collection
    order_data = {
        "client_id": random_product['client_id'],
        "customer_id": random_customer['customer_id'],
        "cart_id": str(cart_id),
        "details": {
            "price": total_amount
        },
        "anonymous": False,
        "updated_at": random_data,
        "created_at": random_data
    }
    order_id = orders_collection.insert_one(order_data).inserted_id
    
    print str(cart_id) + "--" + str(order_id)

elapsed_time = time.time() - start_time

print "Time to execute:" + str(elapsed_time)