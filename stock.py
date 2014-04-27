import collections

from row import ParsedRow, ParsedFirstRow
from config import Config

class Stock:
  _PENDING = 0
  _BUY_TOMORROW = 1
  _BOUGHT = 2
  _SELL_TOMORROW = 3

  def __init__(self, first_row):
    self._permno_str = first_row.permno
    self._first_row = ParsedFirstRow(first_row)

    self._factor = 1.0
    self._adj_price = 0

    self._last_true_range = collections.deque(maxlen=Config.D)
    self._last_d_true_range_sum = 0

  def same_stock(self, row):
    return self._permno_str == row.permno

  def next_row(self, row):
    row = ParsedRow(row)
    assert(row.permno == self._first_row.permno)
    assert(row.date >= self._first_row.date)
    if not row.parsed:
      return

    self._factor = self._factor * (1.0 + row.facpr)
    adj_price = row.price * self._factor
    adj_ask_high = row.askhi * self._factor
    adj_bid_low = row.bidlo * self._factor

    true_range = max(
      adj_price - self._adj_price,
      adj_ask_high - self._adj_price,
      self._adj_price - adj_bid_low)
    self._adj_price = adj_price

    if len(self._last_true_range) >= self._last_true_range.maxlen:
      self._last_d_true_range_sum -= self._last_true_range[0]
    self._last_true_range.append(true_range)
    self._last_d_true_range_sum += true_range

  def done(self):
    print self._permno_str, self._factor
