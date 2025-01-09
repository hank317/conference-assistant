redis_cluster_config = {
    'nodes':[
        {'host': '127.0.0.1', 'port': 7001},
        {'host': '127.0.0.1', 'port': 7002},
        {'host': '127.0.0.1', 'port': 7003},
        {'host': '127.0.0.1', 'port': 7004},
        {'host': '127.0.0.1', 'port': 7005},
        {'host': '127.0.0.1', 'port': 7006},
    ],
    'password':"xxxxxxxxx"
}

redis_config = {
    'host':'127.0.0.1',
    'port':'7001',
    'password':'xxxxxxxxx'
}

cluster = True