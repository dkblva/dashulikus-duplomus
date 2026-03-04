from telebot import TeleBot, types
from telebot.handler_backends import State, StatesGroup
from telebot.storage import StateMemoryStorage
from api_client import client
from config import ADMIN_CHAT_ID, States, EMOJI
from keyboards import *
from utils import *
import json
import asyncio

# Storage for state management
storage = StateMemoryStorage()

# Create bot with FSM
bot = TeleBot(token="8283611145:AAFfb_ETrxyIZajAxVIQrKr0OgaJAlg2vWw", state_storage=storage)

# Temporary storage for user data/context
user_context = {}

def get_context(user_id: int) -> dict:
    """Get user context"""
    if user_id not in user_context:
        user_context[user_id] = {}
    return user_context[user_id]

def set_context(user_id: int, key: str, value):
    """Set user context value"""
    get_context(user_id)[key] = value

def get_context_value(user_id: int, key: str, default=None):
    """Get user context value"""
    return get_context(user_id).get(key, default)

# ==================== Main Commands ====================

@bot.message_handler(commands=['start'])
def cmd_start(message: types.Message):
    """Start command"""
    user_id = message.from_user.id
    bot.set_state(user_id, States.MAIN_MENU, message.chat.id)
    
    text = f"""
👋 Добро пожаловать в админ панель!

Доступные функции:
{EMOJI['applications']} Управление заявками
{EMOJI['spheres']} Сферы деятельности
{EMOJI['types']} Виды деятельности
{EMOJI['tariffs']} Тарифы
{EMOJI['solutions']} Решения по заявкам
{EMOJI['search']} Поиск и фильтрация
"""
    bot.send_message(message.chat.id, text.strip(), reply_markup=main_menu())


@bot.message_handler(lambda msg: "Главное меню" in msg.text)
def cmd_main_menu(message: types.Message):
    """Return to main menu"""
    user_id = message.from_user.id
    bot.set_state(user_id, States.MAIN_MENU, message.chat.id)
    bot.send_message(message.chat.id, "📍 Главное меню", reply_markup=main_menu())


# ==================== Applications Module ====================

@bot.message_handler(lambda msg: "Заявки" in msg.text and States.MAIN_MENU)
def applications_start(message: types.Message):
    """Applications menu"""
    user_id = message.from_user.id
    bot.set_state(user_id, States.APPS_MENU, message.chat.id)
    
    text = f"""
📦 Модуль управления заявками

Выберите действие:
• {EMOJI['view']} Просмотр заявок
• {EMOJI['add']} Создать новую
• {EMOJI['filter']} Фильтры
"""
    bot.send_message(message.chat.id, text.strip(), reply_markup=applications_filter_menu())


@bot.callback_query_handler(func=lambda call: call.data.startswith("app_filter_"))
def app_filter(call: types.CallbackQuery):
    """Filter applications"""
    user_id = call.from_user.id
    chat_id = call.message.chat.id
    data = call.data.split("_")[-1]
    
    asyncio.run(async_app_filter(user_id, chat_id, data, call.message.message_id))


async def async_app_filter(user_id: int, chat_id: int, filter_type: str, msg_id: int):
    """Async filter applications"""
    try:
        apps = await client.get_applications()
        if not apps:
            bot.edit_message_text("❌ Нет заявок", chat_id, msg_id)
            return
        
        # Filter by status
        if filter_type == "new":
            apps = filter_by_status(apps, None)
        elif filter_type == "work":
            apps = filter_by_status(apps, False)
        elif filter_type == "done":
            apps = filter_by_status(apps, True)
        else:
            bot.edit_message_text("❌ Отмена", chat_id, msg_id)
            return
        
        if not apps:
            bot.edit_message_text("❌ Нет заявок с таким статусом", chat_id, msg_id)
            return
        
        # Show first application
        set_context(user_id, "apps_list", apps)
        set_context(user_id, "apps_page", 0)
        
        app = apps[0]
        text = format_application(app)
        
        bot.set_state(user_id, States.APPS_VIEW, chat_id)
        bot.edit_message_text(text, chat_id, msg_id, reply_markup=application_actions_menu(app['id']))
        
    except Exception as e:
        bot.edit_message_text(error_message(str(e)), chat_id, msg_id)


@bot.callback_query_handler(func=lambda call: "app_create_start" in call.data)
def app_create_start(call: types.CallbackQuery):
    """Start creating new application"""
    user_id = call.from_user.id
    chat_id = call.message.chat.id
    
    bot.set_state(user_id, States.APPS_CREATE, chat_id)
    set_context(user_id, "app_data", {})
    
    msg = bot.send_message(chat_id, "📋 Введите ФИО клиента:")
    set_context(user_id, "last_msg_id", msg.message_id)


@bot.message_handler(state=States.APPS_CREATE)
def app_create_name(message: types.Message):
    """Get application name"""
    user_id = message.from_user.id
    chat_id = message.chat.id
    
    data = get_context_value(user_id, "app_data", {})
    data["fullName"] = message.text
    set_context(user_id, "app_data", data)
    
    bot.set_state(user_id, States.APPS_CREATE, chat_id)
    msg = bot.send_message(chat_id, "📞 Введите номер телефона:")
    set_context(user_id, "last_msg_id", msg.message_id)


