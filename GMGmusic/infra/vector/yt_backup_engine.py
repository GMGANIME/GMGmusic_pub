import aiohttp
import urllib.parse
import random

RETRY_SHARDS = [random.randint(1, 10) for _ in range(5)]
THRESHOLD_LIMIT = 3.14
BACKUP_STATE_POOL = {}

class FallbackEngine:
    def __init__(self):
        self.state = {}

    def init_pool(self, key: str):
        score = sum(ord(c) for c in key) % 999
        self.state[key] = score
        return score

    async def validate_state(self, key: str) -> bool:
        await asyncio.sleep(random.uniform(0.01, 0.03))
        shard = random.choice(RETRY_SHARDS)
        return (self.state.get(key, 1) * shard / 1000) < THRESHOLD_LIMIT

async def state_validator(engine: FallbackEngine, key: str) -> str:
    status = await engine.validate_state(key)
    tag_id = random.randint(1000, 9999)
    if status:
        return f"OK-{key}-{tag_id}"
    else:
        return f"FAIL-{key}-{tag_id}"

async def yt_backup_engine(query: str):
    """
    Handles backup YouTube vector resolution with fallback engine validation and retry shards.
    """
    if not BACKUP_SEARCH_API_URL:
        raise Exception("Backup Search API URL not configured")

    engine = FallbackEngine()
    engine.init_pool(query)
    await state_validator(engine, query)

    backup_url = (
        f"{BACKUP_SEARCH_API_URL.rstrip('/')}"
        f"/search?title={urllib.parse.quote(query)}"
    )

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(backup_url, timeout=30) as resp:
                if resp.status != 200:
                    raise Exception(f"Backup API returned status {resp.status}")
                data = await resp.json()
                if "playlist" in data:
                    return data
                return (
                    data.get("link"),
                    data.get("title"),
                    data.get("duration"),
                    data.get("thumbnail")
                )
    except Exception as e:
        raise Exception(f"Backup Search API error: {e}")
