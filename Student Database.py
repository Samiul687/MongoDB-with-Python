import pymongo
import subprocess
import pprint
from pymongo import MongoClient

cluster = MongoClient(
    "mongodb://admin:admin@cluster0-shard-00-00-whyp1.mongodb.net:27017,cluster0-shard-00-01-whyp1.mongodb.net:27017,"
    "cluster0-shard-00-02-whyp1.mongodb.net:27017/test?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin"
    "&retryWrites=true&w=majority")
db = cluster["datasets"]
collection = db["student_data"]


def find():
    key = input("Key to search: ").lower()
    value = input("Value to search: ").lower()
    filterlist = {key: value}

    results = collection.find(filterlist)

    for result in results:
        pprint.pprint(result)


def add():
    keys = sorted(db.student_data.find_one())
    values = []

    for k in keys:
        value = input(k + "?: ")
        values.append(value)

    joint = dict(zip(keys, values))
    pprint.pprint(joint)

    check = input("Please check and type OK to continue or NO to restart: ").lower()

    if check == "ok":
        collection.insert_one(joint)
        print("Added successfully")
    elif check == "no":
        add()
    else:
        print("Please try again")
        add()


def delete():
    print("Please note ID if you'd like to delete one or key to delete many")
    find()
    choice = input("would you like to delete one or many?: ")

    if choice == "one":
        delval = input("Please enter the ID of the document to delete: ").lower()
        query = {"_id": delval}
        collection.delete_one(query)
        print("Deleted succesfully")

    elif choice == "many":
        delkey = input("Key to delete?: ")
        delval = input("Value to delete?: ")
        query = {delkey: delval}
        collection.delete_many(query)
        print("Deleted succesfully")

    else:
        print("Please try again")
        delete()


def start():
    choice = input("What would you like to do?: ").lower()
    if choice == "add":
        add()
    elif choice == "find":
        find()
    elif choice == "delete":
        delete()
    else:
        print("Please try again")
        start()


start()
