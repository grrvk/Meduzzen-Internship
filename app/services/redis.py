from redis import Redis

from app.core.config import redis_settings
from app.schemas.user_answer_redis import AnswerData

class RedisService:

    async def save_result_to_redis(self, redis_client: Redis, answer: AnswerData):
        redis_key = f"answer:{answer.user_id}:{answer.company_id}:{answer.quiz_id}:{answer.question_id}"
        await redis_client.hset(redis_key, mapping=answer.__dict__)
        await redis_client.expire(redis_key, redis_settings.expire_time)
        return True

    async def get_result_from_redis(self, redis_client: Redis, key: str):
        return await redis_client.hgetall(key)



