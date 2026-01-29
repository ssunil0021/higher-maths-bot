from redis_client import r
from datetime import date

def add_user(user_id):
    r.sadd("users:all", user_id)
    r.sadd(f"users:daily:{date.today()}", user_id)

def total_users():
    return r.scard("users:all")

def today_users():
    return r.scard(f"users:daily:{date.today()}")
