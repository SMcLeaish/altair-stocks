from dataclasses import dataclass
from datetime import datetime, timedelta
from functools import cached_property

import altair as alt
import pandas as pd
import polars as pl
import yfinance as yf

from .chart import candlestick, line

TIMEFMT = '%Y-%m-%d'
MONTHS_TITLE = '%b %d %Y'
TODAY = datetime.today().strftime(TIMEFMT)
DAYS_BACK = 10


@dataclass(frozen=True)
class Stock:
    ticker: str
    title: str | None
    start: str | None = TODAY
    end: str | None = None
    interval: str = '5m'

    def _fetch_data(self) -> pd.DataFrame:
        pdf = yf.download(
            self.ticker, start=self.start, end=self.end, interval=self.interval
        )
        if pdf is not None:
            return pdf
        return pd.DataFrame({})

    def _fetch_back(self) -> pd.DataFrame | None:
        days_back = 1
        while days_back < DAYS_BACK:
            pdf = yf.download(
                self.ticker,
                start=datetime.today() - timedelta(days=days_back),
                end=self.end,
                interval=self.interval,
            )
            if pdf is not None and not pdf.empty:
                return pdf
            days_back += 1
        return None

    @cached_property
    def df(self) -> pl.DataFrame:
        pdf = self._fetch_data()
        if pdf.empty:
            pdf = self._fetch_back()
        if pdf is not None:
            pdf.columns = [
                col[0] if isinstance(col, tuple) else col for col in pdf.columns
            ]
            pdf = pdf.reset_index()
            return pl.from_pandas(pdf)
        return pl.DataFrame({})

    @property
    def chart(self) -> alt.LayerChart | alt.Chart:
        if self.interval == '5m':
            df = self.df.with_columns(
                pl.col('Datetime')
                .dt.convert_time_zone(time_zone='America/New_York')
                .alias('Time')
            )
            return candlestick(df, self.title)
        return line(self.df, self.title)

    @classmethod
    def today(cls, ticker: str):
        title_fmt = datetime.today().strftime(MONTHS_TITLE)
        return cls(ticker=ticker, title=f'{ticker} - {title_fmt}')

    @classmethod
    def months(cls, ticker: str, num_months: int):
        end = datetime.today()
        start = end - timedelta(days=num_months * 30)
        start_fmt = start.strftime(TIMEFMT)
        start_title = start.strftime(MONTHS_TITLE)
        end_title = end.strftime(MONTHS_TITLE)
        return cls(
            ticker=ticker,
            title=f'{ticker} {start_title} - {end_title}',
            start=start_fmt,
            end=end.strftime(TIMEFMT),
            interval='1d',
        )

    @classmethod
    def ytd(cls, ticker: str):
        end = datetime.today()
        start = datetime(end.year, 1, 1)
        start_fmt = start.strftime(TIMEFMT)
        return cls(
            ticker=ticker,
            title=f'{ticker} - YTD {end.year}',
            start=start_fmt,
            end=end.strftime(TIMEFMT),
            interval='1d',
        )
