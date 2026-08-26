from aiogram import Router, types
from aiogram.filters import Command
from keyboards import main_menu

router = Router()

@router.message(Command("start"))
async def start(message: types.Message):
    await message.answer(
        "🐍💹 Добро пожаловать в Stock Tracker!\n\n"
        "Я помогу тебе следить за ценами акций на Московской бирже.\n"
        "Выбери действие:",
        reply_markup=main_menu()
    )

@router.message(Command("help"))
async def help_command(message: types.Message):
    await message.answer(
        "📖 *Справка по командам:*\n\n"
        "/start — Главное меню\n"
        "/help — Эта справка\n\n"
        "📊 *Кнопки:*\n"
        "• Показать цены — текущие цены твоих акций\n"
        "• Добавить акцию — добавить новую (тикер: SBER, OZON, YNDX)\n"
        "• Удалить акцию — убрать из списка\n"
        "• Удалить все — очистить список\n\n"
        "💰 Данные с задержкой 15 минут (MOEX).",
        parse_mode="Markdown"
    )

@router.callback_query(lambda c: c.data == "back_to_menu")
async def back_to_menu(callback: types.CallbackQuery):
    await callback.message.edit_text(
        "🐍💹 Главное меню:",
        reply_markup=main_menu()
    )
    await callback.answer()