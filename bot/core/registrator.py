import pyrogram
from loguru import logger

from config import settings
from db.functions import register_session_to_db


async def register_sessions() -> None:
    API_ID: int | str = settings.API_ID
    API_HASH: str = settings.API_HASH

    if not API_ID or not API_HASH:
        raise ValueError("API_ID and API_HASH not found in the .env file.")

    session_name: str = input('\nВведите название сессии (для выхода нажмите Enter): ')

    if not session_name:
        return None

    session = pyrogram.Client(
        api_id=API_ID,
        api_hash=API_HASH,
        name=session_name,
        workdir="sessions/"
    )

    async with session:
        user_data = await session.get_me()

    await register_session_to_db(session_name=session_name, tg_id=user_data.id)

    logger.success(f'Успешно добавлена сессия @{user_data.username} | {user_data.first_name} {user_data.last_name}')
