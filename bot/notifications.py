"""
Notifications Module - Send notifications about new applications
Supports: New applications, Status changes, etc.
"""

import asyncio
from typing import Optional, Dict, Any
from api_client import client
from config import ADMIN_CHAT_ID, EMOJI
from utils import format_application
import telebot
from datetime import datetime, timedelta

# This would be injected from the main bot
bot: Optional[telebot.TeleBot] = None

def set_bot(bot_instance: telebot.TeleBot):
    """Set bot instance"""
    global bot
    bot = bot_instance


class NotificationManager:
    """Manage notifications for new applications and updates"""
    
    def __init__(self, check_interval: int = 10, history_file: str = "notification_history.json"):
        self.check_interval = check_interval
        self.history_file = history_file
        self.last_app_count = 0
        self.last_solution_count = 0
        self.notified_apps = set()  # Track already notified apps
        self.load_history()
    
    def load_history(self):
        """Load notification history from file"""
        import json
        try:
            with open(self.history_file, 'r') as f:
                data = json.load(f)
                self.notified_apps = set(data.get('notified_apps', []))
        except:
            pass
    
    def save_history(self):
        """Save notification history to file"""
        import json
        try:
            with open(self.history_file, 'w') as f:
                json.dump({
                    'notified_apps': list(self.notified_apps),
                    'last_update': datetime.now().isoformat()
                }, f)
        except:
            pass
    
    async def check_new_applications(self):
        """Check for new applications"""
        try:
            apps = await client.get_applications()
            if not apps:
                return
            
            # Check for new applications (status = None)
            new_apps = [app for app in apps if app.get('status') is None]
            
            for app in new_apps:
                app_id = app.get('id')
                if app_id not in self.notified_apps:
                    await self.send_new_app_notification(app)
                    self.notified_apps.add(app_id)
            
            self.save_history()
            
        except Exception as e:
            print(f"Error checking applications: {e}")
    
    async def send_new_app_notification(self, app: Dict[str, Any]):
        """Send notification about new application"""
        if not bot:
            print("Bot not initialized")
            return
        
        try:
            text = f"""
🆕 *НОВАЯ ЗАЯВКА*

{format_application(app)}

Время уведомления: {datetime.now().strftime('%H:%M:%S')}
"""
            
            # Create inline buttons
            from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
            kb = InlineKeyboardMarkup()
            kb.add(
                InlineKeyboardButton(f"{EMOJI['view']} Посмотреть", callback_data=f"app_detail_{app['id']}"),
                InlineKeyboardButton(f"{EMOJI['edit']} Редактировать", callback_data=f"app_edit_{app['id']}")
            )
            kb.add(
                InlineKeyboardButton(f"{EMOJI['solution']} Выделить решение", callback_data=f"app_solution_{app['id']}")
            )
            
            bot.send_message(
                ADMIN_CHAT_ID,
                text.strip(),
                reply_markup=kb,
                parse_mode="Markdown"
            )
            
        except Exception as e:
            print(f"Error sending notification: {e}")
    
    async def check_status_changes(self):
        """Check for status changes"""
        try:
            apps = await client.get_applications()
            if not apps:
                return
            
            # You can implement status change tracking here
            # For now, just check for completed but not notified
            completed = [app for app in apps if app.get('status') is True]
            
            # Send notifications for recently completed apps
            for app in completed:
                if app.get('created'):
                    # Check if completed recently (within last hour)
                    try:
                        created = datetime.fromisoformat(app['created'].replace('Z', '+00:00'))
                        if datetime.now(created.tzinfo) - created < timedelta(hours=1):
                            app_id = f"completed_{app.get('id')}"
                            if app_id not in self.notified_apps:
                                await self.send_completion_notification(app)
                                self.notified_apps.add(app_id)
                    except:
                        pass
            
            self.save_history()
            
        except Exception as e:
            print(f"Error checking status: {e}")
    
    async def send_completion_notification(self, app: Dict[str, Any]):
        """Send notification about completed application"""
        if not bot:
            return
        
        try:
            text = f"""
✅ *ЗАЯВКА ЗАВЕРШЕНА*

👤 *{app.get('fullName', 'N/A')}*
📞 {app.get('phoneNumber', 'N/A')}

Статус: ✅ Завершена
Дата создания: {app.get('created', 'N/A')}
"""
            
            bot.send_message(ADMIN_CHAT_ID, text.strip(), parse_mode="Markdown")
            
        except Exception as e:
            print(f"Error sending completion notification: {e}")
    
    async def start_monitoring(self):
        """Start monitoring loop"""
        await client.connect()
        
        try:
            while True:
                await asyncio.sleep(self.check_interval)
                await self.check_new_applications()
                await self.check_status_changes()
        except KeyboardInterrupt:
            print("Monitoring stopped")
        finally:
            await client.disconnect()


# Global instance
notification_manager = NotificationManager()


async def start_notification_system(bot_instance: telebot.TeleBot):
    """Start notification system"""
    set_bot(bot_instance)
    # Run in background
    asyncio.create_task(notification_manager.start_monitoring())


# Webhook for receiving notifications from FormAPI
# If FormAPI can send webhooks when new application is created

from typing import Any

async def handle_webhook_new_app(data: Dict[str, Any]):
    """Handle webhook from FormAPI"""
    try:
        app = data.get('application', {})
        if app and app.get('id') not in notification_manager.notified_apps:
            await notification_manager.send_new_app_notification(app)
            notification_manager.notified_apps.add(app.get('id'))
            notification_manager.save_history()
    except Exception as e:
        print(f"Error handling webhook: {e}")


# Example FastAPI integration for webhooks
"""
from fastapi import FastAPI, Request

app = FastAPI()

@app.post("/webhook/new-application")
async def webhook_new_app(request: Request):
    data = await request.json()
    await handle_webhook_new_app(data)
    return {"status": "ok"}

@app.post("/webhook/status-change")
async def webhook_status_change(request: Request):
    data = await request.json()
    # Handle status change
    return {"status": "ok"}

# To integrate with bot:
# from fastapi import FastAPI
# from notifications import app as notification_app
# app.include_router(notification_app.router)
"""
