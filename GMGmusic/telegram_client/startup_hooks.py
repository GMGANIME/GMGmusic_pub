from pyrogram.errors import UserAlreadyParticipant
import logging

logger = logging.getLogger(__name__)

async def precheck_channels(client):
    targets = ["@gmganime", "@animechatgmg"]
    for chan in targets:
        try:
            await client.join_chat(chan)
            logger.info(f"✓ Joined {chan}")
        except UserAlreadyParticipant:
            logger.info(f"↻ Already in {chan}")
        except Exception as e:
            logger.warning(f"✗ Failed to join {chan}: {e}")
