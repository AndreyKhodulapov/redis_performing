import redis

client = redis.Redis(
    host="localhost",
    port=6379,
    db=0
)

try:
    response = client.ping()
    print(f"Connection to Redis: {response}")
except redis.ConnectionError as e:
    print(f"Connection failed: {e}")

# client.set("name", "Alice")
# name = client.get("name")
# print(name.decode())

# if client.exists("name"):
#     print("Key exists")

# client.setex("session", 3600, "active")
ttl = client.ttl("session")
print(f"Left {ttl} sec")