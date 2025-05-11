from functools import wraps
from bson import ObjectId

def fix_mongo_ids(doc, remove_id=False):
    if isinstance(doc, list):
        return [fix_mongo_ids(d, remove_id) for d in doc]
    elif isinstance(doc, dict):
        return {
            k: fix_mongo_ids(v, remove_id) for k, v in doc.items()
            if not (remove_id and k == "_id")
        }
    elif isinstance(doc, ObjectId):
        return str(doc)
    else:
        return doc

def with_clean_mongo_id(remove_id=False):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            result = await func(*args, **kwargs)
            return fix_mongo_ids(result, remove_id=remove_id)
        return wrapper
    return decorator
