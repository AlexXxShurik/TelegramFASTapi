# Проверка IMEI и Телеграм-бот

Проект предоставляет API для проверки IMEI устройств и Telegram-бот, упрощающий взаимодействие с пользователями. Решение поддерживает PostgreSQL и полностью упаковано в контейнеры Docker.

---

## Содержание

1. [Описание](#описание)  
2. [Основной функционал](#основной-функционал)  
3. [Технологии](#технологии)  
4. [Установка и запуск](#установка-и-запуск)  
5. [API Эндпоинты](#api-эндпоинты)  
6. [Telegram-бот](#telegram-бот)  
7. [Переменные окружения](#переменные-окружения)  
8. [Структура проекта](#структура-проекта)  
9. [Лицензия](#лицензия)

---

## Описание

Данный проект разработан для автоматизации проверки IMEI устройств. Инструмент включает:  
- API для интеграции с внешними системами.  
- Telegram-бот для взаимодействия с конечными пользователями.  
- Возможность добавления устройств в белый список.  

Проект масштабируем и легко интегрируется в существующие системы благодаря контейнеризации.

---

## Основной функционал

1. Проверка IMEI через API и Telegram-бота.  
2. Управление белым списком IMEI.  
3. Безопасное хранение данных пользователей в PostgreSQL.

---

## Технологии

- **Язык программирования:** Python 3.10  
- **Фреймворки и библиотеки:**  
  - FastAPI для создания API  
  - Aiogram для работы с Telegram  
  - SQLAlchemy для работы с базой данных  
- **Контейнеризация:** Docker, Docker Compose  
- **База данных:** PostgreSQL  
- **Дополнительно:** Pydantic, Uvicorn, asyncio  

---

## Установка и запуск

### 1. Клонирование репозитория

Клонируйте репозиторий в локальную директорию:  
```bash
git clone https://github.com/your-repository-url.git
cd your-repository
```

### 2. Настройка переменных окружения

Создайте файл `.env` в корне проекта на основе `.env.example` и заполните его:

```plaintext
SANDBOX_API_TOKEN=your_any_token_for_this_api
LIVE_API_TOKEN=your_api_token_for_imeicheck
BOT_TOKEN=your_telegram_bot_token
POSTGRES_USER=your_postgres_user
POSTGRES_PASSWORD=your_postgres_password
POSTGRES_DB=your_database_name
POSTGRES_HOST=postgres_db  # Для Docker укажите имя сервиса из docker-compose.yml
```

### 3. Запуск с Docker Compose

Соберите и запустите проект с помощью Docker Compose:  
```bash
docker-compose up --build
```

После запуска:  
- API доступно по адресу: [http://localhost:8000](http://localhost:8000)  
- Telegram-бот запускается автоматически.  

---

## API Эндпоинты

### 1. Проверка IMEI

**Метод:** `POST`  
**URL:** `/api/check-imei`  

#### Параметры запроса:
| Параметр  | Тип     | Обязательный | Описание                 |
|-----------|---------|--------------|--------------------------|
| `imei`    | `string`| Да           | IMEI устройства (8-15 цифр). |
| `token`   | `string`| Да           | Токен авторизации в формате `Bearer <ваш_токен>`. |

#### Пример запроса:
```json
{
  "imei": "123456789012345",
  "token": "Bearer your_api_token"
}
```

#### Пример ответа:
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
```

### 2. Добавление IMEI в белый список

**Метод:** `POST`  
**URL:** `/api/whitelist`  

#### Параметры запроса:
| Параметр  | Тип     | Обязательный | Описание                 |
|-----------|---------|--------------|--------------------------|
| `imei`    | `string`| Да           | IMEI устройства.         |
| `token`   | `string`| Да           | Авторизационный токен.   |

#### Пример запроса:
```json
{
  "imei": "123456789012345",
  "token": "Bearer your_api_token"
}
```

#### Пример ответа:
```json
{
  "message": "IMEI added to whitelist successfully",
  "imei": "123456789012345"
}
```

---

## Telegram-бот

### Основные команды

#### `/start`
- Проверяет, находится ли пользователь в белом списке.  
- Если пользователь в списке, открывает доступ к функциям проверки IMEI.  

#### Отправка IMEI
Пользователь отправляет IMEI, а бот возвращает данные об устройстве.  

**Пример сообщения от бота:**
```
📱 Модель: iPhone 12  
🔍 Описание: Apple iPhone 12  
🛡️ Гарантия: Активна  
🔒 SIM-Lock: Нет  
```

---

## Переменные окружения

| Переменная          | Описание                                    | Пример значения          |
|----------------------|---------------------------------------------|--------------------------|
| `SANDBOX_API_TOKEN`  | Токен для доступа к тестовому API.          | `test_token_123`         |
| `LIVE_API_TOKEN`     | Токен для доступа к основному API.          | `live_token_456`         |
| `BOT_TOKEN`          | Токен Telegram-бота.                       | `123456:ABC-DEF1234ghIkl`|
| `POSTGRES_USER`      | Имя пользователя базы данных PostgreSQL.    | `postgres`               |
| `POSTGRES_PASSWORD`  | Пароль пользователя базы данных PostgreSQL.| `password123`            |
| `POSTGRES_DB`        | Название базы данных.                      | `imei_service`           |
| `POSTGRES_HOST`      | Хост базы данных.                          | `postgres_db`            |

---

## Структура проекта

```plaintext
├── app
│   ├── api
│   │   ├── imei_service.py      # Логика взаимодействия с внешними API.
│   │   ├── models.py            # Pydantic-схемы.
│   ├── db
│   │   ├── crud.py              # CRUD-операции.
│   │   ├── model.py             # Модели базы данных.
│   │   ├── session.py           # Конфигурация подключения к БД.
│   ├── main.py                  # Точка входа FastAPI.
├── telegram_bot.py              # Основная логика Telegram-бота.
├── docker-compose.yml           # Конфигурация Docker Compose.
├── requirements.txt             # Зависимости Python.
├── .env.example                 # Шаблон переменных окружения.
```
