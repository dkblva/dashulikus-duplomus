# ПОЛНАЯ ДОКУМЕНТАЦИЯ АДМИН ПАНЕЛИ

## Содержание
1. [Обзор системы](#обзор-системы)
2. [Архитектура](#архитектура)
3. [Установка](#установка)
4. [Интеграция](#интеграция)
5. [Использование](#использование)
6. [Расширение](#расширение)

---

## Обзор системы

**Админ панель** - это полнофункциональная Telegram-система управления заявками с интеграцией к REST API.

### Ключевые особенности
- ✅ **FSM (Finite State Machine)** - многошаговые формы
- ✅ **Асинхронность** - неблокирующая работа с API
- ✅ **Пагинация** - удобный просмотр больших списков
- ✅ **Inline-кнопки** - быстрые действия
- ✅ **Валидация** - проверка input данных
- ✅ **Обработка ошибок** - понятные сообщения
- ✅ **Контекст пользователей** - сохранение состояния

---

## Архитектура

```
┌─────────────────────────────┐
│   Telegram Bot (pyTeleBot)  │
│                             │
│ ┌───────────────────────┐   │
│ │  bot_extended.py      │   │ - Основная логика
│ │  (FSM handlers)       │   │ - Обработчики команд
│ └───────────────────────┘   │ - Управление состояниями
│         ↓                   │
│ ┌───────────────────────┐   │
│ │  keyboards.py         │   │ - Inline-кнопки
│ │  (UI Layer)           │   │ - Reply-кнопки
│ └───────────────────────┘   │
│         ↓                   │
│ ┌───────────────────────┐   │
│ │  utils.py             │   │ - Форматирование
│ │  (Utilities)          │   │ - Фильтрация
│ │                       │   │ - Поиск
│ └───────────────────────┘   │
└─────────────────────────────┘
         ↓ (async)
┌─────────────────────────────┐
│   api_client.py             │
│   (Async HTTP Client)       │
└─────────────────────────────┘
         ↓ (HTTP)
┌─────────────────────────────┐
│   FormAPI (.NET)            │
│   - Applications            │
│   - SphereActivity          │
│   - TypeActivity            │
│   - Tarif                   │
│   - Solution                │
└─────────────────────────────┘
         ↓
┌─────────────────────────────┐
│   SQL Server Database       │
│   (FormDB)                  │
└─────────────────────────────┘
```

---

## Установка

### Предварительные требования
- Python 3.8+
- pip
- Telegram Bot Token (от @BotFather)
- Ваш Telegram ID (от @userinfobot)

### Шаг 1: Клонирование

```bash
cd dashulikus-duplomus-master/bot
```

### Шаг 2: Установка зависимостей

```bash
pip install -r requirements.txt
```

Зависимости:
```
telebot==4.21.0          # Telegram Bot API
aiohttp==3.9.1           # Async HTTP client
pydantic==2.5.0          # Data validation
python-dotenv==1.0.0     # Environment variables
fastapi==0.105.0         # For webhook support (optional)
uvicorn==0.24.0          # ASGI server (optional)
```

### Шаг 3: Конфигурация

Отредактируйте `config.py`:

```python
# Telegram Bot
TOKEN = "ВАШ_ТОКЕН_ОТ_BOTFATHER"      # Получить у @BotFather
ADMIN_CHAT_ID = ВАШ_TELEGRAM_ID         # Получить у @userinfobot

# API Configuration
API_BASE_URL = "http://localhost:5000"  # URL вашего API
API_TIMEOUT = 10                        # Timeout в секундах

# Pagination
ITEMS_PER_PAGE = 5                      # Элементов на странице

# Если используете .env файл:
# Создайте .env:
# TELEGRAM_TOKEN=xxx
# API_URL=http://localhost:5000
# ADMIN_ID=123456
```

### Шаг 4: Запуск бота

```bash
# Основная версия с расширенным функционалом
python bot_extended.py

# Если используется Docker:
docker build -t admin-bot .
docker run --env-file .env admin-bot
```

---

## Интеграция

### API Endpoints

#### Applications (Заявки)
```
GET    /api/applications           - Все заявки
GET    /api/applications/{id}      - По ID
POST   /api/applications           - Создать
PUT    /api/applications/{id}      - Обновить
DELETE /api/applications/{id}      - Удалить

Request body (POST/PUT):
{
  "fullName": "Иван Петров",
  "phoneNumber": "+7 (950) 123-45-67",
  "email": "ivan@example.com",
  "organizationName": "Рога и копыта",
  "sphereId": "00000000-0000-0000-0000-000000000000",  // (optional)
  "typeId": "00000000-0000-0000-0000-000000000000",    // (optional)
  "status": false,  // null = новая, false = в работе, true = завершена
  "comment": "Комментарий"  // (optional)
}
```

#### SphereActivity (Сферы деятельности)
```
GET    /api/sphereActivity         - Все сферы
GET    /api/sphereActivity/{id}    - По ID
POST   /api/sphereActivity         - Создать
PUT    /api/sphereActivity/{id}    - Обновить
DELETE /api/sphereActivity/{id}    - Удалить

Request body:
{
  "nameSphere": "IT Консалтинг"
}
```

#### TypeActivity (Виды деятельности)
```
GET    /api/typeActivity           - Все виды
GET    /api/typeActivity/{id}      - По ID
POST   /api/typeActivity           - Создать
PUT    /api/typeActivity/{id}      - Обновить
DELETE /api/typeActivity/{id}      - Удалить

Request body:
{
  "nameType": "Разработка ПО"
}
```

#### Tarif (Тарифы)
```
GET    /api/tarif                  - Все тарифы
GET    /api/tarif/{id}             - По ID
POST   /api/tarif                  - Создать
PUT    /api/tarif/{id}             - Обновить
DELETE /api/tarif/{id}             - Удалить

Request body:
{
  "name": "Premium",
  "description": "Полный пакет услуг",
  "price": 50000
}
```

#### Solution (Решения)
```
GET    /api/solution               - Все решения
GET    /api/solution/{id}          - По ID
POST   /api/solution               - Создать
PUT    /api/solution/{id}          - Обновить
DELETE /api/solution/{id}          - Удалить

Request body:
{
  "description": "Разработка мобильного приложения",
  "idApplication": "00000000-0000-0000-0000-000000000000",
  "idTarif": "00000000-0000-0000-0000-000000000000"
}
```

### Использование API Client

```python
from api_client import client
import asyncio

async def example():
    # Подключение
    await client.connect()
    
    # Applications
    apps = await client.get_applications()
    app = await client.get_application("app-id")
    await client.create_application({...})
    await client.update_application("app-id", {...})
    await client.delete_application("app-id")
    
    # Spheres
    spheres = await client.get_spheres()
    await client.create_sphere("IT Консалтинг")
    
    # Types
    types = await client.get_types()
    await client.create_type("Разработка")
    
    # Tariffs
    tariffs = await client.get_tariffs()
    await client.create_tariff("Premium", "Описание", 50000)
    
    # Solutions
    solutions = await client.get_solutions()
    await client.create_solution("app-id", "tarif-id", "Описание")
    
    # Отключение
    await client.disconnect()

# Запуск
asyncio.run(example())
```

---

## Использование

### Основные потоки

#### 1. Просмотр заявок

```
Пользователь: /start
        ↓
Бот: Главное меню
        ↓
Пользователь: 📦 Заявки
        ↓
Бот: Выбрать фильтр
        ↓
Пользователь: ⏳ В работе
        ↓
Бот: Показать первую заявку
        ↓
Пользователь: ✏️ Редактировать
        ↓
Бот: Выбрать поле
        ↓
Пользователь: Новое значение
        ↓
Бот: ✅ Поле обновлено
```

#### 2. Создание решения

```
Пользователь: 📦 Заявки → Выбрать заявку → 💼 Решение
        ↓
Бот: Выбрать тариф
        ↓
Пользователь: Выбрать тариф
        ↓
Бот: Ввести описание
        ↓
Пользователь: Описание решения
        ↓
Бот: ✅ Решение создано
```

#### 3. Поиск

```
Пользователь: 📊 Поиск → По телефону
        ↓
Пользователь: +7 (950) 123-45-67
        ↓
Бот: Результаты поиска (до 5)
        ↓
Пользователь: Может тапнуть на результат
```

### Команды

```
/start, /menu     - Главное меню
/cancel           - Отмена текущей операции
/help             - Справка
```

### Estados (FSM States)

```python
MAIN_MENU                    # Главное меню
APPS_MENU                    # Меню заявок
APPS_VIEW                    # Просмотр заявки
APPS_CREATE                  # Создание заявки
APPS_EDIT                    # Редактирование
APPS_EDIT_FIELD              # Редактирование поля
APPS_STATUS_CHANGE           # Смена статуса

SPHERES_MENU, SPHERES_VIEW, SPHERES_CREATE_NAME, SPHERES_EDIT_NAME
TYPES_MENU, TYPES_VIEW, TYPES_CREATE_NAME, TYPES_EDIT_NAME
TARIFFS_MENU, TARIFFS_VIEW, TARIFFS_CREATE_*, TARIFFS_EDIT_FIELD

SOLUTIONS_MENU
SOLUTIONS_SELECT_APP
SOLUTIONS_SELECT_TARIFF
SOLUTIONS_ENTER_DESC
SOLUTIONS_VIEW

SEARCH_MENU
SEARCH_BY_ID, SEARCH_BY_PHONE, SEARCH_BY_EMAIL, SEARCH_BY_ORG, SEARCH_BY_DATE
```

---

## Расширение

### Добавить новый тип поиска

1. **config.py** - добавить состояние:
```python
class States:
    SEARCH_BY_STATUS = "search_by_status"
```

2. **keyboards.py** - добавить кнопку:
```python
def search_menu():
    kb.add(
        InlineKeyboardButton("📊 По статусу", callback_data="search_by_status")
    )
```

3. **bot_extended.py** - обработчик:
```python
@bot.callback_query_handler(func=lambda call: call.data == "search_by_status")
def handle_search_status(call: types.CallbackQuery):
    # Логика
    pass
```

### Добавить новый модуль

1. Добавить методы в `api_client.py`
2. Добавить состояния в `config.py`
3. Создать обработчики в `bot_extended.py`
4. Добавить клавиатуры в `keyboards.py`
5. Добавить утилиты в `utils.py`

### Пример: Новый модуль "Комментарии"

**config.py:**
```python
class States:
    COMMENTS_MENU = "comments_menu"
    COMMENTS_VIEW = "comments_view"
    COMMENTS_CREATE = "comments_create"
```

**api_client.py:**
```python
async def get_comments(self, app_id: str) -> Optional[List[Dict]]:
    result = await self._request("GET", f"api/comments/{app_id}")
    return result if isinstance(result, list) else None

async def add_comment(self, app_id: str, text: str) -> Optional[Dict]:
    data = {"applicationId": app_id, "text": text}
    return await self._request("POST", "api/comments", json=data)
```

**bot_extended.py:**
```python
def comments_start(message: types.Message):
    user_id = message.from_user.id
    bot.set_state(user_id, States.COMMENTS_MENU, message.chat.id)
    bot.send_message(message.chat.id, "💬 Комментарии")
```

---

## Обработка ошибок

### Common Issues

#### 1. "Timeout: API не ответил"
```
Причина: API недоступен или медленно отвечает
Решение: 
- Проверить URL в config.py
- Убедиться что API запущен
- Увеличить timeout в config.py
```

#### 2. "CORS Error"
```
Причина: CrossOriginResourceSharing блокирует запрос
Решение: 
- Проверить CORS конфигурацию в Program.cs
- Убедиться что API запущен с CORS разрешением
```

#### 3. "Заявка не найдена"
```
Причина: ID заявки неверный или заявка удалена
Решение:
- Проверить ID
- Проверить в базе данных
```

#### 4. FSM состояние не меняется
```
Причина: StateMemoryStorage теряет состояние при перезагрузке
Решение:
- Для продакшена используйте Redis:
from telebot.storage import RedisStorage
storage = RedisStorage(host='localhost', port=6379)
```

---

## Мониторинг и Логирование

### Базовое логирование

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

logger.info(f"User {user_id} started search")
logger.error(f"API error: {e}")
```

### Логирование в файл

```python
file_handler = logging.FileHandler('bot.log')
file_handler.setLevel(logging.DEBUG)

logger.addHandler(file_handler)
```

---

## Deployment

### На локальной машине
```bash
python bot_extended.py
```

### С использованием systemd (Linux)

Создать `/etc/systemd/system/admin-bot.service`:
```ini
[Unit]
Description=Admin Telegram Bot
After=network.target

[Service]
Type=simple
User=botuser
WorkingDirectory=/home/botuser/bot
ExecStart=/usr/bin/python3 /home/botuser/bot/bot_extended.py

Restart=on-failure
RestartSec=10

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl daemon-reload
sudo systemctl enable admin-bot
sudo systemctl start admin-bot
```

### С использованием Docker

**Dockerfile:**
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["python", "bot_extended.py"]
```

```bash
docker build -t admin-telegram-bot .
docker run --env-file .env admin-telegram-bot
```

### На VPS (например, VPS с Ubuntu)

1. SSH подключение
2. Установка Python и pip
3. Клонирование репозитория
4. Установка зависимостей
5. Запуск с supervisord или systemd
6. Использование Let's Encrypt для HTTPS (если нужен webhook)

---

## Performance Tips

1. **Кеширование:**
```python
# Кешировать списки справочников (они меняются редко)
cache = {}
cache_time = {}

async def get_cached_spheres():
    if 'spheres' in cache and time.time() - cache_time.get('spheres', 0) < 3600:
        return cache['spheres']
    
    spheres = await client.get_spheres()
    cache['spheres'] = spheres
    cache_time['spheres'] = time.time()
    return spheres
```

2. **Асинхронные батчи:**
```python
async def batch_get_apps():
    tasks = [
        client.get_application(id1),
        client.get_application(id2),
        client.get_application(id3),
    ]
    return await asyncio.gather(*tasks)
```

3. **Пулинг вместо вебхуков:**
```python
# infinity_polling более надежен для большинства случаев
bot.infinity_polling()

# Если нужны вебхуки, используйте FastAPI
from fastapi import FastAPI, Request

app = FastAPI()

@app.post("/telegram-webhook")
async def webhook(request: Request):
    json_data = await request.json()
    update = types.Update.de_json(json_data)
    bot.process_new_updates([update])
```

---

## Тестирование

### Unit тесты

```python
import unittest
from unittest.mock import patch, AsyncMock

class TestAPIClient(unittest.TestCase):
    async def test_get_applications(self):
        with patch('aiohttp.ClientSession.get') as mock:
            mock.return_value.__aenter__.return_value.json = AsyncMock(
                return_value=[{"id": "123", "fullName": "Test"}]
            )
            
            apps = await client.get_applications()
            assert len(apps) == 1

if __name__ == '__main__':
    unittest.main()
```

### Integration тесты

```python
# Подключиться к real API и протестировать
async def test_integration():
    await client.connect()
    
    apps = await client.get_applications()
    assert isinstance(apps, list)
    
    await client.disconnect()

asyncio.run(test_integration())
```

---

## FAQ

**Q: Как изменить язык бота?**
A: Все сообщения в bot_extended.py, переведите нужные строки на другой язык.

**Q: Как добавить администраторов?**
A: Создайте список админов в config.py и проверяйте `message.from_user.id` перед доступом.

**Q: Как ограничить доступ только к определенным пользователям?**
```python
ADMIN_IDS = [506698213, 123456789]

if message.from_user.id not in ADMIN_IDS:
    bot.send_message(message.chat.id, "❌ Доступ запрещен")
    return
```

**Q: Как добавить много ботов на один API?**
A: Создавайте отдельные экземпляры бота с разными токенами и одним API клиентом.

**Q: Как увеличить скорость работы?**
A: - Используйте Redis для хранения состояний
   - Кешируйте часто запрашиваемые данные
   - Используйте асинхронные батчи для множественных запросов

---

## Лицензия

Часть проекта dashulikus-duplomus

## Контакты

Для вопросов и пожеланий - отправьте Issues на GitHub
