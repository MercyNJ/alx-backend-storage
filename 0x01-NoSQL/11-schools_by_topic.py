#!/usr/bin/env python3
"""A Python function that returns the list of school
having a specific topic.
"""

import pymongo


def schools_by_topic(mongo_collection, topic):
    """
    Returns a list of schools having a specific topic.

    Args:
        mongo_collection: PyMongo collection object.
        topic (string): The topic to search for.

    Returns:
        A list of schools that have the specified topic.
    """

    return mongo_collection.find({"topics": topic})
