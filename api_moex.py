import aiohttp
import asyncio
import logging

logger = logging.getLogger(__name__)

async def get_stock_price(ticker: str, session: aiohttp.ClientSession):
    """Асинхронно получает текущую цену акции с MOEX."""

    url = f"https://iss.moex.com/iss/engines/stock/markets/shares/boards/tqbr/securities/{ticker}.json"
    
    try:
        async with session.get(url, timeout=10) as response:
            data = await response.json()
            
            market_data = data.get('marketdata', {}).get('data', [])
            if not market_data:
                return None
            
            price = market_data[0][12]  # Цена в 12-м столбце
            return float(price) if price else None
    
    except asyncio.TimeoutError:
        logger.error(f"Таймаут при запросе {ticker}")
        return None
    except Exception as e:
        logger.error(f"Ошибка получения {ticker}: {e}")
        return None


async def get_all_prices(tickers: list, session: aiohttp.ClientSession):
    """Асинхронно получает цены для списка тикеров."""
    
    tasks = [get_stock_price(session, ticker) for ticker in tickers]
    results = await asyncio.gather(*tasks)
    
    # Собираем словарь {тикер: цена}
    return dict(zip(tickers, results))