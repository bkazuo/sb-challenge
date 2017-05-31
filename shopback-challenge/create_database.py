#!/usr/bin/python

import subprocess

print "Creating customers..."
subprocess.call(["python", "customer_generator.py"], cwd="generator")
print "Creating products.."
subprocess.call(["python", "product_generator.py"], cwd="generator")
print "Creating orders and carts..."
subprocess.call(["python", "order_cart_generator.py"], cwd="generator")