"""
Health Check Script - Test bot, API, and bot configuration
Run this before starting the bot to verify everything is set up correctly
"""

import sys
import asyncio
import requests
from config import TOKEN, ADMIN_CHAT_ID, API_BASE_URL, API_TIMEOUT
from api_client import client

class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    END = '\033[0m'

def print_status(name: str, status: bool, message: str = ""):
    icon = f"{Colors.GREEN}✅{Colors.END}" if status else f"{Colors.RED}❌{Colors.END}"
    print(f"{icon} {name}: {message}")

def print_section(title: str):
    print(f"\n{Colors.BLUE}{'='*50}{Colors.END}")
    print(f"{Colors.BLUE}{title}{Colors.END}")
    print(f"{Colors.BLUE}{'='*50}{Colors.END}")

async def main():
    print_section("🔍 ЗДОРОВЬЕ БОТА - CHECK")
    
    all_ok = True
    
    # 1. Check Configuration
    print_section("1. Проверка конфигурации")
    
    if TOKEN and TOKEN != "8283611145:AAFfb_ETrxyIZajAxVIQrKr0OgaJAlg2vWw":
        print_status("Telegram Token", True, "Установлен")
    else:
        print_status("Telegram Token", False, "Используется значение по умолчанию! Измените TOKEN в config.py")
        all_ok = False
    
    if ADMIN_CHAT_ID and ADMIN_CHAT_ID != 506698213:
        print_status("Admin Chat ID", True, f"Установлен (ID: {ADMIN_CHAT_ID})")
    else:
        print_status("Admin Chat ID", False, "Используется значение по умолчанию! Измените ADMIN_CHAT_ID в config.py")
        all_ok = False
    
    print_status("API URL", True, f"Установлен ({API_BASE_URL})")
    print_status("API Timeout", True, f"{API_TIMEOUT} сек")
    
    # 2. Check Telegram Bot Token
    print_section("2. Проверка Telegram Bot Token")
    
    try:
        import telebot
        bot = telebot.TeleBot(TOKEN)
        bot_info = bot.get_me()
        print_status("Telegram Bot", True, f"@{bot_info.username} ({bot_info.first_name})")
    except Exception as e:
        print_status("Telegram Bot", False, f"Ошибка: {str(e)}")
        print(f"{Colors.YELLOW}Возможные причины:{Colors.END}")
        print("  - Неверный TOKEN")
        print("  - Нет интернета")
        print("  - Бот заблокирован @BotFather")
        all_ok = False
    
    # 3. Check API Connectivity
    print_section("3. Проверка подключения к API")
    
    try:
        response = requests.get(
            f"{API_BASE_URL}/api/applications",
            timeout=API_TIMEOUT
        )
        print_status("API Доступен", True, f"{API_BASE_URL}")
        print_status("API Ответ", True, f"HTTP {response.status_code}")
    except requests.Timeout:
        print_status("API Доступен", False, f"Timeout ({API_TIMEOUT}s)")
        print(f"{Colors.YELLOW}Решение:{Colors.END}")
        print(f"  - Увеличить API_TIMEOUT в config.py")
        print(f"  - Проверить URL: {API_BASE_URL}")
        all_ok = False
    except requests.ConnectionError:
        print_status("API Доступен", False, f"Невозможно подключиться к {API_BASE_URL}")
        print(f"{Colors.YELLOW}Решение:{Colors.END}")
        print(f"  - Убедиться что API запущен")
        print(f"  - Проверить URL в config.py")
        print(f"  - Проверить firewall")
        all_ok = False
    except Exception as e:
        print_status("API Доступен", False, f"Ошибка: {str(e)}")
        all_ok = False
    
    # 4. Test API Endpoints
    print_section("4. Проверка API endpoints")
    
    endpoints = [
        ("/api/applications", "Заявки"),
        ("/api/sphereActivity", "Сферы деятельности"),
        ("/api/typeActivity", "Виды деятельности"),
        ("/api/tarif", "Тарифы"),
        ("/api/solution", "Решения"),
    ]
    
    for endpoint, name in endpoints:
        try:
            response = requests.get(
                f"{API_BASE_URL}{endpoint}",
                timeout=API_TIMEOUT
            )
            print_status(f"GET {endpoint}", response.status_code == 200, name)
        except Exception as e:
            print_status(f"GET {endpoint}", False, name)
    
    # 5. Test Async API Client
    print_section("5. Проверка Async API Client")
    
    try:
        await client.connect()
        
        apps = await client.get_applications()
        if apps is not None:
            print_status("get_applications()", True, f"Получено {len(apps) if isinstance(apps, list) else 'data'}")
        else:
            print_status("get_applications()", True, "API ответил (нет данных)")
        
        spheres = await client.get_spheres()
        print_status("get_spheres()", True, f"Получено {len(spheres) if isinstance(spheres, list) else 'data'}")
        
        types_list = await client.get_types()
        print_status("get_types()", True, f"Получено {len(types_list) if isinstance(types_list, list) else 'data'}")
        
        tariffs = await client.get_tariffs()
        print_status("get_tariffs()", True, f"Получено {len(tariffs) if isinstance(tariffs, list) else 'data'}")
        
        await client.disconnect()
        
    except Exception as e:
        print_status("Async Client", False, f"Ошибка: {str(e)}")
        all_ok = False
    
    # 6. Summary
    print_section("📊 ИТОГИ")
    
    if all_ok:
        print(f"{Colors.GREEN}✅ ВСЕ ПРОВЕРКИ ПРОЙДЕНЫ! БОТ ГОТОВ К ЗАПУСКУ!{Colors.END}")
        print("\nДля запуска выполните:")
        print(f"{Colors.YELLOW}python bot_extended.py{Colors.END}")
        return 0
    else:
        print(f"{Colors.RED}❌ НАЙДЕНЫ ПРОБЛЕМЫ!{Colors.END}")
        print("\nПожалуйста, исправьте ошибки перед запуском бота.")
        print("\nСм. документацию:")
        print("  - QUICKSTART.md - Быстрый старт")
        print("  - README.md - Подробная информация")
        print("  - DOCUMENTATION.md - Полная документация")
        return 1

if __name__ == "__main__":
    print(f"\n{Colors.BLUE}🔍 Проверка здоровья системы{Colors.END}")
    print(f"Версия Python: {sys.version.split()[0]}")
    
    return_code = asyncio.run(main())
    sys.exit(return_code)
