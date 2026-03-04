"""
Complete Admin Bot - FULL VERSION with all features
Applications, Spheres, Types, Tariffs, Solutions, Search
"""

import telebot
from telebot import types
from config import ADMIN_CHAT_ID, States, EMOJI, ITEMS_PER_PAGE, TOKEN
from keyboards import *
import requests
import json
from datetime import datetime

bot = telebot.TeleBot(token=TOKEN, skip_pending=True)
user_context = {}

def get_context(user_id):
    if user_id not in user_context:
        user_context[user_id] = {'state': 'main_menu'}
    return user_context[user_id]

def set_state(user_id, state):
    ctx = get_context(user_id)
    ctx['state'] = state
    print(f"   🔄 State: {state}", flush=True)

def call_api(method, endpoint, data=None):
    """Synchronous API call with logging"""
    try:
        url = f"https://localhost:7082/{endpoint}"
        headers = {"Content-Type": "application/json"}
        
        print(f"   📡 {method} {endpoint}", flush=True)
        if data and method != "GET":
            print(f"      📦 {json.dumps(data, ensure_ascii=False)[:100]}", flush=True)
        
        if method == "GET":
            r = requests.get(url, headers=headers, verify=False, timeout=5)
        elif method == "POST":
            r = requests.post(url, json=data, headers=headers, verify=False, timeout=5)
        elif method == "PUT":
            r = requests.put(url, json=data, headers=headers, verify=False, timeout=5)
        elif method == "DELETE":
            r = requests.delete(url, headers=headers, verify=False, timeout=5)
        else:
            return None
        
        print(f"      Status: {r.status_code}", flush=True)
        
        if r.status_code in [200, 201]:
            return r.json()
        elif r.status_code == 204:
            return {"status": "ok"}
        else:
            err_text = r.text[:150] if r.text else "No response"
            print(f"      ❌ {err_text}", flush=True)
            return None
    except Exception as e:
        print(f"   ❌ Exception: {str(e)[:100]}", flush=True)
        return None

# ==================== APPLICATION CREATION ====================

@bot.message_handler(func=lambda msg: get_context(msg.from_user.id).get('state') == 'app_fullName')
def app_step_fullName(message):
    user_id = message.from_user.id
    chat_id = message.chat.id
    name = message.text.strip()
    
    if not name or len(name) < 2:
        bot.send_message(chat_id, "❌ ФИО должно быть не менее 2 символов")
        return
    
    get_context(user_id)['app_fullName'] = name
    set_state(user_id, 'app_phoneNumber')
    bot.send_message(chat_id, "📞 Введите номер телефона:")

@bot.message_handler(func=lambda msg: get_context(msg.from_user.id).get('state') == 'app_phoneNumber')
def app_step_phone(message):
    user_id = message.from_user.id
    chat_id = message.chat.id
    phone = message.text.strip()
    
    get_context(user_id)['app_phoneNumber'] = phone
    set_state(user_id, 'app_email')
    bot.send_message(chat_id, "📧 Введите email:")

@bot.message_handler(func=lambda msg: get_context(msg.from_user.id).get('state') == 'app_email')
def app_step_email(message):
    user_id = message.from_user.id
    chat_id = message.chat.id
    email = message.text.strip()
    
    get_context(user_id)['app_email'] = email
    set_state(user_id, 'app_organizationName')
    bot.send_message(chat_id, "🏢 Введите организацию:")

@bot.message_handler(func=lambda msg: get_context(msg.from_user.id).get('state') == 'app_organizationName')
def app_step_org(message):
    user_id = message.from_user.id
    chat_id = message.chat.id
    org = message.text.strip()
    
    ctx = get_context(user_id)
    ctx['app_organizationName'] = org
    
    # Try to create
    app_data = {
        'fullName': ctx.get('app_fullName', ''),
        'phoneNumber': ctx.get('app_phoneNumber', ''),
        'email': ctx.get('app_email', ''),
        'organizationName': org
    }
    
    print(f"✅ Creating app: {json.dumps(app_data, ensure_ascii=False)}", flush=True)
    
    result = call_api("POST", "api/applications", app_data)
    
    if result:
        bot.send_message(chat_id, "✅ Заявка создана!")
    else:
        bot.send_message(chat_id, "❌ Ошибка создания заявки")
    
    set_state(user_id, 'main_menu')
    cmd_start(message)

# ==================== SPHERE CREATION ====================