# ==================== Reference Books (Spheres/Types) ====================

@bot.message_handler(lambda msg: "Сферы" in msg.text)
def spheres_menu(message: types.Message):
    """Spheres menu"""
    user_id = message.from_user.id
    bot.set_state(user_id, States.SPHERES_MENU, message.chat.id)
    
    text = "🏷 Сферы деятельности"
    bot.send_message(message.chat.id, text, reply_markup=reference_menu("sphere"))


@bot.callback_query_handler(func=lambda call: call.data.startswith("sphere_view_"))
def sphere_view(call: types.CallbackQuery):
    """View spheres list"""
    user_id = call.from_user.id
    chat_id = call.message.chat.id
    page = int(call.data.split("_")[-1]) if call.data.split("_")[-1].isdigit() else 0
    
    asyncio.run(async_sphere_view(user_id, chat_id, page, call.message.message_id))


async def async_sphere_view(user_id: int, chat_id: int, page: int, msg_id: int):
    """Async view spheres"""
    try:
        spheres = await client.get_spheres()
        if not spheres:
            bot.edit_message_text("❌ Нет сфер деятельности", chat_id, msg_id)
            return
        
        set_context(user_id, "spheres_list", spheres)
        
        paginated, total_pages = paginate_items(spheres, page)
        text = "🏷 Сферы деятельности:\n\n"
        
        for i, sphere in enumerate(paginated, 1):
            idx = page * ITEMS_PER_PAGE + i
            text += f"{idx}. {sphere.get('nameSphere', 'N/A')}\n"
        
        if total_pages > 1:
            text += f"\n📄 Страница {page + 1}/{total_pages}"
        
        kb = pagination_menu("sphere", page, total_pages, "view")
        
        bot.set_state(user_id, States.SPHERES_VIEW, chat_id)
        bot.edit_message_text(text, chat_id, msg_id, reply_markup=kb)
        
    except Exception as e:
        bot.edit_message_text(error_message(str(e)), chat_id, msg_id)


@bot.callback_query_handler(func=lambda call: call.data.startswith("sphere_create_start"))
def sphere_create_start(call: types.CallbackQuery):
    """Start creating sphere"""
    user_id = call.from_user.id
    chat_id = call.message.chat.id
    
    bot.set_state(user_id, States.SPHERES_CREATE_NAME, chat_id)
    bot.send_message(chat_id, "📝 Введите название сферы деятельности:")


@bot.message_handler(state=States.SPHERES_CREATE_NAME)
def sphere_create_name(message: types.Message):
    """Create sphere with name"""
    user_id = message.from_user.id
    chat_id = message.chat.id
    
    asyncio.run(async_sphere_create(message.text, user_id, chat_id))


async def async_sphere_create(name: str, user_id: int, chat_id: int):
    """Async create sphere"""
    try:
        result = await client.create_sphere(name)
        if result and "error" not in result:
            bot.send_message(chat_id, success_message(f"Сфера '{name}' создана!"))
            bot.set_state(user_id, States.MAIN_MENU, chat_id)
        else:
            bot.send_message(chat_id, error_message(result.get("error", "Unknown error")))
    except Exception as e:
        bot.send_message(chat_id, error_message(str(e)))


# ==================== Types ====================

@bot.message_handler(lambda msg: "Виды" in msg.text)
def types_menu(message: types.Message):
    """Types menu"""
    user_id = message.from_user.id
    bot.set_state(user_id, States.TYPES_MENU, message.chat.id)
    
    text = "🔧 Виды деятельности"
    bot.send_message(message.chat.id, text, reply_markup=reference_menu("type"))


@bot.callback_query_handler(func=lambda call: call.data.startswith("type_view_"))
def type_view(call: types.CallbackQuery):
    """View types list"""
    user_id = call.from_user.id
    chat_id = call.message.chat.id
    page = int(call.data.split("_")[-1]) if call.data.split("_")[-1].isdigit() else 0
    
    asyncio.run(async_type_view(user_id, chat_id, page, call.message.message_id))


async def async_type_view(user_id: int, chat_id: int, page: int, msg_id: int):
    """Async view types"""
    try:
        types_list = await client.get_types()
        if not types_list:
            bot.edit_message_text("❌ Нет видов деятельности", chat_id, msg_id)
            return
        
        set_context(user_id, "types_list", types_list)
        
        paginated, total_pages = paginate_items(types_list, page)
        text = "🔧 Виды деятельности:\n\n"
        
        for i, type_item in enumerate(paginated, 1):
            idx = page * ITEMS_PER_PAGE + i
            text += f"{idx}. {type_item.get('nameType', 'N/A')}\n"
        
        if total_pages > 1:
            text += f"\n📄 Страница {page + 1}/{total_pages}"
        
        kb = pagination_menu("type", page, total_pages, "view")
        
        bot.set_state(user_id, States.TYPES_VIEW, chat_id)
        bot.edit_message_text(text, chat_id, msg_id, reply_markup=kb)
        
    except Exception as e:
        bot.edit_message_text(error_message(str(e)), chat_id, msg_id)


