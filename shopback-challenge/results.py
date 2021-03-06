# -*- coding: utf-8 -*-
from pymongo import MongoClient

from helper import *
from settings import *
from pprint import pprint

"""
    Getting the desired results
    - Perfil de gastos mensal.
    - Perfil de gastos por categoria mensal.
    - Média dos últimos 3 meses de gastos mensal.
    - Média dos últimos 3 meses por categoria mensal.
    - Informações de usuários.
"""

# Connection
client = MongoClient(DATABASE_NAME, DATABASE_PORT)
db = client.sb_db

summary_collection = db.summary

# Perfil de gastos mensal
monthly_rev = summary_collection.aggregate( [{"$unwind": "$orders"},
        {"$group": {"_id": {"order_date": "$orders.order_date", "customer_id": "$customer_id"}, "total": {"$sum": "$orders.total"}}},
        {"$sort": {"_id": -1}}
    ])

print "Perfil de gastos mensal"
for month_rev in monthly_rev:
    print(month_rev)
print "-----------"

# Média dos 3 últimos meses de gastos mensal
monthly_rev_avg = summary_collection.aggregate( [{"$unwind": "$orders"},
        {"$group": {"_id": {"order_date": "$orders.order_date", "customer_id": "$customer_id"}, "average": {"$avg": "$orders.total"}}},
        {"$sort": {"_id": -1}},
        {"$match": {"_id.order_date": {"$in": ['20175', '20174', '20173']}}}
    ])

print "Média dos 3 últimos meses de gastos mensal"
for month_rev_avg in monthly_rev_avg:
    print(month_rev_avg)
print "-----------"


# Perfil de gastos por categoria mensal
monthly_rev_per_category = summary_collection.aggregate([{"$unwind": "$orders"}, {"$unwind": "$orders.categories"},
        {"$group": {
            "_id":{"order_date": "$orders.order_date", "category": "$orders.categories", "customer_id": "$customer_id"}, 
            "total": {"$sum": "$orders.total"}
            }},
        {"$sort": {"_id.order_date": -1}}
    ])


print "Perfil de gastos por categoria mensal"
for month_rev_per_categ in monthly_rev_per_category:
    print(month_rev_per_categ)
print "-----------"

# Média dos 3 últimos meses por categoria mensal
monthly_rev_avg_per_category = summary_collection.aggregate([{"$unwind": "$orders"}, {"$unwind": "$orders.categories"},
        {"$group": {
            "_id":{"order_date": "$orders.order_date", "category": "$orders.categories", "customer_id": "$customer_id"}, 
            "average": {"$avg": "$orders.total"}
            }},
        {"$sort": {"_id.order_date": -1}},
        {"$match": {"_id.order_date": {"$in": ['20175', '20174', '20173']}}}
    ])

print "Média dos 3 últimos meses por categoria mensal"
for month_rev_avg_per_categ in monthly_rev_avg_per_category:
    print(month_rev_avg_per_categ)
