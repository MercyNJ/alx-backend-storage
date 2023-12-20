#!/usr/bin/env python3
"""
This module provides a Cache class for interacting with a Redis database.
"""

import uuid
import redis
from typing import Union, Optional, Callable
from functools import wraps


def count_calls(method: Callable) -> Callable:
    """
    Decorator to count how many times a method is called.
    """

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        key = method.__qualname__
        count = self._redis.incr(key)
        result = method(self, *args, **kwargs)
        return result
    return wrapper


def call_history(method: Callable) -> Callable:
    """
    Decorator to store the history of inputs and outputs for a function in Redis.
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        input_key = "{}:inputs".format(method.__qualname__)
        output_key = "{}:outputs".format(method.__qualname__)
        self._redis.rpush(input_key, str(args))
        result = method(self, *args, **kwargs)
        self._redis.rpush(output_key, str(result))
        return result
    return wrapper

def replay(fn: Callable):
    """
    Display the history of calls for a particular function.
    """

    redis_client = redis.Redis()
    target_name = fn.__qualname__
    value = redis_client.get(target_name)

    try:
        value = int(value.decode("utf-8"))
    except Exception:
        value = 0

    print("{} was called {} times:".format(target_name, value))

    inputs = redis_client.lrange("{}:inputs".format(target_name), 0, -1)
    outputs = redis_client.lrange("{}:outputs".format(target_name), 0, -1)

    for input, output in zip(inputs, outputs):
        try:
            input = input.decode("utf-8")
        except Exception:
            input = ""

        try:
            output = output.decode("utf-8")
        except Exception:
            output = ""

        print("{}(*{}) -> {}".format(target_name, input, output))



class Cache:
    """
    Cache class for interacting with a Redis database.
    """

    def __init__(self):
        """ Initializes the cache."""
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    @call_history
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Store data in Redis with a randomly generated key.
        """
        random_key = str(uuid.uuid4())
        self._redis.set(random_key, data)
        return random_key

    def get(self, key: str, fn: Optional[Callable] = None) -> Union[str, bytes, int, float, None]:
        """
        Retrieve data from Redis based on the key and apply the conversion function if provided.
        """
        data = self._redis.get(key)
        if data is None:
            return None

        if fn is not None:
            return fn(data)

        return data

    def get_str(self, key: str) -> Union[str, None]:
        """
        Retrieve data from Redis as a string.
        """
        return self.get(key, fn=lambda d: d.decode('utf-8'))

    def get_int(self, key: str) -> Union[int, None]:
        """
        Retrieve data from Redis as an integer.
        """
        return self.get(key, fn=int)


cache = Cache()
cache.store("foo")
cache.store("bar")
cache.store(42)
replay(cache.store)
