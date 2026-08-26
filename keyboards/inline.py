from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def main_menu():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📊 Показать цены", callback_data="show_prices")],
        [InlineKeyboardButton(text="➕ Добавить акцию", callback_data="add_stock")],
        [InlineKeyboardButton(text="➖ Удалить акцию", callback_data="remove_stock")],
        [InlineKeyboardButton(text="🗑️ Удалить все", callback_data="remove_all")]
    ])

def back_button():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔙 Назад", callback_data="back_to_menu")]
    ])

def remove_stock_keyboard(stocks: list):
    buttons = [[InlineKeyboardButton(text=f"❌ {ticker}", callback_data=f"remove_{ticker}")] for ticker in stocks]
    buttons.append([InlineKeyboardButton(text="🔙 Назад", callback_data="back_to_menu")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def remove_all_keyboard():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="⚠️ ДА, УДАЛИТЬ ВСЕ", callback_data="confirm_remove_all")],
        [InlineKeyboardButton(text="🔙 Назад", callback_data="back_to_menu")]
    ])