@bot.message_handler(func=lambda msg: get_context(msg.from_user.id).get('state') == 'sphere_create')
def sphere_create_handler(message):
    user_id = message.from_user.id
    chat_id = message.chat.id
    name = message.text.strip()
    
    if not name or len(name) < 2:
        bot.send_message(chat_id, "❌ Минимум 2 символа")
        return
    
    result = call_api("POST", "api/sphereActivity", {"nameSphere": name})
    
    if result:
        bot.send_message(chat_id, f"✅ Сфера создана!")
    else:
        bot.send_message(chat_id, "❌ Ошибка")
    
    set_state(user_id, 'main_menu')
    cmd_start(message)

# ==================== TYPE CREATION ====================

@bot.message_handler(func=lambda msg: get_context(msg.from_user.id).get('state') == 'type_create')
def type_create_handler(message):
    user_id = message.from_user.id
    chat_id = message.chat.id
    name = message.text.strip()
    
    if not name or len(name) < 2:
        bot.send_message(chat_id, "❌ Минимум 2 символа")
        return
    
    result = call_api("POST", "api/typeActivity", {"nameType": name})
    
    if result:
        bot.send_message(chat_id, f"✅ Вид создан!")
    else:
        bot.send_message(chat_id, "❌ Ошибка")
    
    set_state(user_id, 'main_menu')
    cmd_start(message)

# ==================== TARIFF CREATION ====================

@bot.message_handler(func=lambda msg: get_context(msg.from_user.id).get('state') == 'tariff_name')
def tariff_step_name(message):
    user_id = message.from_user.id
    chat_id = message.chat.id
    name = message.text.strip()
    
    if not name or len(name) < 2:
        bot.send_message(chat_id, "❌ Минимум 2 символа")
        return
    
    get_context(user_id)['tariff_name'] = name
    set_state(user_id, 'tariff_desc')
    bot.send_message(chat_id, "📝 Описание:")

@bot.message_handler(func=lambda msg: get_context(msg.from_user.id).get('state') == 'tariff_desc')
def tariff_step_desc(message):
    user_id = message.from_user.id
    chat_id = message.chat.id
    desc = message.text.strip()
    
    get_context(user_id)['tariff_desc'] = desc
    set_state(user_id, 'tariff_price')
    bot.send_message(chat_id, "💰 Цена (число):")

@bot.message_handler(func=lambda msg: get_context(msg.from_user.id).get('state') == 'tariff_price')
def tariff_step_price(message):
    user_id = message.from_user.id
    chat_id = message.chat.id
    
    try:
        price = int(float(message.text.strip()))
    except ValueError:
        bot.send_message(chat_id, "❌ Введите число")
        return
    
    ctx = get_context(user_id)
    result = call_api("POST", "api/tarif", {
        "name": ctx['tariff_name'],
        "description": ctx['tariff_desc'],
        "price": price
    })
    
    if result:
        bot.send_message(chat_id, "✅ Тариф создан!")
    else:
        bot.send_message(chat_id, "❌ Ошибка")
    
    set_state(user_id, 'main_menu')
    cmd_start(message)

# ==================== SEARCH ====================

@bot.message_handler(func=lambda msg: get_context(msg.from_user.id).get('state') == 'search_phone')
def search_by_phone(message):
    user_id = message.from_user.id
    chat_id = message.chat.id
    phone = message.text.strip()
    
    apps = call_api("GET", "api/applications")
    if not apps:
        bot.send_message(chat_id, "❌ Нет заявок")
        set_state(user_id, 'main_menu')
        return
    
    filtered = [a for a in apps if phone in a.get('phoneNumber', '')]
    
    if filtered:
        text = f"📱 Найдено: {len(filtered)}\n\n"
        for app in filtered[:5]:
            text += f"👤 {app.get('fullName', '-')}\n📞 {app.get('phoneNumber', '-')}\n\n"
        bot.send_message(chat_id, text)
    else:
        bot.send_message(chat_id, "❌ Не найдено")
    
    set_state(user_id, 'main_menu')

@bot.message_handler(func=lambda msg: get_context(msg.from_user.id).get('state') == 'search_email')
def search_by_email(message):
    user_id = message.from_user.id
    chat_id = message.chat.id
    email = message.text.strip()
    
    apps = call_api("GET", "api/applications")
    if not apps:
        bot.send_message(chat_id, "❌ Нет заявок")
        set_state(user_id, 'main_menu')
        return
    
    filtered = [a for a in apps if email.lower() in a.get('email', '').lower()]
    
    if filtered:
        text = f"📧 Найдено: {len(filtered)}\n\n"
        for app in filtered[:5]:
            text += f"👤 {app.get('fullName', '-')}\n📧 {app.get('email', '-')}\n\n"
        bot.send_message(chat_id, text)
    else:
        bot.send_message(chat_id, "❌ Не найдено")
    
    set_state(user_id, 'main_menu')

