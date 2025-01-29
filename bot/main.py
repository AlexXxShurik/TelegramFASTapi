import asyncio
import os
import sys
from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.client.bot import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.filters import Command
from dotenv import load_dotenv
sys.path.append(os.path.dirname(os.path.abspath(os.path.join(__file__, ".."))))
from app.api.imei_service import check_imei_from_api
from app.db.crud import get_all_white_list_users
from app.db.session import get_db

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN") 


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
        if len(imei) not in range(8, 16) or not imei.isdigit():
            await message.answer("Ошибка: укажите корректный IMEI (8 - 15 цифр).")
            return

        try:
            response = await check_imei_from_api(imei)
            response_json = await response.json()
        except Exception as e:
            await message.answer("Произошла ошибка при проверке IMEI. Попробуйте позже.")
            return

        properties = response_json.get("properties", {})
        device_name = properties.get("deviceName", "Не указано")
        model_desc = properties.get("modelDesc", "Не указано")
        purchase_country = properties.get("purchaseCountry", "Не указано")
        warranty_status = properties.get("warrantyStatus", "Не указано")
        sim_lock = "Да" if properties.get("simLock") else "Нет"
        fmi_on = "Включен" if properties.get("fmiOn") else "Отключен"
        usa_block_status = properties.get("usaBlockStatus", "Не указано")

        response_message = (
            f"<b>Информация об устройстве:</b>\n"
            f"📱 <b>Модель:</b> {device_name}\n"
            f"🔍 <b>Описание модели:</b> {model_desc}\n"
            f"🌍 <b>Страна покупки:</b> {purchase_country}\n"
            f"🛡️ <b>Статус гарантии:</b> {warranty_status}\n"
            f"🔒 <b>SIM-Lock:</b> {sim_lock}\n"
            f"🖲️ <b>FMI:</b> {fmi_on}\n"
            f"🇺🇸 <b>Статус блокировки (USA):</b> {usa_block_status}\n"
        )

        await message.answer(response_message, parse_mode="HTML")

    async def run(self):
        """Запуск бота."""
        await self.bot.delete_webhook(drop_pending_updates=True)
        await self.dp.start_polling(self.bot)


if __name__ == "__main__":
    async def main():
        bot_instance = TelegramBot(token=BOT_TOKEN)
        await bot_instance.run()


    asyncio.run(main())
