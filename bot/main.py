import asyncio
import os
import sys

from app.api.imei_service import check_imei_from_api

sys.path.append(os.path.dirname(os.path.abspath(os.path.join(__file__, ".."))))

from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.client.bot import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.filters import Command
from dotenv import load_dotenv
from app.db.crud import get_all_white_list_users
from app.db.session import get_db


load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
LIVE_API_TOKEN = os.getenv("LIVE_API_TOKEN")

class TelegramBot:
    def __init__(self, token: str):
        self.token = token
        self.bot = Bot(
            token=self.token,
            session=AiohttpSession(),
            default=DefaultBotProperties(parse_mode=ParseMode.HTML)
        )
        self.dp = Dispatcher(storage=MemoryStorage())
        self.register_handlers()

    def register_handlers(self):
        """Регистрация хэндлеров."""
        self.dp.message.register(self.cmd_start, Command("start"))
        self.dp.message.register(self.handle_imei)

    async def cmd_start(self, message: types.Message):
        """Обработка команды /start."""
        user_id = message.from_user.id
        first_name = message.from_user.first_name
        db = next(get_db())
        users = get_all_white_list_users(db)

        if any(user.user_id == user_id for user in users):
            await message.answer(f"Добро пожаловать {first_name}! Отправьте мне IMEI для проверки.")
        else:
            await message.answer(f"Здравствуйте, {first_name}! Извините, Вам доступ закрыт.")


    async def handle_imei(self, message: types.Message):
        """Обработка входящего сообщения с IMEI."""
        imei = message.text.strip()
        if len(imei) != 15 or not imei.isdigit():
            await message.answer("Ошибка: укажите корректный IMEI (15 цифр).")
            return

        valid = check_imei_from_api(imei, LIVE_API_TOKEN)

        await message.answer(f"Ваш IMEI: <b>{imei}</b>")

    async def run(self):
        """Запуск бота."""
        await self.bot.delete_webhook(drop_pending_updates=True)
        await self.dp.start_polling(self.bot)


if __name__ == "__main__":
    async def main():
        bot_instance = TelegramBot(token=BOT_TOKEN)
        await bot_instance.run()

    asyncio.run(main())
