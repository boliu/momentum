import collections
import datetime
import sys

from row import ParsedRow, ParsedFirstRow
from config import Config
from last_n_high import LastNHigh

class _Transaction:
  def __init__(self, parsed_row, factor, average_true_range):
    self.buy_row = parsed_row
    self.buy_factor = factor
    self.average_true_range = average_true_range

  def exit_price(self):
    return self.average_true_range * Config.M

  def sell(self, sell_row, sell_factor):
    print self.buy_row.price * self.buy_factor, '->',\
            sell_row.price * sell_factor

class Stock:
  _PENDING = 0
  _BUY_TOMORROW = 1
  _BOUGHT = 2
  _SELL_TOMORROW = 3

  def __init__(self, first_row):
    self._permno_str = first_row.permno
    self._first_row = ParsedFirstRow(first_row)

    self._state = Stock._PENDING
    self._buy = None
    self._factor = 1.0
    self._adj_price = 0

    self._last_true_range = collections.deque(maxlen=Config.D)
    self._last_d_true_range_sum = 0
    self._high_price = LastNHigh(Config.N * 365)
    self._n_time_delta = datetime.timedelta(days=Config.N * 365)

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
    average_true_range =\
        self._last_d_true_range_sum / len(self._last_true_range)

    high_price = sys.maxint
    if row.date - self._first_row.date >= self._n_time_delta:
      high_price = self._high_price.last_n_high()
    self._high_price.insert(adj_price)

    if self._state == Stock._PENDING:
      if adj_price > high_price:
        self._state = Stock._BUY_TOMORROW
    elif self._state == Stock._BUY_TOMORROW:
      self._buy = _Transaction(row, self._factor, average_true_range)
      self._state = Stock._BOUGHT
    elif self._state == Stock._BOUGHT:
      if average_true_range > self._buy.average_true_range:
        self._buy.average_true_range = average_true_range
      if adj_price <= self._buy.exit_price():
        self._state = Stock._SELL_TOMORROW
    else:
      assert self._state == Stock._SELL_TOMORROW
      self._buy.sell(row, self._factor)
      self._buy = None
      self._state = Stock._PENDING

  def done(self):
    print self._permno_str, self._factor
