from redis import Redis

r = Redis()

print(r.set('foo', 'bar'))
print(r.get('foo'))
