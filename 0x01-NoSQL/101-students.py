#!/usr/bin/env python3
"""
MongoDB Operations with Python using pymongo.
"""

from pymongo import MongoClient


def top_students(mongo_collection):
    """
    Returns all students sorted by average score.
    """

    return mongo_collection.aggregate([
        {
            "$project": {
                "name": "$name",
                "averageScore": {"$avg": {"$ifNull": ["$topics.score", 0]}}
            }
        },
        {"$sort": {"averageScore": -1}}
    ])
