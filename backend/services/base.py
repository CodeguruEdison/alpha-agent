from abc import ABC, abstractmethod

from models.schemas import Fundamentals, MarketDataResponse, PriceCandle, StockInfo


class MarketDataServiceBase(ABC):
    """
    Interface for all market data services.

    Any class that fetches market data MUST implement
    all these methods. This guarantees our agents always
    get the same data shape regardless of the data source.

    Current implementations:
        - YFinanceService  ← free, no API key needed
        - PolygonService   ← real-time, needs API key (Epic 2.2)
    """

    @abstractmethod
    def get_stock_info(self, ticker: str) -> StockInfo:
        """
        Fetch basic identity and current price info.
        Must return a typed StockInfo model.
        """
        ...

    @abstractmethod
    def get_price_history(self, ticker: str, period: str = "6mo") -> list[PriceCandle]:
        """
        Fetch historical OHLCV price data.
        Must return a typed list of PriceCandle models.
        """
        ...

    @abstractmethod
    def get_fundamentals(self, ticker: str) -> Fundamentals:
        """
        Fetch fundamental financial data.
        Must return a typed Fundamentals model.
        """
        ...

    @abstractmethod
    def get_full_market_data(
        self,
        ticker: str,
        period: str = "6mo",
    ) -> MarketDataResponse:
        """
        Fetch everything in one call.
        Must return a typed MarketDataResponse.
        """
        ...
