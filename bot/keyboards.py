from telebot.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from config import EMOJI

# ==================== Main Menu ====================

def main_menu():
    """Main admin menu"""
    kb = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    kb.add(
        KeyboardButton(f"{EMOJI['applications']} Заявки"),
        KeyboardButton(f"{EMOJI['spheres']} Сферы"),
    )
    kb.add(
        KeyboardButton(f"{EMOJI['types']} Виды"),
        KeyboardButton(f"{EMOJI['tariffs']} Тарифы"),
    )
    kb.add(
        KeyboardButton(f"{EMOJI['solutions']} Решения"),
        KeyboardButton(f"{EMOJI['search']} Поиск"),
    )
    return kb


# ==================== Applications Menu ====================

def applications_filter_menu():
    """Filter applications by status"""
    kb = InlineKeyboardMarkup()
    kb.add(
        InlineKeyboardButton(f"{EMOJI['new']} Новые", callback_data="app_filter_new"),
        InlineKeyboardButton("⏳ В работе", callback_data="app_filter_work"),
    )
    kb.add(
        InlineKeyboardButton(f"{EMOJI['confirm']} Завершено", callback_data="app_filter_done"),
        InlineKeyboardButton(f"{EMOJI['cancel']} Отмена", callback_data="app_filter_cancel"),
    )
    kb.add(
        InlineKeyboardButton(f"{EMOJI['add']} Создать", callback_data="app_create_start"),
    )
    return kb


def application_actions_menu(app_id: str):
    """Actions for application"""
    kb = InlineKeyboardMarkup()
    kb.add(
        InlineKeyboardButton(f"{EMOJI['edit']} Редактировать", callback_data=f"app_edit_{app_id}"),
        InlineKeyboardButton(f"{EMOJI['status']} Статус", callback_data=f"app_status_{app_id}"),
    )
    kb.add(
        InlineKeyboardButton(f"{EMOJI['solution']} Решение", callback_data=f"app_solution_{app_id}"),
        InlineKeyboardButton(f"{EMOJI['delete']} Удалить", callback_data=f"app_delete_{app_id}"),
    )
    kb.add(
        InlineKeyboardButton(f"{EMOJI['back']} Назад", callback_data="app_back_list"),
    )
    return kb


def application_status_menu(app_id: str):
    """Change application status"""
    kb = InlineKeyboardMarkup()
    kb.add(
        InlineKeyboardButton("⏳ В работе", callback_data=f"app_set_status_{app_id}_work"),
        InlineKeyboardButton(f"{EMOJI['confirm']} Завершено", callback_data=f"app_set_status_{app_id}_done"),
    )
    kb.add(
        InlineKeyboardButton(f"{EMOJI['cancel']} Отменено", callback_data=f"app_set_status_{app_id}_cancel"),
    )
    return kb


def application_edit_menu(app_id: str):
    """Edit application fields"""
    kb = InlineKeyboardMarkup()
    kb.add(
        InlineKeyboardButton("ФИО", callback_data=f"app_edit_field_{app_id}_name"),
        InlineKeyboardButton("📞 Телефон", callback_data=f"app_edit_field_{app_id}_phone"),
    )
    kb.add(
        InlineKeyboardButton("Email", callback_data=f"app_edit_field_{app_id}_email"),
        InlineKeyboardButton("🏢 Организация", callback_data=f"app_edit_field_{app_id}_org"),
    )
    kb.add(
        InlineKeyboardButton(f"{EMOJI['back']} Готово", callback_data=f"app_edit_done_{app_id}"),
    )
    return kb


def confirm_delete_menu(item_type: str, item_id: str):
    """Confirm deletion"""
    kb = InlineKeyboardMarkup()
    kb.add(
        InlineKeyboardButton(f"{EMOJI['confirm']} Удалить", callback_data=f"confirm_delete_{item_type}_{item_id}"),
        InlineKeyboardButton(f"{EMOJI['cancel']} Отмена", callback_data=f"cancel_delete_{item_type}_{item_id}"),
    )
    return kb


# ==================== Spheres/Types/Tariffs Menu ====================

def reference_menu(ref_type: str):
    """Menu for reference books (spheres/types/tariffs)"""
    kb = InlineKeyboardMarkup()
    kb.add(
        InlineKeyboardButton(f"{EMOJI['view']} Просмотр", callback_data=f"{ref_type}_view_0"),
        InlineKeyboardButton(f"{EMOJI['add']} Добавить", callback_data=f"{ref_type}_create_start"),
    )
    return kb


