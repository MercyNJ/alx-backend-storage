#!/usr/bin/env python3
"""
Web Module - Implements functions for accessing and caching web pages.
"""

import requests
import redis
import time
from functools import wraps

redis_client = redis.Redis()


def count_calls(method):
    """Decorator to count how many times a method is called."""
    @wraps(method)
    def wrapper(url, *args, **kwargs):
        """Wrapper function for counting method calls."""
        count_key = "count:{}".format(url)
        count = redis_client.incr(count_key)
        result = method(url, *args, **kwargs)
        return result
    return wrapper


def cache_result(expiration=10):
    """Decorator to cache the result of a method with an expiration time."""
    def decorator(method):
        @wraps(method)
        def wrapper(url, *args, **kwargs):
            """Wrapper function for caching method results."""
            cache_key = "cache:{}".format(url)
            cached_data = redis_client.get(cache_key)
            if cached_data:
                return cached_data.decode("utf-8")
            else:
                result = method(url, *args, **kwargs)
                redis_client.setex(cache_key, expiration, result)
                return result
        return wrapper
    return decorator


@count_calls
@cache_result(expiration=10)
def get_page(url):
    """Get the HTML content of a URL."""
    response = requests.get(url)
    return response.text


slow_url = (
    "http://slowwly.robertomurray.co.uk/delay/1000/"
    "url/http://www.example.com"
)

start_time = time.time()
slow_response_1 = get_page(slow_url)
slow_response_2 = get_page(slow_url)
end_time = time.time()

print("Slow Response 1:", slow_response_1)
print("Slow Response 2:", slow_response_2)
print("Elapsed Time:", end_time - start_time)
