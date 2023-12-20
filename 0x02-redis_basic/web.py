#!/usr/bin/env python3
"""
Web Module - Implements functions for accessing and caching web pages.
"""

import redis
import time
import requests
from functools import wraps

redis_client = redis.Redis()


def cached_url(method):
    """Decorator for the get_page function."""
    @wraps(method)
    def wrapper(url):
        """Wrapper function."""
        cache_key = "cached:" + url
        cached_data = redis_client.get(cache_key)

        if cached_data:
            return cached_data.decode("utf-8")

        count_key = "count:" + url
        html_content = method(url)

        redis_client.incr(count_key)
        redis_client.setex(cache_key, 10, html_content)

        return html_content

    return wrapper


@cached_url
def get_page(url: str) -> str:
    """Obtain the HTML content of a particular URL."""
    response = requests.get(url)
    return response.text


if __name__ == "__main__":
    get_page('http://slowwly.robertomurray.co.uk')

    slow_url = "http://slowwly.robertomurray.co.uk"
    start_time = time.time()
    slow_content = get_page(slow_url)
    end_time = time.time()

    print(f"Content from slow URL:\n{slow_content}")
    print(f"Time taken: {end_time - start_time} seconds\n")

    start_time_cached = time.time()
    cached_slow_content = get_page(slow_url)
    end_time_cached = time.time()

    print(f"Cached content from slow URL:\n{cached_slow_content}")
    print(f"Ttaken(cached): {end_time_cached - start_time_cached} seconds\n")

    access_count = redis_client.get(f"count:{slow_url}")
    print(f"Access count for slow URL: {access_count.decode('utf-8')}")
