#!/usr/bin/env python3
"""A Python script that provides some stats about Nginx
logs stored in MongoDB.
"""

from pymongo import MongoClient


def log_stats(mongo_collection):
    """
    Provides some stats about Nginx logs stored in MongoDB.

    Args:
        mongo_collection: PyMongo collection object.

    Returns:
        A dictionary containing the required statistics.
    """

    total_logs = mongo_collection.count_documents({})

    http_methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    method_stats = {method: mongo_collection.count_documents(
        {"method": method}) for method in http_methods}

    status_check_logs = mongo_collection.count_documents(
            {"method": "GET", "path": "/status"})

    return {
        "total_logs": total_logs,
        "method_stats": method_stats,
        "status_check_logs": status_check_logs
    }


if __name__ == "__main__":
    client = MongoClient('mongodb://127.0.0.1:27017')
    db = client.logs
    nginx_collection = db.nginx

    stats = log_stats(nginx_collection)

    print("{} logs".format(stats["total_logs"]))
    print("Methods:")
    for method, count in stats["method_stats"].items():
        print("\tmethod {}: {}".format(method, count))
    print("{} status check".format(stats["status_check_logs"]))
