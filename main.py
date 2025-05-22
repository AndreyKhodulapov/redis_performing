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

client.rpush("tasks", "Task 1", "Task 2")
tasks = client.lrange("tasks", 0, -1)
print([task.decode() for task in tasks])

client.hset("user:1001", mapping={
    "name": "John",
    "age": 30,
    "email": "kek@example.com"
})

user = client.hgetall("user:1001")
print({k.decode(): v.decode() for k, v in user.items()})

client.zadd("leaderboard", {"player1": 100, "player2": 90})
leaders = client.zrange("leaderboard", 0, -1, withscores=True)
for player, score in leaders:
    print(player.decode(), score)