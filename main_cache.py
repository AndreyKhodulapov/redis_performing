import redis
import time

client = redis.Redis(
    host="localhost",
    port=6379,
    db=0
)

def fake_api_query(user_id: int):
    time.sleep(2)
    return f"User Profile({user_id=})"


def get_user_profile(user_id: int):
    key = f"user:{user_id}:profile"

    profile = client.get(key)
    if profile:
        print(f"Cache hit {client.ttl(key)=}")
        return profile.decode()

    profile = fake_api_query(user_id)
    client.setex(key, 60, profile)

    return profile

print(get_user_profile(1))
print(get_user_profile(1))