@bot.message_handler(func=lambda msg: get_context(msg.from_user.id).get('state') == 'search_org')
def search_by_org(message):
    user_id = message.from_user.id
    chat_id = message.chat.id
    org = message.text.strip()
    
    apps = call_api("GET", "api/applications")
    if not apps:
        bot.send_message(chat_id, "❌ Нет заявок")
        set_state(user_id, 'main_menu')
        return
    
    filtered = [a for a in apps if org.lower() in a.get('organizationName', '').lower()]
    
    if filtered:
        text = f"🏢 Найдено: {len(filtered)}\n\n"
        for app in filtered[:5]:
            text += f"👤 {app.get('fullName', '-')}\n🏢 {app.get('organizationName', '-')}\n\n"
        bot.send_message(chat_id, text)
    else:
        bot.send_message(chat_id, "❌ Не найдено")
    
    set_state(user_id, 'main_menu')

@bot.message_handler(func=lambda msg: get_context(msg.from_user.id).get('state') == 'search_id')
def search_by_id(message):
    user_id = message.from_user.id
    chat_id = message.chat.id
    app_id = message.text.strip()
    
    app = call_api("GET", f"api/applications/{app_id}")
    
    if app and isinstance(app, dict) and 'id' in app:
        status_map = {True: "✅ Завершена", False: "⏳ В работе", None: "⚪ Новая"}
        text = f"""🔍 Найдена заявка:

🆔 {app.get('id', '?')}
👤 {app.get('fullName', '-')}
📞 {app.get('phoneNumber', '-')}
📧 {app.get('email', '-')}
🏢 {app.get('organizationName', '-')}
📊 {status_map.get(app.get('status'), '?')}"""
        bot.send_message(chat_id, text)
    else:
        bot.send_message(chat_id, "❌ Заявка не найдена")
    
    set_state(user_id, 'main_menu')

# ==================== COMMANDS ====================

@bot.message_handler(commands=['start', 'menu'])
def cmd_start(message):
    user_id = message.from_user.id
    chat_id = message.chat.id
    
    set_state(user_id, 'main_menu')
    bot.send_message(chat_id, "🏠 *АДМИН ПАНЕЛЬ*\n\nВыберите модуль:", 
                    reply_markup=main_menu(), parse_mode="Markdown")

# ==================== BUTTONS ====================

@bot.message_handler(func=lambda msg: "📦" in msg.text)
def btn_applications(message):
    user_id = message.from_user.id
    chat_id = message.chat.id
    
    set_state(user_id, 'apps_menu')
    bot.send_message(chat_id, "📦 *ЗАЯВКИ*\n\nФильтр:", 
                    reply_markup=applications_filter_menu(), parse_mode="Markdown")

@bot.message_handler(func=lambda msg: "🏷" in msg.text)
def btn_spheres(message):
    user_id = message.from_user.id
    chat_id = message.chat.id
    
    set_state(user_id, 'spheres_menu')
    bot.send_message(chat_id, "🏷 *СФЕРЫ*\n\nДействие:", 
                    reply_markup=reference_menu("sphere"), parse_mode="Markdown")

@bot.message_handler(func=lambda msg: "🔧" in msg.text)
def btn_types(message):
    user_id = message.from_user.id
    chat_id = message.chat.id
    
    set_state(user_id, 'types_menu')
    bot.send_message(chat_id, "🔧 *ВИДЫ*\n\nДействие:", 
                    reply_markup=reference_menu("type"), parse_mode="Markdown")

@bot.message_handler(func=lambda msg: "💰" in msg.text)
def btn_tariffs(message):
    user_id = message.from_user.id
    chat_id = message.chat.id
    
    set_state(user_id, 'tariffs_menu')
    bot.send_message(chat_id, "💰 *ТАРИФЫ*\n\nДействие:", 
                    reply_markup=reference_menu("tariff"), parse_mode="Markdown")

@bot.message_handler(func=lambda msg: "✅" in msg.text)
def btn_solutions(message):
    user_id = message.from_user.id
    chat_id = message.chat.id
    
    set_state(user_id, 'solutions_menu')
    solutions = call_api("GET", "api/solution")
    
    if solutions and isinstance(solutions, list) and solutions:
        text = "✅ *РЕШЕНИЯ:*\n\n"
        for sol in solutions[:5]:
            text += f"📋 {sol.get('description', '-')[:50]}\n"
        bot.send_message(chat_id, text, parse_mode="Markdown")
    else:
        bot.send_message(chat_id, "❌ Нет решений")

