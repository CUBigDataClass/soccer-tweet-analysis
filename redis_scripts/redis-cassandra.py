import redis

def connect_to_host(ip, port=6379):
    r = redis.StrictRedis(host=ip, port=port, db=0)
    r.set('foo', 'bar')

connect_to_host('172.31.10.39')
