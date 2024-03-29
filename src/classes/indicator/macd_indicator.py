import logging
from enum import Enum

import talib

from .indicator import AbstractIndicator, IndicatorValue


class MACDIndicatorSign(Enum):
    SEPARATE_MACD_GREATER = 1
    SEPATATE_SIGNAL_GREATER = 2
    BOTH_UNDER_MACD_LESS = 3
    BOTH_UNDER_SIGNAL_LESS = 4
    BOTH_OVER_MACD_GREATER = 5
    BOTH_OVER_SIGNAL_GREATER = 6


class MACDIndicator(AbstractIndicator):

    def __init__(self, fast_period=12, slow_period=26, signal_period=9, is_test=False):
        super().__init__(is_test=is_test)
        self.fast_period = fast_period
        self.slow_period = slow_period
        self.signal_period = signal_period

    def get(self, df):
        macd, signal, _ = talib.MACD(
            df['c'], fastperiod=self.fast_period, slowperiod=self.slow_period, signalperiod=self.signal_period)

        latest_macd = macd.iloc[-1]
        latest_signal = signal.iloc[-1]

        material = dict(macd=macd, signal=signal)

        if latest_macd < 0:
            if latest_signal < 0:
                if latest_macd < latest_signal:
                    indicator_value = IndicatorValue(MACDIndicatorSign.BOTH_UNDER_MACD_LESS.name, material=material)
                else:
                    indicator_value = IndicatorValue(MACDIndicatorSign.BOTH_UNDER_SIGNAL_LESS.name, material=material)
            else:
                indicator_value = IndicatorValue(MACDIndicatorSign.SEPATATE_SIGNAL_GREATER.name, material=material)
        else:
            if latest_signal > 0:
                if latest_macd > latest_signal:
                    indicator_value = IndicatorValue(MACDIndicatorSign.BOTH_OVER_MACD_GREATER.name, material=material)
                else:
                    indicator_value = IndicatorValue(MACDIndicatorSign.BOTH_OVER_SIGNAL_GREATER.name, material=material)
            else:
                indicator_value = IndicatorValue(MACDIndicatorSign.SEPARATE_MACD_GREATER, material=material)

        if not self.is_test:
            logging.info("sign=>%s macd=>%s signal=>%s", indicator_value.value, latest_macd, latest_signal)

        return indicator_value
