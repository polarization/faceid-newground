# coding=utf-8
import redis
from config import redis_IP, redis_port


pool = redis.ConnectionPool(host=redis_IP, port=redis_port, db=0)
redis_cli = redis.Redis(connection_pool=pool)


def get_value(key):

    """
    :param key:
    :return: Return the value at key name, or None if the key doesn’t exist
    """
    return redis_cli.get(key)


def set_keyvalue(key, value, expire_time=None):
    if expire_time is None:
        return redis_cli.set(key, value)
    else:
        return redis_cli.setex(key, value, expire_time)


def delete_keys(*keys):
    return redis_cli.delete(*keys)
