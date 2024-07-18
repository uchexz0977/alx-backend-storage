#!/usr/bin/env python3
"""
Cache class to store data in Redis with randomly generated keys.
"""

import redis
import uuid
from typing import Union, Callable, Optional
from functools import wraps

class Cache:
    def __init__(self):
        """
        Initialize the Cache class.
        Create a Redis client instance and flush the database.
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Store the data in Redis with a randomly generated key.
        
        Args:
            data (Union[str, bytes, int, float]): Data to store in Redis.

        Returns:
            str: The randomly generated key used to store the data.
        """
        # Generate a random key
        key = str(uuid.uuid4())
        # Store the data in Redis using the generated key
        self._redis.set(key, data)
        return key

# Example usage:
if __name__ == "__main__":
    cache = Cache()
    key = cache.store("Hello, World!")
    print(f"Data stored with key: {key}")

class Cache:
    def __init__(self):
        """
        Initialize the Cache class.
        Create a Redis client instance and flush the database.
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Store the data in Redis with a randomly generated key.
        
        Args:
            data (Union[str, bytes, int, float]): Data to store in Redis.

        Returns:
            str: The randomly generated key used to store the data.
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn: Optional[Callable] = None) -> Union[str, bytes, int, float, None]:
        """
        Retrieve the data from Redis and optionally apply a conversion function.
        
        Args:
            key (str): The key to retrieve from Redis.
            fn (Optional[Callable]): The function to apply to the data.

        Returns:
            Union[str, bytes, int, float, None]: The retrieved data, optionally converted using fn.
        """
        data = self._redis.get(key)
        if data is None:
            return None
        if fn:
            return fn(data)
        return data

    def get_str(self, key: str) -> Optional[str]:
        """
        Retrieve the data from Redis and convert it to a string.
        
        Args:
            key (str): The key to retrieve from Redis.

        Returns:
            Optional[str]: The retrieved data as a string.
        """
        return self.get(key, lambda d: d.decode('utf-8'))

    def get_int(self, key: str) -> Optional[int]:
        """
        Retrieve the data from Redis and convert it to an integer.
        
        Args:
            key (str): The key to retrieve from Redis.

        Returns:
            Optional[int]: The retrieved data as an integer.
        """
        return self.get(key, lambda d: int(d))


"""
Cache class to store data in Redis with randomly generated keys.
"""

def count_calls(method: Callable) -> Callable:
    """
    Decorator to count the number of times a method is called.
    
    Args:
        method (Callable): The method to be decorated.

    Returns:
        Callable: The wrapped method with counting functionality.
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        # Increment the count for the method's qualified name
        key = method.__qualname__
        self._redis.incr(key)
        # Call the original method
        return method(self, *args, **kwargs)
    return wrapper

class Cache:
    def __init__(self):
        """
        Initialize the Cache class.
        Create a Redis client instance and flush the database.
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Store the data in Redis with a randomly generated key.
        
        Args:
            data (Union[str, bytes, int, float]): Data to store in Redis.

        Returns:
            str: The randomly generated key used to store the data.
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn: Optional[Callable] = None) -> Union[str, bytes, int, float, None]:
        """
        Retrieve the data from Redis and optionally apply a conversion function.
        
        Args:
            key (str): The key to retrieve from Redis.
            fn (Optional[Callable]): The function to apply to the data.

        Returns:
            Union[str, bytes, int, float, None]: The retrieved data, optionally converted using fn.
        """
        data = self._redis.get(key)
        if data is None:
            return None
        if fn:
            return fn(data)
        return data

    def get_str(self, key: str) -> Optional[str]:
        """
        Retrieve the data from Redis and convert it to a string.
        
        Args:
            key (str): The key to retrieve from Redis.

        Returns:
            Optional[str]: The retrieved data as a string.
        """
        return self.get(key, lambda d: d.decode('utf-8'))

    def get_int(self, key: str) -> Optional[int]:
        """
        Retrieve the data from Redis and convert it to an integer.
        
        Args:
            key (str): The key to retrieve from Redis.

        Returns:
            Optional[int]: The retrieved data as an integer.
        """
        return self.get(key, lambda d: int(d))
"""
Cache class to store data in Redis with randomly generated keys.
"""
def count_calls(method: Callable) -> Callable:
    """
    Decorator to count the number of times a method is called.
    
    Args:
        method (Callable): The method to be decorated.

    Returns:
        Callable: The wrapped method with counting functionality.
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        key = method.__qualname__
        self._redis.incr(key)
        return method(self, *args, **kwargs)
    return wrapper

