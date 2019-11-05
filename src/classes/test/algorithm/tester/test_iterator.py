import pandas as pd

from .position import Position
from ....progress_recorder import TradeProgressBuilder


class TestIteratorState:

    def __init__(self, df, recorders, log_interval=10000):
        self.df = df
        self.index = 0
        self.position = None
        self.indicator_values = None
        self.progress_builder = TradeProgressBuilder(recorders) if recorders else None
        self.log_interval = log_interval

    def entry(self, order_direction):
        self.position = Position(self.df)
        self.position.market_order(self.index, order_direction)
        if self.progress_builder:
            self.progress_builder.entry(self)

    def progress(self):
        if self.position:
            self.position.set_max_profit(self.index)

        if self.progress_builder:
            self.progress_builder.progress(self)

        if self.index % self.log_interval == 0:
            print('progress: {}'.format(self.index))

    def exit(self):
        self.position.take_profit_order(self.index)
        if self.progress_builder:
            self.progress_builder.exit(self)
        self.position = None

    def build(self):
        result = self.progress_builder.build()
        print(result['moment'].describe(include='all'))


class TestIterator:

    def __init__(self, candles_file_path, indicators, recorders, start=-10000, end=-1, window_size=4000):
        df = pd.read_csv(candles_file_path)
        self.df = df.iloc[start:end, :]
        self.window_size = window_size
        self.indicators = indicators
        self.current = 0
        self.test_iterator_state = TestIteratorState(self.df, recorders)

    def __iter__(self):
        return self

    def __next__(self):
        length = len(self.df.index)

        end = self.current + self.window_size
        if end > length:
            self.test_iterator_state.build()
            raise StopIteration()

        df = self.df.iloc[self.current:end, :]
        self.current += 1

        self.test_iterator_state.index = end - 1
        self.test_iterator_state.indicator_values = self.indicators.get_values(df)
        self.test_iterator_state.progress()

        return self.test_iterator_state
