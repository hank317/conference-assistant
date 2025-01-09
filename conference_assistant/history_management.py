import json
import redis
from rediscluster import RedisCluster, ClusterConnectionPool
from conference_assistant.config import redis_cluster_config, redis_config, cluster


# Redis standalone mode 
if not cluster:
    try:
        client = redis.StrictRedis(host=redis_config.get('host'), port=redis_config.get('port'), password=redis_config.get('password'))
    except Exception as e:
        client = None
# Redis cluster mode
else:
    try:
        pool = ClusterConnectionPool(startup_nodes=redis_cluster_config.get('nodes'), password=redis_cluster_config.get('password'), decode_responses=False)
        client = RedisCluster(connection_pool=pool)
    except Exception as e:
        client = None
    
    
def get_history(session_id: str, round:int) -> list:
    """Retrieve the conversation history of a specific round based on the session ID.

    Args:
        session_id (str): ID used to manage session history.
        round (int): Required historical dialogue length.

    Returns:
        list: Session history.
    """
    if client:
        key = "nbnlp:conferenceAssistantHistory:" + session_id
        value = client.lrange(key, -round, -1)
        return value
    else:
        return []


def set_history(session_id: str, query: str, answer: str) -> None:
    """Store the session content of the current round.
    
    Args:
        session_id (str): ID used to manage session history.
        query (str): User query.
        answer (str): Assistant answer.
    """
    if client:
        key = "nbnlp:conferenceAssistantHistory:" + session_id
        value = {'query':query, 'answer':answer}
        client.rpush(key, json.dumps(value))
        client.expire(key, 600) #过期时间 1h
    
    
def delete_history(session_id: str) -> None:
    """Delete session history.

    Args:
        session_id (str): ID used to manage session history.
    """
    if client:
        key = "nbnlp:conferenceAssistantHistory:" + session_id
        client.delete(key)
        

    