@bot.message_handler(func=lambda msg: "📊" in msg.text)
def btn_search(message):
    user_id = message.from_user.id
    chat_id = message.chat.id
    
    set_state(user_id, 'search_menu')
    bot.send_message(chat_id, "📊 *ПОИСК*\n\nПо чему?", 
                    reply_markup=search_menu(), parse_mode="Markdown")

# ==================== CALLBACKS ====================

@bot.callback_query_handler(func=lambda call: call.data.startswith("app_filter_"))
def cb_app_filter(call):
    user_id = call.from_user.id
    chat_id = call.message.chat.id
    msg_id = call.message.message_id
    filter_type = call.data.replace("app_filter_", "")
    
    if filter_type == "cancel":
        set_state(user_id, 'main_menu')
        cmd_start(call.message)
        return
    
    apps = call_api("GET", "api/applications")
    
    if not apps:
        bot.edit_message_text("❌ Нет заявок", chat_id, msg_id)
        bot.answer_callback_query(call.id)
        return
    
    if filter_type == "new":
        filtered = [a for a in apps if a.get('status') is None]
        title = "⚪ НОВЫЕ"
    elif filter_type == "work":
        filtered = [a for a in apps if a.get('status') is False]
        title = "⏳ В РАБОТЕ"
    elif filter_type == "done":
        filtered = [a for a in apps if a.get('status') is True]
        title = "✅ ЗАВЕРШЕНЫ"
    else:
        filtered = apps
        title = "📋 ВСЕ"
    
    if not filtered:
        bot.edit_message_text(f"{title}\n\n❌ Нет", chat_id, msg_id)
        bot.answer_callback_query(call.id)
        return
    
    ctx = get_context(user_id)
    ctx['apps_list'] = filtered
    ctx['current_app_index'] = 0
    
    app = filtered[0]
    status_map = {True: "✅", False: "⏳", None: "⚪"}
    
    text = f"""{title}

🆔 {str(app.get('id', '?'))[:8]}
👤 {app.get('fullName', '-')}
📞 {app.get('phoneNumber', '-')}
📧 {app.get('email', '-')}
🏢 {app.get('organizationName', '-')}
📊 {status_map.get(app.get('status'), '?')}

1/{len(filtered)}"""
    
    bot.edit_message_text(text, chat_id, msg_id)
    bot.answer_callback_query(call.id)

# SPHERE CALLBACKS
@bot.callback_query_handler(func=lambda call: call.data.startswith("sphere_view_"))
def cb_sphere_view(call):
    chat_id = call.message.chat.id
    msg_id = call.message.message_id
    
    spheres = call_api("GET", "api/sphereActivity")
    
    if not spheres or not isinstance(spheres, list):
        bot.edit_message_text("❌ Нет", chat_id, msg_id)
        bot.answer_callback_query(call.id)
        return
    
    text = "🏷 СФЕРЫ:\n\n"
    for i, s in enumerate(spheres[:10], 1):
        name = s.get('nameSphere', '-')
        if name and name != 'string':  # Filter out bad data
            text += f"{i}. {name}\n"
    
    bot.edit_message_text(text, chat_id, msg_id)
    bot.answer_callback_query(call.id)

@bot.callback_query_handler(func=lambda call: call.data == "sphere_create_start")
def cb_sphere_create(call):
    user_id = call.from_user.id
    chat_id = call.message.chat.id
    msg_id = call.message.message_id
    
    set_state(user_id, 'sphere_create')
    bot.delete_message(chat_id, msg_id)
    bot.send_message(chat_id, "📝 Название сферы:")

# TYPE CALLBACKS
@bot.callback_query_handler(func=lambda call: call.data.startswith("type_view_"))
def cb_type_view(call):
    chat_id = call.message.chat.id
    msg_id = call.message.message_id
    
    types_list = call_api("GET", "api/typeActivity")
    
    if not types_list or not isinstance(types_list, list):
        bot.edit_message_text("❌ Нет", chat_id, msg_id)
        bot.answer_callback_query(call.id)
        return
    
    text = "🔧 ВИДЫ:\n\n"
    for i, t in enumerate(types_list[:10], 1):
        name = t.get('nameType', '-')
        if name and name != 'string':
            text += f"{i}. {name}\n"
    
    bot.edit_message_text(text, chat_id, msg_id)
    bot.answer_callback_query(call.id)

@bot.callback_query_handler(func=lambda call: call.data == "type_create_start")
def cb_type_create(call):
    user_id = call.from_user.id
    chat_id = call.message.chat.id
    msg_id = call.message.message_id
    
    set_state(user_id, 'type_create')
    bot.delete_message(chat_id, msg_id)
    bot.send_message(chat_id, "📝 Название вида:")

