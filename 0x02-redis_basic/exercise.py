#!/usr/bin/env python3
"""
This module provides a Cache class for interacting with a Redis database.
"""

import uuid
import redis
from typing import Union


class Cache:
    """
    Cache class for interacting with a Redis database.
    """

    def __init__(self):
        """ Initializes the cache."""
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Store data in Redis with a randomly generated key.
        """
        random_key = str(uuid.uuid4())
        self._redis.set(random_key, data)
        return random_key
