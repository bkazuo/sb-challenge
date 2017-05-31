from pymongo import MongoClient
import sys
# import datetime

sys.path.insert(0, '../')
from helper import *
from settings import *

"""
Create random users
"""

# Connection
client = MongoClient(DATABASE_NAME, DATABASE_PORT)
db = client.sb_db
customer_collection = db.customers

for index in range(NUMBER_OF_CUSTOMERS): 
    data = {
        "customer_id": createHash(),
        "email": createRandomEmail(),
        "details": {
            "first_name": createRandomString(), 
            "last_name": createRandomString(),
            "telephone": createRandomNumber(),
            "identification": [{   
                "type": "cpf",
                "typeName": "CPF",
                "number": ""
            }]
        },
        "address": [{
            "city": "",
            "state": "",
            "zip_code": "",
            "is_primary": True,
        }],
        "updated_at": datetime.utcnow(),
        "created_at": datetime.utcnow()
    }
    customer_id = customer_collection.insert_one(data).inserted_id
    print customer_id