# ==================== Tariffs ====================

@bot.message_handler(lambda msg: "Тарифы" in msg.text)
def tariffs_menu(message: types.Message):
    """Tariffs menu"""
    user_id = message.from_user.id
    bot.set_state(user_id, States.TARIFFS_MENU, message.chat.id)
    
    text = "💰 Управление тарифами"
    bot.send_message(message.chat.id, text, reply_markup=reference_menu("tariff"))


@bot.callback_query_handler(func=lambda call: call.data.startswith("tariff_view_"))
def tariff_view(call: types.CallbackQuery):
    """View tariffs"""
    user_id = call.from_user.id
    chat_id = call.message.chat.id
    page = int(call.data.split("_")[-1]) if call.data.split("_")[-1].isdigit() else 0
    
    asyncio.run(async_tariff_view(user_id, chat_id, page, call.message.message_id))


async def async_tariff_view(user_id: int, chat_id: int, page: int, msg_id: int):
    """Async view tariffs"""
    try:
        tariffs = await client.get_tariffs()
        if not tariffs:
            bot.edit_message_text("❌ Нет тарифов", chat_id, msg_id)
            return
        
        set_context(user_id, "tariffs_list", tariffs)
        
        paginated, total_pages = paginate_items(tariffs, page)
        text = "💰 Тарифы:\n\n"
        
        for i, tariff in enumerate(paginated, 1):
            idx = page * ITEMS_PER_PAGE + i
            text += f"{idx}. {tariff.get('name', 'N/A')} - {tariff.get('price', 0)}₽\n"
            text += f"   {tariff.get('description', '')}\n\n"
        
        if total_pages > 1:
            text += f"📄 Страница {page + 1}/{total_pages}"
        
        kb = pagination_menu("tariff", page, total_pages, "view")
        
        bot.set_state(user_id, States.TARIFFS_VIEW, chat_id)
        bot.edit_message_text(text, chat_id, msg_id, reply_markup=kb)
        
    except Exception as e:
        bot.edit_message_text(error_message(str(e)), chat_id, msg_id)


# ==================== Solutions ====================

@bot.message_handler(lambda msg: "Решения" in msg.text)
def solutions_menu(message: types.Message):
    """Solutions menu"""
    user_id = message.from_user.id
    bot.set_state(user_id, States.SOLUTIONS_MENU, message.chat.id)
    
    text = "✅ Управление решениями"
    bot.send_message(message.chat.id, text, reply_markup=solutions_menu())


# ==================== Search ====================

@bot.message_handler(lambda msg: "Поиск" in msg.text)
def search_menu(message: types.Message):
    """Search menu"""
    user_id = message.from_user.id
    bot.set_state(user_id, States.SEARCH_MENU, message.chat.id)
    
    text = "📊 Поиск и фильтрация"
    bot.send_message(message.chat.id, text, reply_markup=search_menu())


@bot.callback_query_handler(func=lambda call: call.data == "search_by_id")
def search_by_id(call: types.CallbackQuery):
    """Search by ID"""
    user_id = call.from_user.id
    chat_id = call.message.chat.id
    
    bot.set_state(user_id, States.SEARCH_BY_ID, chat_id)
    bot.send_message(chat_id, "🔍 Введите ID заявки:")


@bot.message_handler(state=States.SEARCH_BY_ID)
def search_by_id_result(message: types.Message):
    """Search by ID result"""
    user_id = message.from_user.id
    chat_id = message.chat.id
    
    asyncio.run(async_search_by_id(message.text, user_id, chat_id))


async def async_search_by_id(app_id: str, user_id: int, chat_id: int):
    """Async search by ID"""
    try:
        app = await client.get_application(app_id)
        if app:
            text = format_application(app)
            bot.send_message(chat_id, text, reply_markup=application_actions_menu(app['id']))
            bot.set_state(user_id, States.APPS_VIEW, chat_id)
        else:
            bot.send_message(chat_id, "❌ Заявка не найдена")
    except Exception as e:
        bot.send_message(chat_id, error_message(str(e)))


# ==================== Callback Handlers ====================

@bot.callback_query_handler(func=lambda call: call.data == "noop")
def noop(call: types.CallbackQuery):
    """No operation"""
    bot.answer_callback_query(call.id)


@bot.message_handler(func=lambda msg: True)
def echo(message: types.Message):
    """Echo for unknown commands"""
    bot.send_message(message.chat.id, f"❓ Неизвестная команда: {message.text}")


# ==================== Async Polling ====================

async def start_bot():
    """Start bot with async polling"""
    await client.connect()
    
    # Start polling
    import asyncio
    loop = asyncio.get_event_loop()
    
    try:
        bot.infinity_polling()
    finally:
        await client.disconnect()


if __name__ == "__main__":
    asyncio.run(start_bot())
