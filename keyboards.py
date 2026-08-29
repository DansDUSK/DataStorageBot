from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

def main_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📝Добавить заметку", callback_data="add_note"),
         InlineKeyboardButton(text="💾Добавить файл", callback_data="add_file")],
        [InlineKeyboardButton(text="🔎Поиск", callback_data="search"),
         InlineKeyboardButton(text="🖨Показать записи", callback_data="get_files_all")],
        [InlineKeyboardButton(text="🗑️ Удалить запись", callback_data="delete_menu")],
        [InlineKeyboardButton(text="✨Статистика", callback_data="stats")],
        [InlineKeyboardButton(text="👀О разработчике", callback_data="about_developer")]
    ])

def get_filess():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📄Показать заметки", callback_data="get_notes")],
        [InlineKeyboardButton(text="📚Показать файлы(по айди профиля)", callback_data="get_files")],
        [InlineKeyboardButton(text="📚Показать файл(по уникальному коду)", callback_data="get_files1")],
        [InlineKeyboardButton(text="🎇Показать все записи", callback_data="all_files")],
        [InlineKeyboardButton(text="🔙 Назад", callback_data="menu")]
    ])
def search_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔎📝Поиск заметок", callback_data="search_note"),
         InlineKeyboardButton(text="🔎💾Поиск файлов", callback_data="search_file")],
        [InlineKeyboardButton(text="🔎🖨Поиск всех данных", callback_data="search_all")],
        [InlineKeyboardButton(text="🔙 Назад", callback_data="menu")]
    ])
def delete_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🗑️ Удалить заметку", callback_data="delete_note")],
        [InlineKeyboardButton(text="🗑️ Удалить файл по ID(уникальный код)", callback_data="delete_file")],
        [InlineKeyboardButton(text="💣 Удалить все данные", callback_data="delete_all")],
        [InlineKeyboardButton(text="🔙 Назад", callback_data="menu")]
    ])

def cancel_menu():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="❌Отмена", callback_data="menu")]
    ])

def cancel_menu2():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔙 Назад", callback_data="menu")]
    ])