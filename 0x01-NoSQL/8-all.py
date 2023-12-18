#!/usr/bin/env python3
"""
Lists all documents in the given MongoDB collection.
"""


import pymongo


def list_all(mongo_collection):
    """
    Returns list of all documents in a collection.
    """

    if mongo_collection.count_documents({}) == 0:
        return []

    documents = list(mongo_collection.find())
    return documents
