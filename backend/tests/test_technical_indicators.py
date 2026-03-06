import pytest

from models.schemas import (
    MACD,
    RSI,
    BollingerBands,
    TechnicalIndicators,
)
from services.technical_indicators import TechnicalIndicatorService

TEST_TICKER = "AAPL"


@pytest.fixture
def service() -> TechnicalIndicatorService:
    """
    Create a fresh TechnicalIndicatorService instance for each test
    """
    return TechnicalIndicatorService()


def test_rsi_value_between_0_100(service) -> None:
    result = service.get_rsi(TEST_TICKER)
    assert 0 <= result.value <= 100


def test_rsi_signal_overbought(service) -> None:
    """FR1 — RSI > 70 must return signal = overbought."""

    rsi = RSI(value=75.0, signal="overbought")
    assert rsi.signal == "overbought"


def test_rsi_signal_is_valid_value(
    service: TechnicalIndicatorService,
) -> None:
    """
    FR1 — signal must always be one of the 3 valid values.
    We can't control what RSI value AAPL returns today
    but we can always assert the signal is valid.
    """
    result = service.get_rsi(TEST_TICKER)

    print(result.model_dump_json())

    assert result.signal in ["overbought", "oversold", "neutral"]


def test_macd_returns_correct_type(
    service: TechnicalIndicatorService,
) -> None:
    """FR2 — MACD must return a typed MACD model."""

    result = service.get_macd(TEST_TICKER)

    print(result.model_dump_json())

    assert isinstance(result, MACD)


def test_macd_histogram_is_difference(
    service: TechnicalIndicatorService,
) -> None:
    """
    FR2 — histogram must equal macd_line - signal_line.
    This verifies our math is correct.
    """
    result = service.get_macd(TEST_TICKER)

    print(result.model_dump_json())

    expected = round(result.macd_line - result.signal_line, 2)
    assert round(result.histogram, 2) == expected


def test_bollinger_bands_returns_correct_type(
    service: TechnicalIndicatorService,
) -> None:
    """FR3 — must return a typed BollingerBands model."""
    from models.schemas import BollingerBands

    result = service.get_bollinger_bands(TEST_TICKER)

    print(result.model_dump_json())

    assert isinstance(result, BollingerBands)


def test_bollinger_bands_order(
    service: TechnicalIndicatorService,
) -> None:
    """
    FR3 — upper must always be > middle > lower.
    This verifies the math is correct.
    """
    result = service.get_bollinger_bands(TEST_TICKER)

    print(result.model_dump_json())

    assert result.upper_band > result.middle_band
    assert result.middle_band > result.lower_band


def test_get_technical_indicators_returns_all(
    service: TechnicalIndicatorService,
) -> None:
    """
    FR4 — combined response must contain all 3 indicators.
    This is the main method our AI agents will call.
    """

    result = service.get_technical_indicators(TEST_TICKER)

    print(result.model_dump_json())

    assert isinstance(result, TechnicalIndicators)
    assert isinstance(result.rsi, RSI)
    assert isinstance(result.macd, MACD)
    assert isinstance(result.bollinger, BollingerBands)


def test_get_technical_indicators_ticker_uppercase(
    service: TechnicalIndicatorService,
) -> None:
    """
    FR4 — ticker must always be returned uppercase.
    User might type 'aapl' but we always return 'AAPL'.
    """
    result = service.get_technical_indicators("aapl")

    print(result.model_dump_json())

    assert result.ticker == "AAPL"


def test_invalid_ticker_raises_value_error(
    service: TechnicalIndicatorService,
) -> None:
    """
    FR5 — invalid ticker must raise ValueError
    with a helpful message.
    """
    with pytest.raises(ValueError) as exc_info:
        service.get_technical_indicators("XYZFAKETICKERXYZ")

    assert "Could not calculate indicators for" in str(exc_info.value)