# TARIFF CALLBACKS
@bot.callback_query_handler(func=lambda call: call.data.startswith("tariff_view_"))
def cb_tariff_view(call):
    chat_id = call.message.chat.id
    msg_id = call.message.message_id
    
    tariffs = call_api("GET", "api/tarif")
    
    if not tariffs or not isinstance(tariffs, list):
        bot.edit_message_text("❌ Нет", chat_id, msg_id)
        bot.answer_callback_query(call.id)
        return
    
    text = "💰 ТАРИФЫ:\n\n"
    for i, t in enumerate(tariffs[:10], 1):
        name = t.get('name', '-')
        price = t.get('price', 0)
        desc = t.get('description', '')
        
        # Filter out bad data (string, max int)
        if name and name != 'string' and price < 2000000000:
            text += f"{i}. {name} - {price}₽\n"
            if desc and desc != 'string':
                text += f"   _{desc[:40]}_\n"
            text += "\n"
    
    bot.edit_message_text(text, chat_id, msg_id)
    bot.answer_callback_query(call.id)

@bot.callback_query_handler(func=lambda call: call.data == "tariff_create_start")
def cb_tariff_create(call):
    user_id = call.from_user.id
    chat_id = call.message.chat.id
    msg_id = call.message.message_id
    
    set_state(user_id, 'tariff_name')
    bot.delete_message(chat_id, msg_id)
    bot.send_message(chat_id, "📝 Название тариф:")

# SEARCH CALLBACKS
@bot.callback_query_handler(func=lambda call: call.data == "search_by_phone")
def cb_search_phone(call):
    user_id = call.from_user.id
    chat_id = call.message.chat.id
    msg_id = call.message.message_id
    
    set_state(user_id, 'search_phone')
    bot.delete_message(chat_id, msg_id)
    bot.send_message(chat_id, "📱 Номер телефона:")

@bot.callback_query_handler(func=lambda call: call.data == "search_by_email")
def cb_search_email(call):
    user_id = call.from_user.id
    chat_id = call.message.chat.id
    msg_id = call.message.message_id
    
    set_state(user_id, 'search_email')
    bot.delete_message(chat_id, msg_id)
    bot.send_message(chat_id, "📧 Email:")

@bot.callback_query_handler(func=lambda call: call.data == "search_by_org")
def cb_search_org(call):
    user_id = call.from_user.id
    chat_id = call.message.chat.id
    msg_id = call.message.message_id
    
    set_state(user_id, 'search_org')
    bot.delete_message(chat_id, msg_id)
    bot.send_message(chat_id, "🏢 Организация:")

@bot.callback_query_handler(func=lambda call: call.data == "search_by_id")
def cb_search_id(call):
    user_id = call.from_user.id
    chat_id = call.message.chat.id
    msg_id = call.message.message_id
    
    set_state(user_id, 'search_id')
    bot.delete_message(chat_id, msg_id)
    bot.send_message(chat_id, "🔍 ID заявки:")

@bot.callback_query_handler(func=lambda call: call.data == "noop")
def cb_noop(call):
    bot.answer_callback_query(call.id)

# CREATE APP CALLBACK
@bot.callback_query_handler(func=lambda call: call.data.startswith("app_create"))
def cb_app_create(call):
    user_id = call.from_user.id
    chat_id = call.message.chat.id
    msg_id = call.message.message_id
    
    set_state(user_id, 'app_fullName')
    bot.delete_message(chat_id, msg_id)
    bot.send_message(chat_id, "👤 ФИО:")

# ==================== FALLBACK ====================

@bot.message_handler(func=lambda msg: True)
def fallback(message):
    user_id = message.from_user.id
    chat_id = message.chat.id
    
    set_state(user_id, 'main_menu')
    bot.send_message(chat_id, "❓ Команда не найдена\n\nИспользуйте /start")

# ==================== MAIN ====================

if __name__ == "__main__":
    print("\n" + "="*60)
    print("🤖 ПОЛНОФУНКЦИОНАЛЬНЫЙ БОТ V2")
    print("✅ Заявки, Сферы, Виды, Тарифы, Решения, Поиск")
    print("="*60 + "\n")
    
    try:
        bot.infinity_polling(skip_pending=True, interval=0.5)
    except KeyboardInterrupt:
        print("\n🛑 Остановлен", flush=True)
    except Exception as e:
        print(f"\n❌ Ошибка: {e}", flush=True)
        import traceback
        traceback.print_exc()
