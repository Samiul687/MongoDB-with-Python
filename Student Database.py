import pymongo
import subprocess
import pprint
import os
from pymongo import MongoClient
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

choice = None

cluster = MongoClient(
    "mongodb://admin:admin@cluster0-shard-00-00-whyp1.mongodb.net:27017,cluster0-shard-00-01-whyp1.mongodb.net:27017,"
    "cluster0-shard-00-02-whyp1.mongodb.net:27017/test?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin"
    "&retryWrites=true&w=majority")
db = cluster["datasets"]
collection = db["student_data"]


def checkkeys():
    try:
        sorted(db.student_data.find_one())
    except TypeError:
        print("No keys found")
        exit()


checkkeys()
keys = sorted(db.student_data.find_one())


def edit():
    toedit = input("ID of document to edit: ")
    results = collection.find({"_id": toedit})
    for result in results:
        pprint.pprint(result)

    edkey = input("\nKey of value to edit: ")
    edval = input("Value to change to: ")
    collection.find_one_and_update(
        {"_id": toedit},
        {"$set":
             {edkey: edval}
         }, upsert=True
    )

    results = collection.find({"_id": toedit})
    for result in results:
        pprint.pprint(result)

    print("\nThe change was successful")


def find():
    key = input("\nKey to search: ").lower()
    if key in keys:
        value = input("Value to search: ").lower()
        filterlist = {key: value}

        results = collection.find(filterlist)
        print(results)

        if results == " ":
            print("None found, please try again")
            find()
        else:
            for result in results:
                pprint.pprint(result)
                print("\n")

    else:
        print("Please try again")
        find()


def add():
    print("\nFill in the values or type \"reset\" at any time to reset")
    values = []
    length = len(keys)
    k = 0

    while k < length:
        value = input(keys[k].capitalize() + "?: ").lower()
        if value != "back":
            values.append(value)
            k += 1
        else:
            k -= 1
            values = values[:-1]

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
    print("\nIf deleting ONE, note ID. If deleting MANY, note key and value.")
    find()
    delchoice = input("\nWould you like to delete one, many or all?: ")

    if delchoice == "one":
        delval = input("Please enter the ID of the document to delete: ").lower()
        query = {"_id": delval}
        collection.delete_one(query)
        print("One deleted succesfully")

    elif delchoice == "many":
        delkey = input("Key to delete?: ")
        delval = input("Value to delete?: ")
        query = {delkey: delval}
        collection.delete_many(query)
        print("Many deleted successfully")

    elif delchoice == "all":
        collection.delete_many({})
        print("All deleted successfully")

    else:
        print("Please try again")
        delete()


def start():
    starchoice = input("\nWhat would you like to do?: ").lower()
    if starchoice == "add":
        add()
    elif starchoice == "find":
        find()
    elif starchoice == "delete":
        delete()
    elif starchoice == "edit":
        edit()
    else:
        print("Please try again")
        start()


while choice != "exit":
    start()
