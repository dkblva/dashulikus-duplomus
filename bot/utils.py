from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from config import ITEMS_PER_PAGE, MAX_MESSAGE_LENGTH, STATUS_NAMES

def format_application(app: Dict[str, Any]) -> str:
    """Format application data for display"""
    lines = [
        f"🆔 ID: {app.get('id', 'N/A')[:8]}...",
        f"👤 ФИО: {app.get('fullName', 'N/A')}",
        f"📞 Телефон: {app.get('phoneNumber', 'N/A')}",
        f"📧 Email: {app.get('email', 'N/A')}",
        f"🏢 Организация: {app.get('organizationName', 'N/A')}",
        f"🏷 Сфера: {app.get('sphereName', 'N/A')}",
        f"🔧 Вид: {app.get('typeName', 'N/A')}",
        f"📊 Статус: {STATUS_NAMES.get(app.get('status'), 'Unknown')}",
        f"📅 Дата: {format_date(app.get('created'))}",
        f"💬 Комментарий: {app.get('comment', 'Нет')}",
    ]
    return "\n".join(lines)


def format_date(date_str: Optional[str]) -> str:
    """Format date string"""
    if not date_str:
        return "N/A"
    try:
        dt = datetime.fromisoformat(date_str.replace("Z", "+00:00"))
        return dt.strftime("%d.%m.%Y %H:%M")
    except:
        return date_str


def paginate_items(items: List[Dict], page: int) -> tuple[List[Dict], int]:
    """Get items for current page"""
    total_pages = (len(items) + ITEMS_PER_PAGE - 1) // ITEMS_PER_PAGE
    page = max(0, min(page, total_pages - 1))
    
    start = page * ITEMS_PER_PAGE
    end = start + ITEMS_PER_PAGE
    
    return items[start:end], total_pages


def format_items_list(items: List[Dict], page: int, format_func=None) -> str:
    """Format list of items with pagination info"""
    if not items:
        return "❌ Ничего не найдено"
    
    paginated, total_pages = paginate_items(items, page)
    
    lines = []
    for i, item in enumerate(paginated, 1):
        if format_func:
            line = format_func(item, i)
        else:
            idx = page * ITEMS_PER_PAGE + i
            line = f"{idx}. {item.get('name', item.get('fullName', 'N/A'))}"
        lines.append(line)
    
    if len(items) > ITEMS_PER_PAGE:
        lines.append(f"\n📄 Страница {page + 1}/{total_pages}")
    
    return "\n".join(lines)


def format_short_list(items: List[Dict]) -> str:
    """Format short list (first 5 items)"""
    if not items:
        return "❌ Ничего не найдено"
    
    lines = []
    for i, item in enumerate(items[:5], 1):
        name = item.get('name', item.get('nameSphere', item.get('nameType', 'N/A')))
        if 'price' in item:
            lines.append(f"{i}. {name} - {item['price']}₽")
        else:
            lines.append(f"{i}. {name}")
    
    if len(items) > 5:
        lines.append(f"\n... и еще {len(items) - 5} элементов")
    
    return "\n".join(lines)


def search_by_field(items: List[Dict], field: str, query: str) -> List[Dict]:
    """Search items by field"""
    query = query.lower()
    results = []
    
    for item in items:
        value = str(item.get(field, "")).lower()
        if query in value:
            results.append(item)
    
    return results


def filter_by_status(apps: List[Dict], status: Optional[bool]) -> List[Dict]:
    """Filter applications by status"""
    return [app for app in apps if app.get('status') == status]


def filter_by_date(apps: List[Dict], days: int) -> List[Dict]:
    """Filter applications by date range"""
    cutoff_date = datetime.now() - timedelta(days=days)
    
    results = []
    for app in apps:
        try:
            created = datetime.fromisoformat(app.get('created', '').replace("Z", "+00:00"))
            if created >= cutoff_date:
                results.append(app)
        except:
            pass
    
    return results


def chunk_message(text: str, max_length: int = MAX_MESSAGE_LENGTH) -> List[str]:
    """Split long message into chunks"""
    if len(text) <= max_length:
        return [text]
    
    chunks = []
    lines = text.split("\n")
    current = ""
    
    for line in lines:
        if len(current) + len(line) + 1 <= max_length:
            current += line + "\n"
        else:
            if current:
                chunks.append(current.strip())
            current = line + "\n"
    
    if current:
        chunks.append(current.strip())
    
    return chunks


def error_message(error: str) -> str:
    """Format error message"""
    return f"❌ Ошибка: {error}"


def success_message(text: str) -> str:
    """Format success message"""
    return f"✅ {text}"


def get_user_state_key(user_id: int, key: str) -> str:
    """Get unique state key for user"""
    return f"{user_id}_{key}"


def is_valid_uuid(value: str) -> bool:
    """Check if string is valid UUID"""
    try:
        import uuid
        uuid.UUID(value)
        return True
    except:
        return False


def is_valid_phone(phone: str) -> bool:
    """Check if phone number format is valid"""
    import re
    return bool(re.match(r'^\+?\d{10,15}$', phone.replace(" ", "").replace("-", "")))


def is_valid_email(email: str) -> bool:
    """Check if email format is valid"""
    import re
    return bool(re.match(r'^[^\s@]+@[^\s@]+\.[^\s@]+$', email))


def format_sphere(sphere: Dict) -> str:
    """Format sphere for display"""
    return f"🏷 {sphere.get('nameSphere', 'N/A')}"


def format_type(type_: Dict) -> str:
    """Format type for display"""
    return f"🔧 {type_.get('nameType', 'N/A')}"


def format_tariff(tariff: Dict) -> str:
    """Format tariff for display"""
    return f"💰 {tariff.get('name', 'N/A')} - {tariff.get('price', 0)}₽\n{tariff.get('description', 'N/A')}"


def format_solution(solution: Dict, app: Optional[Dict] = None) -> str:
    """Format solution for display"""
    lines = [
        f"🆔 Решение: {solution.get('id', 'N/A')[:8]}...",
        f"📋 Заявка: {solution.get('idApplication', 'N/A')[:8]}...",
        f"💰 Тариф: {solution.get('tarifName', solution.get('idTarif', 'N/A'))}",
        f"📝 Описание: {solution.get('description', 'N/A')}",
    ]
    if app:
        lines.insert(1, f"👤 Клиент: {app.get('fullName', 'N/A')}")
    return "\n".join(lines)
