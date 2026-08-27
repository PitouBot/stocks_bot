from aiogram import Router, F 
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from database import add_stock, get_stocks, remove_stock, remove_all_stocks
from api_moex import get_all_prices
from states import AddStock
from keyboards import main_menu, back_button, remove_stock_keyboard, remove_all_keyboard

router = Router()

# --- Показать цены ---
@router.callback_query(F.data == "show_prices")
async def show_prices(callback: CallbackQuery):
    stocks = get_stocks(callback.from_user.id)
    
    if not stocks:
        await callback.message.edit_text(
            "📭 У тебя пока нет добавленных акций.\n"
            "Нажми «➕ Добавить акцию», чтобы добавить первую.",
            reply_markup=back_button()
        )
        await callback.answer()
        return
    
    prices = await get_all_prices(stocks, callback.bot.my_session)
    
    text = "📊 *Твои акции:*\n\n"
    for ticker in stocks:
        price = prices.get(ticker)
        if price:
            text += f"• {ticker}: `{price:.2f} ₽`\n"
        else:
            text += f"• {ticker}: ⚠️ Ошибка загрузки\n"
    
    await callback.message.edit_text(text, parse_mode="Markdown", reply_markup=back_button())
    await callback.answer()

# --- Добавить акцию (начало) ---
@router.callback_query(F.data == "add_stock")
async def add_stock_start(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        "✏️ Введи тикер акции.\n"
        "Примеры: `SBER`, `OZON`, `YNDX`, `GAZP`\n\n"
        "Тикер можно посмотреть на сайте MOEX или в брокерском приложении.",
        parse_mode="Markdown",
        reply_markup=back_button()
    )
    await state.set_state(AddStock.waiting_for_ticker)
    await callback.answer()

# --- Добавить акцию (ввод тикера) ---
@router.message(AddStock.waiting_for_ticker)
async def add_stock_ticker(message: Message, state: FSMContext):
    ticker = message.text.strip().upper()
    user_id = message.from_user.id

    # 1. Проверяем, есть ли уже такая акция у пользователя
    user_stocks = get_stocks(user_id)
    if ticker in user_stocks:
        await message.answer(
            f"⚠️ Акция `{ticker}` уже есть в твоём списке.",
            parse_mode="Markdown",
            reply_markup=back_button()
        )
        await state.clear()
        return
    
    # Проверяем, существует ли акция
    prices = await get_all_prices([ticker], message.bot.my_session)
    
    if not prices.get(ticker):
        await message.answer(
            f"❌ Тикер `{ticker}` не найден на бирже MOEX.\n"
            "Проверь правильность ввода (например, SBER, OZON).",
            parse_mode="Markdown",
            reply_markup=back_button()
        )
        await state.clear()
        return

    # Добавляем акцию
    add_stock(user_id, ticker)
    await message.answer(
        f"✅ Акция `{ticker}` добавлена!\n"
        f"💰 Текущая цена: `{prices[ticker]:.2f} ₽`",
        parse_mode="Markdown",
        reply_markup=main_menu()
    )
    await state.clear()

# --- Удалить все (подтверждение) ---
@router.callback_query(F.data == "remove_all")
async def remove_all_confirm(callback: CallbackQuery):
    stocks = get_stocks(callback.from_user.id)
    
    if not stocks:
        await callback.message.edit_text(
            "📭 У тебя нет акций для удаления.",
            reply_markup=back_button()
        )
        await callback.answer()
        return
        
    await callback.message.edit_text(
        "⚠️ Ты уверен, что хочешь удалить ВСЕ акции?\n"
        "Это действие нельзя отменить.",
        reply_markup=remove_all_keyboard()
    )
    await callback.answer()

# --- Подтверждение удаления всех ---
@router.callback_query(F.data == "confirm_remove_all")
async def confirm_remove_all(callback: CallbackQuery):
    remove_all_stocks(callback.from_user.id)
    await callback.message.edit_text(
        "🗑️ Все акции удалены.",
        reply_markup=main_menu()
    )
    await callback.answer()

# --- Удалить акцию (список) ---
@router.callback_query(F.data == "remove_stock")
async def remove_stock_start(callback: CallbackQuery):
    stocks = get_stocks(callback.from_user.id)
    
    if not stocks:
        await callback.message.edit_text(
            "📭 У тебя нет акций для удаления.",
            reply_markup=back_button()
        )
        await callback.answer()
        return
    
    await callback.message.edit_text(
        "🗑️ Выбери акцию для удаления:",
        reply_markup=remove_stock_keyboard(stocks)
    )
    await callback.answer()

# --- Удалить конкретную акцию ---
@router.callback_query(F.data.startswith("remove_"))
async def remove_stock_confirm(callback: CallbackQuery):
    ticker = callback.data.replace("remove_", "")
    
    remove_stock(callback.from_user.id, ticker)
    await callback.message.edit_text(
        f"✅ Акция `{ticker}` удалена из списка.",
        parse_mode="Markdown",
        reply_markup=main_menu()
    )
    await callback.answer()
