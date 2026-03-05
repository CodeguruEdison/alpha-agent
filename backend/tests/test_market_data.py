import pytest

from models.schemas import Fundamentals, MarketDataResponse, PriceCandle, StockInfo
from services.market_data import MarketDataService

# ------Set up ---------

# We use well known  stable tickers for  tests

TEST_TICKER = "AAPL"


@pytest.fixture
def service() -> MarketDataService:
    """
    Creates a fresh MarketDataService for each test.
    This is dependency injection in tests —
    instead of FastAPI injecting it, pytest does.
    """
    return MarketDataService()


# Test 1  Stock Info ----------


def test_get_stock_info_returns_correct_type(service) -> None:
    """
    Verify get_stock_info returns a StockInfo model
    with real data filled in.
    """
    result = service.get_stock_info(TEST_TICKER)

    assert isinstance(result, StockInfo)

    assert result.ticker == "AAPL"
    assert result.name != ""
    assert result.current_price > 0
    assert result.market_cap > 0


# Test 2 -Price History
def test_get_price_history_returns_candles(service) -> None:
    """
    Verify get_price_history returns a list of PriceCandle models.
    6 months should give us roughly 120-130 candles.
    """
    result = service.get_price_history(TEST_TICKER, period="6mo")

    assert isinstance(result, list)

    assert len(result) > 100

    first_candle = result[0]
    assert isinstance(first_candle, PriceCandle)
    assert first_candle.open > 0
    assert first_candle.close > 0
    assert first_candle.volume > 0

    assert len(first_candle.date) == 10

    assert first_candle.date[4] == "-"

    assert first_candle.date[7] == "-"


# --- Test 3 -- Fundamentals
def test_get_fundamentals_return_correct_type(service) -> None:
    """
    Verify get_fundamentals returns Fundamentals model.
    AAPL always  has P/E and EPS so we assert those exists.
    """
    result = service.get_fundamentals(TEST_TICKER)

    assert isinstance(result, Fundamentals)

    assert result.pe_ratio is not None
    assert result.eps is not None
    assert result.beta is not None


# --- Test 4 --Full Market Data


def test_get_full_market_data_combines_all(service):
    """
    Verify get_full_market_data return a complete
    MarketDataResponse  with all  3 sections populated
    """
    result = service.get_full_market_data(TEST_TICKER)

    assert isinstance(result, MarketDataResponse)
    assert isinstance(result.fundamentals, Fundamentals)
    assert isinstance(result.history, list)


def test_invalid_ticker_raises_error(service) -> None:
    """
    Verify that searching for a fake ticker raises
    a ValueError with a helpful message.
    """
    with pytest.raises(ValueError) as exc_info:
        service.get_stock_info("XYZFAKETICKERXYZ")

    assert "Could not fetch data" in str(exc_info.value)
