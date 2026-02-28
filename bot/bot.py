import telebot
from fastapi import FastAPI
from pydantic import BaseModel
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
import threading

TOKEN = "8283611145:AAFfb_ETrxyIZajAxVIQrKr0OgaJAlg2vWw"
CHAT_ID = "506698213"

bot = telebot.TeleBot(TOKEN)
app = FastAPI()

# -----------------------
# Модель данных
# -----------------------

class FormData(BaseModel):
    name: str
    phone: str


# -----------------------
# Хранилище заявок
# -----------------------

applications = []
app_counter = 1

user_state = {}   # хранит текущее меню пользователя


# -----------------------
# Клавиатуры
# -----------------------

def main_menu():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(
        KeyboardButton("📁 Заявки"),
        KeyboardButton("📊 Статистика")
    )
    return kb


def applications_menu():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(
        KeyboardButton("📋 Все заявки"),
        KeyboardButton("⏳ В ожидании")
    )
    kb.add(
        KeyboardButton("✅ Принятые"),
        KeyboardButton("❌ Отклонённые")
    )
    kb.add(KeyboardButton("⬅️ Назад"))
    return kb


# -----------------------
# API приёма заявок
# -----------------------

@app.post("/send")
def send_form(data: FormData):
    global app_counter

    application = {
        "id": app_counter,
        "name": data.name,
        "phone": data.phone,
        "status": "⏳ В ожидании"
    }

    applications.append(application)
    app_counter += 1

    text = (
        f"📩 Новая заявка #{application['id']}\n"
        f"👤 {application['name']}\n"
        f"📞 {application['phone']}\n"
        f"📌 {application['status']}"
    )

    bot.send_message(CHAT_ID, text)
    return {"status": "ok", "id": application["id"]}


# -----------------------
# Старт
# -----------------------

@bot.message_handler(commands=["start"])
def start(message):
    user_state[message.chat.id] = "main"
    bot.send_message(
        message.chat.id,
        "🏠 Главное меню",
        reply_markup=main_menu()
    )


# -----------------------
# Обработка сообщений
# -----------------------

@bot.message_handler(func=lambda message: True)
def handler(message):
    chat_id = message.chat.id
    text = message.text
    state = user_state.get(chat_id, "main")

    # -------- ГЛАВНОЕ МЕНЮ --------
    if state == "main":
        if text == "📁 Заявки":
            user_state[chat_id] = "apps"
            bot.send_message(chat_id, "📁 Раздел: Заявки", reply_markup=applications_menu())

        elif text == "📊 Статистика":
            show_stats(chat_id)

    # -------- МЕНЮ ЗАЯВОК --------
    elif state == "apps":
        if text == "📋 Все заявки":
            show_list(chat_id, "all")

        elif text == "⏳ В ожидании":
            show_list(chat_id, "pending")

        elif text == "✅ Принятые":
            show_list(chat_id, "approved")

        elif text == "❌ Отклонённые":
            show_list(chat_id, "rejected")

        elif text == "⬅️ Назад":
            user_state[chat_id] = "main"
            bot.send_message(chat_id, "🏠 Главное меню", reply_markup=main_menu())


# -----------------------
# Вывод заявок
# -----------------------

def show_list(chat_id, mode):
    if mode == "all":
        filtered = applications
    else:
        status_map = {
            "pending": "⏳ В ожидании",
            "approved": "✅ Принята",
            "rejected": "❌ Отклонена"
        }
        filtered = [a for a in applications if a["status"] == status_map[mode]]

    if not filtered:
        bot.send_message(chat_id, "❗ Заявок нет")
        return

    for app_item in filtered:
        text = (
            f"#{app_item['id']} | {app_item['name']}\n"
            f"📞 {app_item['phone']}\n"
            f"🏷 {app_item['sphere']}\n"
            f"📌 {app_item['status']}"
        )

        keyboard = InlineKeyboardMarkup()
        keyboard.add(
            InlineKeyboardButton("✅ Принять", callback_data=f"approve_{app_item['id']}"),
            InlineKeyboardButton("❌ Отклонить", callback_data=f"reject_{app_item['id']}")
        )

        bot.send_message(chat_id, text, reply_markup=keyboard)


# -----------------------
# Статистика
# -----------------------

def show_stats(chat_id):
    total = len(applications)
    pending = len([a for a in applications if a["status"] == "⏳ В ожидании"])
    approved = len([a for a in applications if a["status"] == "✅ Принята"])
    rejected = len([a for a in applications if a["status"] == "❌ Отклонена"])

    text = (
        f"📊 Статистика:\n\n"
        f"Всего: {total}\n"
        f"⏳ В ожидании: {pending}\n"
        f"✅ Принятые: {approved}\n"
        f"❌ Отклонённые: {rejected}"
    )

    bot.send_message(chat_id, text)


# -----------------------
# Inline кнопки
# -----------------------

@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    if call.data.startswith("approve_"):
        app_id = int(call.data.split("_")[1])
        update_status(app_id, "✅ Принята")
        bot.answer_callback_query(call.id, "Заявка принята")

    elif call.data.startswith("reject_"):
        app_id = int(call.data.split("_")[1])
        update_status(app_id, "❌ Отклонена")
        bot.answer_callback_query(call.id, "Заявка отклонена")

    bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)


def update_status(app_id, new_status):
    for app_item in applications:
        if app_item["id"] == app_id:
            app_item["status"] = new_status
            break


# -----------------------
# Запуск
# -----------------------

def run_bot():
    try:
        bot.infinity_polling(timeout=10, long_polling_timeout=5)
    except Exception as e:
        print("Bot stopped:", e)

thread = threading.Thread(target=run_bot, daemon=True)
thread.start()

