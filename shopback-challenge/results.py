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
        {"$group": {"_id": "$orders.order_date", "total": {"$sum": "$orders.total"}}},
        {"$sort": {"_id": -1}}
    ])

for month_rev in monthly_rev:
    pprint(month_rev)
print "-----------"

# Média dos 3 últimos meses de gastos mensal
monthly_rev_avg = summary_collection.aggregate( [{"$unwind": "$orders"},
        {"$group": {"_id": "$orders.order_date", "total": {"$avg": "$orders.total"}}},
        {"$sort": {"_id": -1}},
        {"$limit": 3}
    ])

for month_rev_avg in monthly_rev_avg:
    pprint(month_rev_avg)

