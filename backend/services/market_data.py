import logging
from datetime import datetime

import yfinance as yf

from models.schemas import Fundamentals, MarketDataResponse, PriceCandle, StockInfo

logger = logging.getLogger(__name__)


class MarketDataService:
    """
    Fetches real-time and historical stock data using yfinance.

    This is the foundation all AI agents rely on.
    It is injected into routes via FastAPI's Depends() system
    — meaning FastAPI creates and manages the instance for us,
    we never do MarketDataService() manually in our routes.
    """

    def _get_ticker(self, ticker: str) -> yf.Ticker:
        """
        Private helper — creates a yfinance Ticker object.
        Prefixed with _ to signal 'only used inside this class'.
        """
        return yf.Ticker(ticker.upper())

    def get_stock_info(self, ticker: str) -> StockInfo:
        """
        Fetch basic identity and current price info.
        Returns a typed StockInfo model — not a raw dict.
        """
        try:
            stock = self._get_ticker(ticker)
            info = stock.info
            if not info or len(info.keys()) <= 1:
                raise ValueError(f"Could not fetch data for ticker: {ticker}")

            # yfinance sometimes returns 0 or None for missing fields
            # we use .get(key, default) to safely handle this
            return StockInfo(
                ticker=ticker.upper(),
                name=info.get("longName", "Unknown"),
                sector=info.get("sector", "Unknown"),
                industry=info.get("industry", "Unknown"),
                exchange=info.get("exchange", "Unknown"),
                currency=info.get("currency", "USD"),
                market_cap=info.get("marketCap", 0),
                current_price=info.get("currentPrice", 0.0),
                previous_close=info.get("previousClose", 0.0),
                day_high=info.get("dayHigh", 0.0),
                day_low=info.get("dayLow", 0.0),
                volume=info.get("volume", 0),
                avg_volume=info.get("averageVolume", 0),
                fifty_two_week_high=info.get("fiftyTwoWeekHigh", 0.0),
                fifty_two_week_low=info.get("fiftyTwoWeekLow", 0.0),
            )
        except ValueError:
            raise
        except Exception as e:
            logger.error(f"Error fetching stock info for {ticker}: {e}")
            raise ValueError(f"Could not fetch data for ticker: {ticker}")

    def get_price_history(
        self,
        ticker: str,
        period: str = "6mo",
    ) -> list[PriceCandle]:
        """
        Fetch historical OHLCV price data.
        Returns a typed list of PriceCandle models.

        period options:
            "1mo" = 1 month
            "3mo" = 3 months
            "6mo" = 6 months  ← default
            "1y"  = 1 year
        """
        try:
            stock = self._get_ticker(ticker)
            history = stock.history(period=period)

            if history.empty:
                raise ValueError(f"No price history found for {ticker}")

            # Convert each DataFrame row into a PriceCandle model
            candles = []
            for date, row in history.iterrows():
                trade_date = datetime.strptime(str(date), "%Y-%m-%d %H:%M:%S%z")
                candles.append(
                    PriceCandle(
                        date=trade_date.strftime("%Y-%m-%d"),
                        open=round(float(row["Open"]), 2),
                        high=round(float(row["High"]), 2),
                        low=round(float(row["Low"]), 2),
                        close=round(float(row["Close"]), 2),
                        volume=int(row["Volume"]),
                    )
                )

            return candles

        except Exception as e:
            logger.error(f"Error fetching price history for {ticker}: {e}")
            raise ValueError(f"Could not fetch price history for: {ticker}")

    def get_fundamentals(self, ticker: str) -> Fundamentals:
        """
        Fetch fundamental financial data.
        Returns a typed Fundamentals model.
        """
        try:
            stock = self._get_ticker(ticker)
            info = stock.info

            return Fundamentals(
                pe_ratio=info.get("trailingPE"),
                forward_pe=info.get("forwardPE"),
                eps=info.get("trailingEps"),
                revenue=info.get("totalRevenue"),
                revenue_growth=info.get("revenueGrowth"),
                gross_margins=info.get("grossMargins"),
                profit_margins=info.get("profitMargins"),
                debt_to_equity=info.get("debtToEquity"),
                return_on_equity=info.get("returnOnEquity"),
                free_cashflow=info.get("freeCashflow"),
                dividend_yield=info.get("dividendYield"),
                beta=info.get("beta"),
                shares_outstanding=info.get("sharesOutstanding"),
            )

        except Exception as e:
            logger.error(f"Error fetching fundamentals for {ticker}: {e}")
            raise ValueError(f"Could not fetch fundamentals for: {ticker}")

    def get_full_market_data(
        self,
        ticker: str,
        period: str = "6mo",
    ) -> MarketDataResponse:
        """
        Fetch everything in one call — info, history, fundamentals.
        This is the main method our AI agents will call.
        Returns a fully typed MarketDataResponse.
        """
        return MarketDataResponse(
            ticker=ticker.upper(),
            info=self.get_stock_info(ticker),
            history=self.get_price_history(ticker, period),
            fundamentals=self.get_fundamentals(ticker),
        )


# ── Dependency Injection ───────────────────────────────────────────────
# This function is what FastAPI's Depends() will call.
# FastAPI creates one MarketDataService instance per request
# and injects it into our route handlers automatically.
def get_market_data_service() -> MarketDataService:
    return MarketDataService()