def reference_edit_menu(ref_type: str, item_id: str):
    """Edit reference item"""
    kb = InlineKeyboardMarkup()
    kb.add(
        InlineKeyboardButton(f"{EMOJI['edit']} Редактировать", callback_data=f"{ref_type}_edit_{item_id}"),
        InlineKeyboardButton(f"{EMOJI['delete']} Удалить", callback_data=f"{ref_type}_delete_{item_id}"),
    )
    kb.add(
        InlineKeyboardButton(f"{EMOJI['back']} Назад", callback_data=f"{ref_type}_view_list"),
    )
    return kb


def pagination_menu(ref_type: str, current_page: int, total_pages: int, action: str = "view"):
    """Pagination for lists"""
    kb = InlineKeyboardMarkup()
    
    if current_page > 0:
        kb.add(InlineKeyboardButton("⬅️ Назад", callback_data=f"{ref_type}_{action}_{current_page - 1}"))
    
    kb.add(InlineKeyboardButton(f"📄 {current_page + 1}/{total_pages}", callback_data="noop"))
    
    if current_page < total_pages - 1:
        kb.add(InlineKeyboardButton("Вперед ➡️", callback_data=f"{ref_type}_{action}_{current_page + 1}"))
    
    return kb


# ==================== Tariffs Special Menu ====================

def tariff_edit_menu(tariff_id: str):
    """Edit tariff fields"""
    kb = InlineKeyboardMarkup()
    kb.add(
        InlineKeyboardButton("Название", callback_data=f"tariff_edit_field_{tariff_id}_name"),
        InlineKeyboardButton("📝 Описание", callback_data=f"tariff_edit_field_{tariff_id}_desc"),
    )
    kb.add(
        InlineKeyboardButton("💰 Стоимость", callback_data=f"tariff_edit_field_{tariff_id}_price"),
    )
    kb.add(
        InlineKeyboardButton(f"{EMOJI['back']} Готово", callback_data=f"tariff_edit_done_{tariff_id}"),
    )
    return kb


# ==================== Solutions Menu ====================

def solutions_menu():
    """Solutions menu"""
    kb = InlineKeyboardMarkup()
    kb.add(
        InlineKeyboardButton(f"{EMOJI['add']} Новое решение", callback_data="solution_create_start"),
        InlineKeyboardButton(f"{EMOJI['view']} Просмотр", callback_data="solution_search_start"),
    )
    return kb


def tariff_select_menu(tariffs: list, callback_prefix: str):
    """Select tariff inline"""
    kb = InlineKeyboardMarkup()
    for tariff in tariffs[:10]:  # Max 10 buttons per row
        cb = f"{callback_prefix}_{tariff['id']}"
        text = f"💰 {tariff['name']} ({tariff['price']}₽)"
        kb.add(InlineKeyboardButton(text, callback_data=cb))
    return kb


# ==================== Search Menu ====================

def search_menu():
    """Search options"""
    kb = InlineKeyboardMarkup()
    kb.add(
        InlineKeyboardButton("🔍 По ID", callback_data="search_by_id"),
        InlineKeyboardButton("📞 По телефону", callback_data="search_by_phone"),
    )
    kb.add(
        InlineKeyboardButton("📧 По email", callback_data="search_by_email"),
        InlineKeyboardButton("🏢 По организации", callback_data="search_by_org"),
    )
    kb.add(
        InlineKeyboardButton("📅 По дате", callback_data="search_by_date"),
    )
    return kb


def date_filter_menu():
    """Date filter options"""
    kb = InlineKeyboardMarkup()
    kb.add(
        InlineKeyboardButton("📅 День", callback_data="date_filter_day"),
        InlineKeyboardButton("📅 Неделя", callback_data="date_filter_week"),
    )
    kb.add(
        InlineKeyboardButton("📅 Месяц", callback_data="date_filter_month"),
    )
    return kb


# ==================== Back Button ====================

def back_button(callback: str):
    """Simple back button"""
    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton(f"{EMOJI['back']} Назад", callback_data=callback))
    return kb


def main_menu_button():
    """Return to main menu"""
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(KeyboardButton(f"{EMOJI['menu']} Главное меню"))
    return kb
