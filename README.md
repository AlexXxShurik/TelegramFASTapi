# Проверка IMEI и Телеграм-бот

Этот проект предоставляет API для проверки IMEI устройств и Telegram-бота, работающего с пользователями напрямую. Сервис включает базу данных PostgreSQL и полностью упакован в Docker-контейнеры.

## Содержание

- [Описание](#описание)
- [Технологии](#технологии)
- [Установка и запуск](#установка-и-запуск)
- [API Эндпоинты](#api-эндпоинты)
- [Telegram-бот](#telegram-бот)
- [Переменные окружения](#переменные-окружения)
- [Структура проекта](#структура-проекта)
- [Лицензия](#лицензия)

---

## Описание

Проект реализует:
- Проверку информации об устройстве по IMEI через API.
- Управление списком пользователей (добавление в белый список).
- Telegram-бот для взаимодействия с пользователями.

---

## Технологии

- **Язык:** Python 3.10
- **Фреймворк:** FastAPI
- **База данных:** PostgreSQL
- **Telegram SDK:** Aiogram
- **Контейнеризация:** Docker/Docker Compose
- **Дополнительно:** Pydantic, Uvicorn, asyncio

---

## Установка и запуск

### 1. Клонирование репозитория

git clone https://github.com/your-repository-url.git
cd your-repository

### 2. Настройка переменных окружения
Создайте файл .env в корне проекта на основе .env.example и укажите свои переменные:

.env:

SANDBOX_API_TOKEN=your_any_token_for_this_api
LIVE_API_TOKEN=your_api_token_for_imeicheck
BOT_TOKEN=your_telegram_bot_token
POSTGRES_USER=your_postgres_user
POSTGRES_PASSWORD=your_postgres_password
POSTGRES_DB=your_database_name
POSTGRES_HOST='localhost' - если на локальном хосте, 'postgres_db' - если используйте docker

### 3. Запуск с Docker Compose
Постройте и запустите контейнеры:

docker-compose up --build

После запуска:
API будет доступно по адресу: http://localhost:8000
Telegram-бот автоматически запустится и будет готов к использованию.

# API Эндпоинты

## 1. Проверка IMEI

**Метод:** `POST`  
**URL:** `/api/check-imei`  

### Параметры запроса:
| Параметр  | Тип     | Обязательный | Описание                 |
|-----------|---------|--------------|--------------------------|
| `imei`    | `string`| Да           | IMEI устройства (8-15 цифр). |
| `token`   | `string`| Да           | Токен авторизации в формате `Bearer <ваш_токен>`. |

### Пример запроса:
```json
{
  "imei": "123456789012345",
  "token": "Bearer your_api_token"
}

### Пример ответа:

```json
{
  "status": "success",
  "imei": "123456789012345",
  "device_info": {
    "manufacturer": "Apple",
    "model": "iPhone 12",
    "status": "approved"
  }
}

## 2. Добавление в белый список
### Метод: POST
**URL:** `/api/whitelist`

### Параметры запроса:
| Параметр  | Тип     | Обязательный | Описание                                  |
|-----------|---------|--------------|-------------------------------------------|
| `imei`    | `string`| Да           | IMEI устройства (8-15 цифр).              |
| `token`   | `string`| Да           | Токен авторизации в формате `Bearer <ваш_токен>`. |

### Пример запроса:
```json
{
  "imei": "123456789012345",
  "token": "Bearer your_api_token"
}