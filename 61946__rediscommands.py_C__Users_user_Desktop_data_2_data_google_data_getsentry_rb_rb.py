# flake8: noqa

COMMANDS = {'APPEND': {'arity': 3L,
            'flags': ['write', 'denyoom'],
            'key_spec': (1, 1, 1)},
 'AUTH': {'arity': 2L,
          'flags': ['readonly', 'noscript', 'loading', 'stale', 'fast'],
          'key_spec': (0, 0, 0)},
 'BGREWRITEAOF': {'arity': 1L,
                  'flags': ['readonly', 'admin'],
                  'key_spec': (0, 0, 0)},
 'BGSAVE': {'arity': 1L,
            'flags': ['readonly', 'admin'],
            'key_spec': (0, 0, 0)},
 'BITCOUNT': {'arity': -2L,
              'flags': ['readonly'],
              'key_spec': (1, 1, 1)},
 'BITOP': {'arity': -4L,
           'flags': ['write', 'denyoom'],
           'key_spec': (2, -1, 1)},
 'BITPOS': {'arity': -3L, 'flags': ['readonly'], 'key_spec': (1, 1, 1)},
 'BLPOP': {'arity': -3L,
           'flags': ['write', 'noscript'],
           'key_spec': (1, -2, 1)},
 'BRPOP': {'arity': -3L,
           'flags': ['write', 'noscript'],
           'key_spec': (1, 1, 1)},
 'BRPOPLPUSH': {'arity': 4L,
                'flags': ['write', 'denyoom', 'noscript'],
                'key_spec': (1, 2, 1)},
 'CLIENT': {'arity': -2L,
            'flags': ['readonly', 'admin'],
            'key_spec': (0, 0, 0)},
 'COMMAND': {'arity': 0L,
             'flags': ['readonly', 'loading', 'stale'],
             'key_spec': (0, 0, 0)},
 'CONFIG': {'arity': -2L,
            'flags': ['readonly', 'admin', 'stale'],
            'key_spec': (0, 0, 0)},
 'DBSIZE': {'arity': 1L,
            'flags': ['readonly', 'fast'],
            'key_spec': (0, 0, 0)},
 'DEBUG': {'arity': -2L,
           'flags': ['admin', 'noscript'],
           'key_spec': (0, 0, 0)},
 'DECR': {'arity': 2L,
          'flags': ['write', 'denyoom', 'fast'],
          'key_spec': (1, 1, 1)},
 'DECRBY': {'arity': 3L,
            'flags': ['write', 'denyoom', 'fast'],
            'key_spec': (1, 1, 1)},
 'DEL': {'arity': -2L, 'flags': ['write'], 'key_spec': (1, -1, 1)},
 'DISCARD': {'arity': 1L,
             'flags': ['readonly', 'noscript', 'fast'],
             'key_spec': (0, 0, 0)},
 'DUMP': {'arity': 2L,
          'flags': ['readonly', 'admin'],
          'key_spec': (1, 1, 1)},
 'ECHO': {'arity': 2L,
          'flags': ['readonly', 'fast'],
          'key_spec': (0, 0, 0)},
 'EVAL': {'arity': -3L,
          'flags': ['noscript', 'movablekeys'],
          'key_spec': (0, 0, 0)},
 'EVALSHA': {'arity': -3L,
             'flags': ['noscript', 'movablekeys'],
             'key_spec': (0, 0, 0)},
 'EXEC': {'arity': 1L,
          'flags': ['noscript', 'skip_monitor'],
          'key_spec': (0, 0, 0)},
 'EXISTS': {'arity': 2L,
            'flags': ['readonly', 'fast'],
            'key_spec': (1, 1, 1)},
 'EXPIRE': {'arity': 3L,
            'flags': ['write', 'fast'],
            'key_spec': (1, 1, 1)},
 'EXPIREAT': {'arity': 3L,
              'flags': ['write', 'fast'],
              'key_spec': (1, 1, 1)},
 'FLUSHALL': {'arity': 1L, 'flags': ['write'], 'key_spec': (0, 0, 0)},
 'FLUSHDB': {'arity': 1L, 'flags': ['write'], 'key_spec': (0, 0, 0)},
 'GET': {'arity': 2L,
         'flags': ['readonly', 'fast'],
         'key_spec': (1, 1, 1)},
 'GETBIT': {'arity': 3L,
            'flags': ['readonly', 'fast'],
            'key_spec': (1, 1, 1)},
 'GETRANGE': {'arity': 4L, 'flags': ['readonly'], 'key_spec': (1, 1, 1)},
 'GETSET': {'arity': 3L,
            'flags': ['write', 'denyoom'],
            'key_spec': (1, 1, 1)},
 'HDEL': {'arity': -3L,
          'flags': ['write', 'fast'],
          'key_spec': (1, 1, 1)},
 'HEXISTS': {'arity': 3L,
             'flags': ['readonly', 'fast'],
             'key_spec': (1, 1, 1)},
 'HGET': {'arity': 3L,
          'flags': ['readonly', 'fast'],
          'key_spec': (1, 1, 1)},
 'HGETALL': {'arity': 2L, 'flags': ['readonly'], 'key_spec': (1, 1, 1)},
 'HINCRBY': {'arity': 4L,
             'flags': ['write', 'denyoom', 'fast'],
             'key_spec': (1, 1, 1)},
 'HINCRBYFLOAT': {'arity': 4L,
                  'flags': ['write', 'denyoom', 'fast'],
                  'key_spec': (1, 1, 1)},
 'HKEYS': {'arity': 2L,
           'flags': ['readonly', 'sort_for_script'],
           'key_spec': (1, 1, 1)},
 'HLEN': {'arity': 2L,
          'flags': ['readonly', 'fast'],
          'key_spec': (1, 1, 1)},
 'HMGET': {'arity': -3L, 'flags': ['readonly'], 'key_spec': (1, 1, 1)},
 'HMSET': {'arity': -4L,
           'flags': ['write', 'denyoom'],
           'key_spec': (1, 1, 1)},
 'HSCAN': {'arity': -3L,
           'flags': ['readonly', 'random'],
           'key_spec': (1, 1, 1)},
 'HSET': {'arity': 4L,
          'flags': ['write', 'denyoom', 'fast'],
          'key_spec': (1, 1, 1)},
 'HSETNX': {'arity': 4L,
            'flags': ['write', 'denyoom', 'fast'],
            'key_spec': (1, 1, 1)},
 'HVALS': {'arity': 2L,
           'flags': ['readonly', 'sort_for_script'],
           'key_spec': (1, 1, 1)},
 'INCR': {'arity': 2L,
          'flags': ['write', 'denyoom', 'fast'],
          'key_spec': (1, 1, 1)},
 'INCRBY': {'arity': 3L,
            'flags': ['write', 'denyoom', 'fast'],
            'key_spec': (1, 1, 1)},
 'INCRBYFLOAT': {'arity': 3L,
                 'flags': ['write', 'denyoom', 'fast'],
                 'key_spec': (1, 1, 1)},
 'INFO': {'arity': -1L,
          'flags': ['readonly', 'loading', 'stale'],
          'key_spec': (0, 0, 0)},
 'KEYS': {'arity': 2L,
          'flags': ['readonly', 'sort_for_script'],
          'key_spec': (0, 0, 0)},
 'LASTSAVE': {'arity': 1L,
              'flags': ['readonly', 'random', 'fast'],
              'key_spec': (0, 0, 0)},
 'LATENCY': {'arity': -2L,
             'flags': ['readonly',
                       'admin',
                       'noscript',
                       'loading',
                       'stale'],
             'key_spec': (0, 0, 0)},
 'LINDEX': {'arity': 3L, 'flags': ['readonly'], 'key_spec': (1, 1, 1)},
 'LINSERT': {'arity': 5L,
             'flags': ['write', 'denyoom'],
             'key_spec': (1, 1, 1)},
 'LLEN': {'arity': 2L,
          'flags': ['readonly', 'fast'],
          'key_spec': (1, 1, 1)},
 'LPOP': {'arity': 2L,
          'flags': ['write', 'fast'],
          'key_spec': (1, 1, 1)},
 'LPUSH': {'arity': -3L,
           'flags': ['write', 'denyoom', 'fast'],
           'key_spec': (1, 1, 1)},
 'LPUSHX': {'arity': 3L,
            'flags': ['write', 'denyoom', 'fast'],
            'key_spec': (1, 1, 1)},
 'LRANGE': {'arity': 4L, 'flags': ['readonly'], 'key_spec': (1, 1, 1)},
 'LREM': {'arity': 4L, 'flags': ['write'], 'key_spec': (1, 1, 1)},
 'LSET': {'arity': 4L,
          'flags': ['write', 'denyoom'],
          'key_spec': (1, 1, 1)},
 'LTRIM': {'arity': 4L, 'flags': ['write'], 'key_spec': (1, 1, 1)},
 'MGET': {'arity': -2L, 'flags': ['readonly'], 'key_spec': (1, -1, 1)},
 'MIGRATE': {'arity': 6L,
             'flags': ['write', 'admin'],
             'key_spec': (0, 0, 0)},
 'MONITOR': {'arity': 1L,
             'flags': ['readonly', 'admin', 'noscript'],
             'key_spec': (0, 0, 0)},
 'MOVE': {'arity': 3L,
          'flags': ['write', 'fast'],
          'key_spec': (1, 1, 1)},
 'MSET': {'arity': -3L,
          'flags': ['write', 'denyoom'],
          'key_spec': (1, -1, 2)},
 'MSETNX': {'arity': -3L,
            'flags': ['write', 'denyoom'],
            'key_spec': (1, -1, 2)},
 'MULTI': {'arity': 1L,
           'flags': ['readonly', 'noscript', 'fast'],
           'key_spec': (0, 0, 0)},
 'OBJECT': {'arity': 3L, 'flags': ['readonly'], 'key_spec': (2, 2, 2)},
 'PERSIST': {'arity': 2L,
             'flags': ['write', 'fast'],
             'key_spec': (1, 1, 1)},
 'PEXPIRE': {'arity': 3L,
             'flags': ['write', 'fast'],
             'key_spec': (1, 1, 1)},
 'PEXPIREAT': {'arity': 3L,
               'flags': ['write', 'fast'],
               'key_spec': (1, 1, 1)},
 'PFADD': {'arity': -2L,
           'flags': ['write', 'denyoom', 'fast'],
           'key_spec': (1, 1, 1)},
 'PFCOUNT': {'arity': -2L, 'flags': ['write'], 'key_spec': (1, 1, 1)},
 'PFDEBUG': {'arity': -3L, 'flags': ['write'], 'key_spec': (0, 0, 0)},
 'PFMERGE': {'arity': -2L,
             'flags': ['write', 'denyoom'],
             'key_spec': (1, -1, 1)},
 'PFSELFTEST': {'arity': 1L,
                'flags': ['readonly'],
                'key_spec': (0, 0, 0)},
 'PING': {'arity': 1L,
          'flags': ['readonly', 'stale', 'fast'],
          'key_spec': (0, 0, 0)},
 'PSETEX': {'arity': 4L,
            'flags': ['write', 'denyoom'],
            'key_spec': (1, 1, 1)},
 'PSUBSCRIBE': {'arity': -2L,
                'flags': ['readonly',
                          'pubsub',
                          'noscript',
                          'loading',
                          'stale'],
                'key_spec': (0, 0, 0)},
 'PSYNC': {'arity': 3L,
           'flags': ['readonly', 'admin', 'noscript'],
           'key_spec': (0, 0, 0)},
 'PTTL': {'arity': 2L,
          'flags': ['readonly', 'fast'],
          'key_spec': (1, 1, 1)},
 'PUBLISH': {'arity': 3L,
             'flags': ['readonly',
                       'pubsub',
                       'loading',
                       'stale',
                       'fast'],
             'key_spec': (0, 0, 0)},
 'PUBSUB': {'arity': -2L,
            'flags': ['readonly',
                      'pubsub',
                      'random',
                      'loading',
                      'stale'],
            'key_spec': (0, 0, 0)},
 'PUNSUBSCRIBE': {'arity': -1L,
                  'flags': ['readonly',
                            'pubsub',
                            'noscript',
                            'loading',
                            'stale'],
                  'key_spec': (0, 0, 0)},
 'RANDOMKEY': {'arity': 1L,
               'flags': ['readonly', 'random'],
               'key_spec': (0, 0, 0)},
 'RENAME': {'arity': 3L, 'flags': ['write'], 'key_spec': (1, 2, 1)},
 'RENAMENX': {'arity': 3L,
              'flags': ['write', 'fast'],
              'key_spec': (1, 2, 1)},
 'REPLCONF': {'arity': -1L,
              'flags': ['readonly',
                        'admin',
                        'noscript',
                        'loading',
                        'stale'],
              'key_spec': (0, 0, 0)},
 'RESTORE': {'arity': 4L,
             'flags': ['write', 'denyoom', 'admin'],
             'key_spec': (1, 1, 1)},
 'ROLE': {'arity': 1L,
          'flags': ['admin', 'noscript', 'loading', 'stale'],
          'key_spec': (0, 0, 0)},
 'RPOP': {'arity': 2L,
          'flags': ['write', 'fast'],
          'key_spec': (1, 1, 1)},
 'RPOPLPUSH': {'arity': 3L,
               'flags': ['write', 'denyoom'],
               'key_spec': (1, 2, 1)},
 'RPUSH': {'arity': -3L,
           'flags': ['write', 'denyoom', 'fast'],
           'key_spec': (1, 1, 1)},
 'RPUSHX': {'arity': 3L,
            'flags': ['write', 'denyoom', 'fast'],
            'key_spec': (1, 1, 1)},
 'SADD': {'arity': -3L,
          'flags': ['write', 'denyoom', 'fast'],
          'key_spec': (1, 1, 1)},
 'SAVE': {'arity': 1L,
          'flags': ['readonly', 'admin', 'noscript'],
          'key_spec': (0, 0, 0)},
 'SCAN': {'arity': -2L,
          'flags': ['readonly', 'random'],
          'key_spec': (0, 0, 0)},
 'SCARD': {'arity': 2L,
           'flags': ['readonly', 'fast'],
           'key_spec': (1, 1, 1)},
 'SCRIPT': {'arity': -2L,
            'flags': ['readonly', 'admin', 'noscript'],
            'key_spec': (0, 0, 0)},
 'SDIFF': {'arity': -2L,
           'flags': ['readonly', 'sort_for_script'],
           'key_spec': (1, -1, 1)},
 'SDIFFSTORE': {'arity': -3L,
                'flags': ['write', 'denyoom'],
                'key_spec': (1, -1, 1)},
 'SELECT': {'arity': 2L,
            'flags': ['readonly', 'loading', 'fast'],
            'key_spec': (0, 0, 0)},
 'SET': {'arity': -3L,
         'flags': ['write', 'denyoom'],
         'key_spec': (1, 1, 1)},
 'SETBIT': {'arity': 4L,
            'flags': ['write', 'denyoom'],
            'key_spec': (1, 1, 1)},
 'SETEX': {'arity': 4L,
           'flags': ['write', 'denyoom'],
           'key_spec': (1, 1, 1)},
 'SETNX': {'arity': 3L,
           'flags': ['write', 'denyoom', 'fast'],
           'key_spec': (1, 1, 1)},
 'SETRANGE': {'arity': 4L,
              'flags': ['write', 'denyoom'],
              'key_spec': (1, 1, 1)},
 'SHUTDOWN': {'arity': -1L,
              'flags': ['readonly', 'admin', 'loading', 'stale'],
              'key_spec': (0, 0, 0)},
 'SINTER': {'arity': -2L,
            'flags': ['readonly', 'sort_for_script'],
            'key_spec': (1, -1, 1)},
 'SINTERSTORE': {'arity': -3L,
                 'flags': ['write', 'denyoom'],
                 'key_spec': (1, -1, 1)},
 'SISMEMBER': {'arity': 3L,
               'flags': ['readonly', 'fast'],
               'key_spec': (1, 1, 1)},
 'SLAVEOF': {'arity': 3L,
             'flags': ['admin', 'noscript', 'stale'],
             'key_spec': (0, 0, 0)},
 'SLOWLOG': {'arity': -2L, 'flags': ['readonly'], 'key_spec': (0, 0, 0)},
 'SMEMBERS': {'arity': 2L,
              'flags': ['readonly', 'sort_for_script'],
              'key_spec': (1, 1, 1)},
 'SMOVE': {'arity': 4L,
           'flags': ['write', 'fast'],
           'key_spec': (1, 2, 1)},
 'SORT': {'arity': -2L,
          'flags': ['write', 'denyoom'],
          'key_spec': (1, 1, 1)},
 'SPOP': {'arity': 2L,
          'flags': ['write', 'noscript', 'random', 'fast'],
          'key_spec': (1, 1, 1)},
 'SRANDMEMBER': {'arity': -2L,
                 'flags': ['readonly', 'random'],
                 'key_spec': (1, 1, 1)},
 'SREM': {'arity': -3L,
          'flags': ['write', 'fast'],
          'key_spec': (1, 1, 1)},
 'SSCAN': {'arity': -3L,
           'flags': ['readonly', 'random'],
           'key_spec': (1, 1, 1)},
 'STRLEN': {'arity': 2L,
            'flags': ['readonly', 'fast'],
            'key_spec': (1, 1, 1)},
 'SUBSCRIBE': {'arity': -2L,
               'flags': ['readonly',
                         'pubsub',
                         'noscript',
                         'loading',
                         'stale'],
               'key_spec': (0, 0, 0)},
 'SUBSTR': {'arity': 4L, 'flags': ['readonly'], 'key_spec': (1, 1, 1)},
 'SUNION': {'arity': -2L,
            'flags': ['readonly', 'sort_for_script'],
            'key_spec': (1, -1, 1)},
 'SUNIONSTORE': {'arity': -3L,
                 'flags': ['write', 'denyoom'],
                 'key_spec': (1, -1, 1)},
 'SYNC': {'arity': 1L,
          'flags': ['readonly', 'admin', 'noscript'],
          'key_spec': (0, 0, 0)},
 'TIME': {'arity': 1L,
          'flags': ['readonly', 'random', 'fast'],
          'key_spec': (0, 0, 0)},
 'TTL': {'arity': 2L,
         'flags': ['readonly', 'fast'],
         'key_spec': (1, 1, 1)},
 'TYPE': {'arity': 2L,
          'flags': ['readonly', 'fast'],
          'key_spec': (1, 1, 1)},
 'UNSUBSCRIBE': {'arity': -1L,
                 'flags': ['readonly',
                           'pubsub',
                           'noscript',
                           'loading',
                           'stale'],
                 'key_spec': (0, 0, 0)},
 'UNWATCH': {'arity': 1L,
             'flags': ['readonly', 'noscript', 'fast'],
             'key_spec': (0, 0, 0)},
 'WATCH': {'arity': -2L,
           'flags': ['readonly', 'noscript', 'fast'],
           'key_spec': (1, -1, 1)},
 'ZADD': {'arity': -4L,
          'flags': ['write', 'denyoom', 'fast'],
          'key_spec': (1, 1, 1)},
 'ZCARD': {'arity': 2L,
           'flags': ['readonly', 'fast'],
           'key_spec': (1, 1, 1)},
 'ZCOUNT': {'arity': 4L,
            'flags': ['readonly', 'fast'],
            'key_spec': (1, 1, 1)},
 'ZINCRBY': {'arity': 4L,
             'flags': ['write', 'denyoom', 'fast'],
             'key_spec': (1, 1, 1)},
 'ZINTERSTORE': {'arity': -4L,
                 'flags': ['write', 'denyoom', 'movablekeys'],
                 'key_spec': (0, 0, 0)},
 'ZLEXCOUNT': {'arity': 4L,
               'flags': ['readonly', 'fast'],
               'key_spec': (1, 1, 1)},
 'ZRANGE': {'arity': -4L, 'flags': ['readonly'], 'key_spec': (1, 1, 1)},
 'ZRANGEBYLEX': {'arity': -4L,
                 'flags': ['readonly'],
                 'key_spec': (1, 1, 1)},
 'ZRANGEBYSCORE': {'arity': -4L,
                   'flags': ['readonly'],
                   'key_spec': (1, 1, 1)},
 'ZRANK': {'arity': 3L,
           'flags': ['readonly', 'fast'],
           'key_spec': (1, 1, 1)},
 'ZREM': {'arity': -3L,
          'flags': ['write', 'fast'],
          'key_spec': (1, 1, 1)},
 'ZREMRANGEBYLEX': {'arity': 4L,
                    'flags': ['write'],
                    'key_spec': (1, 1, 1)},
 'ZREMRANGEBYRANK': {'arity': 4L,
                     'flags': ['write'],
                     'key_spec': (1, 1, 1)},
 'ZREMRANGEBYSCORE': {'arity': 4L,
                      'flags': ['write'],
                      'key_spec': (1, 1, 1)},
 'ZREVRANGE': {'arity': -4L,
               'flags': ['readonly'],
               'key_spec': (1, 1, 1)},
 'ZREVRANGEBYLEX': {'arity': -4L,
                    'flags': ['readonly'],
                    'key_spec': (1, 1, 1)},
 'ZREVRANGEBYSCORE': {'arity': -4L,
                      'flags': ['readonly'],
                      'key_spec': (1, 1, 1)},
 'ZREVRANK': {'arity': 3L,
              'flags': ['readonly', 'fast'],
              'key_spec': (1, 1, 1)},
 'ZSCAN': {'arity': -3L,
           'flags': ['readonly', 'random'],
           'key_spec': (1, 1, 1)},
 'ZSCORE': {'arity': 3L,
            'flags': ['readonly', 'fast'],
            'key_spec': (1, 1, 1)},
 'ZUNIONSTORE': {'arity': -4L,
                 'flags': ['write', 'denyoom', 'movablekeys'],
                 'key_spec': (0, 0, 0)}}


if __name__ == '__main__':
    import redis
    import pprint

    rv = {}
    for row in redis.Redis().execute_command('COMMAND'):
        cmd, arity, flags, first_key, last_key, step_count = row
        rv[cmd.upper()] = {
            'arity': arity,
            'flags': flags,
            'key_spec': (int(first_key), int(last_key), int(step_count)),
        }

    tail = []
    with open(__file__.rstrip('co'), 'r+') as f:
        for line in f:
            if line.strip() == "if __name__ == '__main__':":
                tail.append(line)
                tail.extend(f)
                break

        f.seek(0)
        f.truncate(0)
        f.write('# flake8: noqa\n\nCOMMANDS = %s\n\n\n%s' % (
            pprint.pformat(rv, width=74),
            ''.join(tail)))