from typing import Optional

from pydantic import BaseModel

# Order of models:
# 1. StockInfo          ← company identity + current price
# 2. PriceCandle        ← one day of OHLCV data
# 3. Fundamentals       ← financial health metrics
# 4. MarketDataResponse ← combines all 3 above
# 5. ErrorResponse      ← for when things go wrong


class StockInfo(BaseModel):
    """Basic identity and current price info for a stock."""

    ticker: str
    name: str
    sector: str
    industry: str
    exchange: str
    currency: str
    market_cap: int
    current_price: float
    previous_close: float
    day_high: float
    day_low: float
    volume: int
    avg_volume: int
    fifty_two_week_high: float
    fifty_two_week_low: float


class PriceCandle(BaseModel):
    """
    One single day of price data for a stock.
    OHLCV = Open, High, Low, Close, Volume

    When we fetch 6 months of history we get ~126 of these
    (stocks only trade on weekdays, ~21 trading days per month)
    """

    date: str
    # The 4 key prices of the day
    open: float  # price when market opened   e.g. 862.00
    high: float  # highest price of the day   e.g. 881.20
    low: float  # lowest price of the day    e.g. 858.50
    close: float  # price when market closed   e.g. 875.40
    volume: int  # number of shares traded that day e.g. 120,000


class Fundamentals(BaseModel):
    """
    Financial health metrics for a company.
    These come from the company's financial statements —
    income statement, balance sheet, cash flow statement.

    All fields are Optional because:
    - New companies may not have P/E yet (no earnings)
    - Some companies don't pay dividends
    - Data isn't always available for every stock
    """

    # ── Valuation — is the stock cheap or expensive? ──────────────────
    pe_ratio: float | None = None
    # Price-to-Earnings — how much you pay for $1 of earnings
    # NVDA = 68x means you pay $68 for every $1 of earnings
    # Lower = cheaper, Higher = expensive but maybe high growth
    forward_pe: Optional[float] = None
    # Same as P/E but uses NEXT year's expected earnings
    # If forward P/E < trailing P/E, earnings are expected to grow
    eps: Optional[float] = None
    # Earnings Per Share — profit divided by shares outstanding
    # NVDA EPS = $11.93 means they earned $11.93 per share

    # ── Growth — is the company growing? ─────────────────────────────
    revenue: Optional[int] = None
    # Total sales in dollars — NVDA = $60,900,000,000

    revenue_growth: Optional[float] = None
    # How much revenue grew vs last year — NVDA = 1.22 means +122%

    gross_margins: Optional[float] = None
    # % of revenue kept after cost of goods — NVDA = 0.744 means 74.4%
    # Higher margins = more profitable business model

    profit_margins: Optional[float] = None
    # % of revenue that becomes actual profit — NVDA = 0.559 means 55.9%

    # ── Financial Health — can they survive hard times? ───────────────
    debt_to_equity: Optional[float] = None
    # How much debt vs shareholder equity — lower is safer
    # 0.42 means $0.42 of debt for every $1 of equity

    return_on_equity: Optional[float] = None
    # How efficiently they use shareholder money to generate profit
    # 0.91 means they generate $0.91 profit per $1 of equity — excellent
    free_cashflow: Optional[int] = None
    # Cash left over after all expenses — the real measure of profitability
    # Companies can fake earnings but not cash flow

    # ── Other ─────────────────────────────────────────────────────────
    dividend_yield: Optional[float] = None
    # Annual dividend as % of stock price — 0.03 means 3% yield
    # None means the company doesn't pay dividends (most growth stocks)

    beta: Optional[float] = None
    # How volatile vs the S&P 500 — NVDA beta = 1.48
    # 1.0 = moves same as market
    # 1.48 = moves 48% more than market (more volatile)
    # 0.5 = moves half as much (less volatile, e.g. utilities)

    shares_outstanding: Optional[int] = None
    # Total shares that exist — used to calculate market cap


class MarketDataResponse(BaseModel):
    """
    The complete market data response for a stock.
    This is what our API endpoint returns when called.
    This is also what gets passed to all 7 AI agents.

    Example usage:
        GET /api/market/NVDA
        → returns one MarketDataResponse
    """

    ticker: str  # "NVDA" — repeated for convenience
    info: StockInfo  # current price, name, sector etc
    history: list[PriceCandle]  # 6 months of daily candles
    fundamentals: Fundamentals  # P/E, revenue, margins etc


class ErrorResponse(BaseModel):
    """
    Returned when something goes wrong in the API.
    Instead of crashing with a confusing Python error,
    we return a clean structured error the frontend can display.

    Example — user searches for fake ticker "XYZABC":
    {
        "error": "Ticker not found",
        "detail": "Could not fetch data for ticker: XYZABC"
    }
    """

    error: str  # short error title  — "Ticker not found"
    detail: str  # full explanation   — "Could not fetch data for ticker: XYZABC"
