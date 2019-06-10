import uuid

from redis import Redis

"""
用于将用户id存到redis里面
"""
user_size = 50
r = Redis(host='127.0.0.1', decode_responses=True)
r.delete('getuser')
j = 0
while j < user_size + 1:
    si = str("".join(str(uuid.uuid4()).split("-")).lower())
    print("uindex", si)
    r.lpush('getuser', si)
    j += 1
print("done")
print("测试获取一个userid",si)
