import logging

import pandas_ta as ta
import yfinance as yf
from pandas import Series

from models.schemas import MACD, RSI, BollingerBands, TechnicalIndicators

logger = logging.getLogger(__name__)


class TechnicalIndicatorService:
    """
    Calculates technical indicators from historical price data.
    Injected into routes via FastAPI's Depends() system.
    """

    def _get_closing_prices(self, ticker: str) -> Series:
        """
        Private helper — fetches closing prices as a pandas Series.
        All indicators are calculated from closing prices.
        """
        stock = yf.Ticker(ticker.upper())
        history = stock.history(period="6mo")

        if history.empty or len(history) < 2:
            raise ValueError(f"Could not calculate indicators for: {ticker}")

        return history["Close"]

    def get_rsi(self, ticker: str) -> RSI:
        """
        FR1 — Calculate RSI using 14 period (industry standard).
        Returns a typed RSI model with value and signal.
        """
        closes = self._get_closing_prices(ticker)

        # pandas_ta calculates RSI for us
        # period=14 is the industry standard
        rsi_series = ta.rsi(closes, length=14)

        # get the most recent RSI value (last row)
        value = round(float(rsi_series.iloc[-1]), 2)

        # FR1 — determine signal based on value
        if value > 70:
            signal = "overbought"
        elif value < 30:
            signal = "oversold"
        else:
            signal = "neutral"

        return RSI(value=value, signal=signal)

    def get_macd(self, ticker: str) -> MACD:
        """
        FR2 — Calculate MACD using standard periods:
        fast=12, slow=26, signal=9 (industry standard)
        Returns a typed MACD model with signal.
        """
        closes = self._get_closing_prices(ticker)

        # pandas_ta calculates all 3 MACD values at once
        # returns a DataFrame with 3 columns:
        # MACD_12_26_9, MACDh_12_26_9, MACDs_12_26_9
        macd_df = ta.macd(closes, fast=12, slow=26, signal=9)

        # get the most recent values (last row)
        macd_line = round(float(macd_df.iloc[-1, 0]), 2)
        histogram = round(float(macd_df.iloc[-1, 1]), 2)
        signal_line = round(float(macd_df.iloc[-1, 2]), 2)

        # FR2 — determine signal based on crossover
        if macd_line > signal_line:
            signal = "bullish"
        else:
            signal = "bearish"

        return MACD(
            macd_line=macd_line,
            signal_line=signal_line,
            histogram=histogram,
            signal=signal,
        )

    def get_bollinger_bands(self, ticker: str) -> BollingerBands:
        """
        FR3 — Calculate Bollinger Bands using standard periods:
        period=20, std=2 (industry standard)
        Returns a typed BollingerBands model with signal.
        """
        closes = self._get_closing_prices(ticker)

        # pandas_ta calculates all 3 bands at once
        # returns a DataFrame with 3 columns:
        # BBL_20_2.0 (lower), BBM_20_2.0 (middle), BBU_20_2.0 (upper)
        bb_df = ta.bbands(closes, length=20, std=2)

        # get the most recent values (last row)
        lower_band = round(float(bb_df.iloc[-1, 0]), 2)
        middle_band = round(float(bb_df.iloc[-1, 1]), 2)
        upper_band = round(float(bb_df.iloc[-1, 2]), 2)

        # get current price to determine signal
        current_price = float(closes.iloc[-1])

        # FR3 — determine signal based on where price is
        if current_price >= upper_band:
            signal = "overbought"
        elif current_price <= lower_band:
            signal = "oversold"
        else:
            signal = "neutral"

        return BollingerBands(
            upper_band=upper_band,
            middle_band=middle_band,
            lower_band=lower_band,
            signal=signal,
        )

    def get_technical_indicators(self, ticker: str) -> TechnicalIndicators:
        """
        FR4 — fetch all 3 indicators in one call.
        This is the main method our AI agents will call.
        """
        return TechnicalIndicators(
            ticker=ticker.upper(),
            rsi=self.get_rsi(ticker),
            macd=self.get_macd(ticker),
            bollinger=self.get_bollinger_bands(ticker),
        )


# ── Dependency Injection ───────────────────────────────────────────────
# FastAPI calls this function and injects the result into our routes
# via Depends(get_technical_indicator_service)
def get_technical_indicator_service() -> TechnicalIndicatorService:
    return TechnicalIndicatorService()