def call_history(method: Callable) -> Callable:
    """
    Decorator to store the history of inputs and outputs of a method.
    
    Args:
        method (Callable): The method to be decorated.

    Returns:
        Callable: The wrapped method with history functionality.
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        input_key = f"{method.__qualname__}:inputs"
        output_key = f"{method.__qualname__}:outputs"
        
        # Store input arguments in Redis
        self._redis.rpush(input_key, str(args))
        
        # Call the original method and store the result
        result = method(self, *args, **kwargs)
        
        # Store output result in Redis
        self._redis.rpush(output_key, str(result))
        
        return result
    return wrapper

class Cache:
    def __init__(self):
        """
        Initialize the Cache class.
        Create a Redis client instance and flush the database.
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    @call_history
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Store the data in Redis with a randomly generated key.
        
        Args:
            data (Union[str, bytes, int, float]): Data to store in Redis.

        Returns:
            str: The randomly generated key used to store the data.
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn: Optional[Callable] = None) -> Union[str, bytes, int, float, None]:
        """
        Retrieve the data from Redis and optionally apply a conversion function.
        
        Args:
            key (str): The key to retrieve from Redis.
            fn (Optional[Callable]): The function to apply to the data.

        Returns:
            Union[str, bytes, int, float, None]: The retrieved data, optionally converted using fn.
        """
        data = self._redis.get(key)
        if data is None:
            return None
        if fn:
            return fn(data)
        return data

    def get_str(self, key: str) -> Optional[str]:
        """
        Retrieve the data from Redis and convert it to a string.
        
        Args:
            key (str): The key to retrieve from Redis.

        Returns:
            Optional[str]: The retrieved data as a string.
        """
        return self.get(key, lambda d: d.decode('utf-8'))

    def get_int(self, key: str) -> Optional[int]:
        """
        Retrieve the data from Redis and convert it to an integer.
        
        Args:
            key (str): The key to retrieve from Redis.

        Returns:
            Optional[int]: The retrieved data as an integer.
        """
        return self.get(key, lambda d: int(d))


"""
Cache class to store data in Redis with randomly generated keys.
"""

def count_calls(method: Callable) -> Callable:
    """
    Decorator to count the number of times a method is called.
    
    Args:
        method (Callable): The method to be decorated.

    Returns:
        Callable: The wrapped method with counting functionality.
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        key = method.__qualname__
        self._redis.incr(key)
        return method(self, *args, **kwargs)
    return wrapper

def call_history(method: Callable) -> Callable:
    """
    Decorator to store the history of inputs and outputs for a function.
    
    Args:
        method (Callable): The method to be decorated.

    Returns:
        Callable: The wrapped method with history functionality.
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        input_key = method.__qualname__ + ":inputs"
        output_key = method.__qualname__ + ":outputs"
        
        # Store inputs
        self._redis.rpush(input_key, str(args))
        
        # Execute the original method and store output
        output = method(self, *args, **kwargs)
        self._redis.rpush(output_key, str(output))
        
        return output
    return wrapper

class Cache:
    def __init__(self):
        """
        Initialize the Cache class.
        Create a Redis client instance and flush the database.
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    @call_history
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Store the data in Redis with a randomly generated key.
        
        Args:
            data (Union[str, bytes, int, float]): Data to store in Redis.

        Returns:
            str: The randomly generated key used to store the data.
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn: Optional[Callable] = None) -> Union[str, bytes, int, float, None]:
        """
        Retrieve the data from Redis and optionally apply a conversion function.
        
        Args:
            key (str): The key to retrieve from Redis.
            fn (Optional[Callable]): The function to apply to the data.

        Returns:
            Union[str, bytes, int, float, None]: The retrieved data, optionally converted using fn.
        """
        data = self._redis.get(key)
        if data is None:
            return None
        if fn:
            return fn(data)
        return data

    def get_str(self, key: str) -> Optional[str]:
        """
        Retrieve the data from Redis and convert it to a string.
        
        Args:
            key (str): The key to retrieve from Redis.

        Returns:
            Optional[str]: The retrieved data as a string.
        """
        return self.get(key, lambda d: d.decode('utf-8'))

    def get_int(self, key: str) -> Optional[int]:
        """
        Retrieve the data from Redis and convert it to an integer.
        
        Args:
            key (str): The key to retrieve from Redis.

        Returns:
            Optional[int]: The retrieved data as an integer.
        """
        return self.get(key, lambda d: int(d))

def replay(method: Callable) -> None:
    """
    Display the history of calls of a particular function.
    
    Args:
        method (Callable): The function to replay the history for.
    """
    input_key = method.__qualname__ + ":inputs"
    output_key = method.__qualname__ + ":outputs"
    
    redis_instance = method.__self__._redis
    
    inputs = redis_instance.lrange(input_key, 0, -1)
    outputs = redis_instance.lrange(output_key, 0, -1)
    
    print(f"{method.__qualname__} was called {len(inputs)} times:")
    for input_, output in zip(inputs, outputs):
        print(f"{method.__qualname__}(*{input_.decode('utf-8')}) -> {output.decode('utf-8')}")

# Example usage and test cases:
if __name__ == "__main__":
    cache = Cache()

    s1 = cache.store("first")
    print(s1)
    s2 = cache.store("second")
    print(s2)
    s3 = cache.store("third")
    print(s3)

    inputs = cache._redis.lrange("{}:inputs".format(cache.store.__qualname__), 0, -1)
    outputs = cache._redis.lrange("{}:outputs".format(cache.store.__qualname__), 0, -1)

    print("inputs: {}".format(inputs))
    print("outputs: {}".format(outputs))

    replay(cache.store)
