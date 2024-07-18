#!/usr/bin/env python3
"""
Web page retrieval and caching module.
"""

import requests
import redis
from functools import wraps
from typing import Callable

# Initialize Redis client
redis_client = redis.Redis()


def cache_page(expiration: int):
    """
    Decorator to cache the result of a function with an expiration time.

    Args:
        expiration (int): The expiration time for the cache in seconds.

    Returns:
        Callable: The wrapped function with caching functionality.
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(url: str) -> str:
            # Check if the result is cached
            cached_result = redis_client.get(f"cache:{url}")
            if cached_result:
                return cached_result.decode('utf-8')

            # Call the original function
            result = func(url)

            # Cache the result
            redis_client.setex(f"cache:{url}", expiration, result)
            return result
        return wrapper
    return decorator


def count_access(func: Callable) -> Callable:
    """
    Decorator to count how many times a URL is accessed.

    Args:
        func (Callable): The function to be decorated.

    Returns:
        Callable: The wrapped function with access counting functionality.
    """
    @wraps(func)
    def wrapper(url: str) -> str:
        # Increment the access count
        redis_client.incr(f"count:{url}")
        return func(url)
    return wrapper


@count_access
@cache_page(expiration=10)
def get_page(url: str) -> str:
    """
    Get the HTML content of a particular URL.

    Args:
        url (str): The URL to retrieve.

    Returns:
        str: The HTML content of the URL.
    """
    response = requests.get(url)
    return response.text
