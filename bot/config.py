# Configuration and Constants

# API Configuration
API_BASE_URL = "https://localhost:7082"  # Update with your API endpoint
API_TIMEOUT = 10

# Telegram Bot
TOKEN = "7205851013:AAEXLnSQ7y5kmDBVOCvOCmgNvXdMd4fM-Ao"
ADMIN_CHAT_ID = 717971664  # Your admin chat

# Pagination
ITEMS_PER_PAGE = 5
MAX_MESSAGE_LENGTH = 4096

# Status Mappings
STATUS_NAMES = {
    True: "✅ Завершена",
    False: "⏳ В работе",
    None: "⚪ Новая"
}

STATUS_EMOJIS = {
    "completed": "✅",
    "in_progress": "⏳",
    "new": "⚪",
    "cancelled": "❌"
}

# Button Emojis
EMOJI = {
    "applications": "📦",
    "spheres": "🏷",
    "types": "🔧",
    "tariffs": "💰",
    "solutions": "✅",
    "search": "📊",
    "edit": "✏️",
    "delete": "🗑",
    "status": "📝",
    "solution": "💼",
    "back": "⬅️",
    "menu": "🏠",
    "add": "➕",
    "view": "👀",
    "call": "📞",
    "filter": "🔍",
    "new": "🆕",
    "confirm": "✔️",
    "cancel": "❌"
}

# FSM States
class States:
    # Main
    MAIN_MENU = "main_menu"
    
    # Applications
    APPS_MENU = "apps_menu"
    APPS_FILTER = "apps_filter"
    APPS_VIEW = "apps_view"
    APPS_CREATE = "apps_create"
    APPS_EDIT = "apps_edit"
    APPS_EDIT_FIELD = "apps_edit_field"
    APPS_STATUS_CHANGE = "apps_status_change"
    
    # Spheres
    SPHERES_MENU = "spheres_menu"
    SPHERES_VIEW = "spheres_view"
    SPHERES_CREATE = "spheres_create"
    SPHERES_CREATE_NAME = "spheres_create_name"
    SPHERES_EDIT = "spheres_edit"
    SPHERES_EDIT_NAME = "spheres_edit_name"
    
    # Types
    TYPES_MENU = "types_menu"
    TYPES_VIEW = "types_view"
    TYPES_CREATE = "types_create"
    TYPES_CREATE_NAME = "types_create_name"
    TYPES_EDIT = "types_edit"
    TYPES_EDIT_NAME = "types_edit_name"
    
    # Tariffs
    TARIFFS_MENU = "tariffs_menu"
    TARIFFS_VIEW = "tariffs_view"
    TARIFFS_CREATE = "tariffs_create"
    TARIFFS_CREATE_NAME = "tariffs_create_name"
    TARIFFS_CREATE_DESC = "tariffs_create_desc"
    TARIFFS_CREATE_PRICE = "tariffs_create_price"
    TARIFFS_EDIT = "tariffs_edit"
    TARIFFS_EDIT_FIELD = "tariffs_edit_field"
    
    # Solutions
    SOLUTIONS_MENU = "solutions_menu"
    SOLUTIONS_SELECT_APP = "solutions_select_app"
    SOLUTIONS_SELECT_TARIFF = "solutions_select_tariff"
    SOLUTIONS_ENTER_DESC = "solutions_enter_desc"
    SOLUTIONS_VIEW = "solutions_view"
    
    # Search
    SEARCH_MENU = "search_menu"
    SEARCH_BY_ID = "search_by_id"
    SEARCH_BY_PHONE = "search_by_phone"
    SEARCH_BY_EMAIL = "search_by_email"
    SEARCH_BY_ORG = "search_by_org"
    SEARCH_FILTER_DATE = "search_filter_date"
