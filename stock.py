import collections
import datetime
import sys

from row import ParsedRow, ParsedFirstRow
from config import Config
from last_n_high import LastNHigh
import output

class _Transaction:
  def __init__(self, parsed_row, factor, average_true_range, exit_price):
    self.buy_row = parsed_row
    self.buy_factor = factor
    self.average_true_range = average_true_range
    self.exit_price = exit_price
    self.adj_dividents = 0

  def update(self, exit_price, adj_dividents):
    if exit_price > self.exit_price:
      self.exit_price = exit_price
    self.adj_dividents += adj_dividents

  def sell(self, sell_row, sell_factor):
    profit = sell_row.bidlo * sell_factor + self.adj_dividents - self.buy_row.askhi * self.buy_factor
    output.print_trasaction(
        ticker=self.buy_row.ticker,
        comnam=self.buy_row.common_name,
        permno=self.buy_row.permno,
        entrydate=self.buy_row.date,
        entryPRC=self.buy_row.price,
        entryBIDLO=self.buy_row.bidlo,
        entryASKHI=self.buy_row.askhi,
        entryVOL=self.buy_row.volume,
        entryFactor=self.buy_factor,
        exitdate=sell_row.date,
        exitPRC=sell_row.price,
        exitBIDLO=sell_row.bidlo,
        exitASKHI=sell_row.askhi,
        exitVOL=sell_row.volume,
        exitFactor=sell_factor,
        divident=self.adj_dividents,
        PnL=profit)


class Stock:
  _PENDING = 0
  _BUY_TOMORROW = 1
  _BOUGHT = 2
  _SELL_TOMORROW = 3

  def __init__(self, first_row):
    self._permno_str = first_row.permno
    self._first_row = ParsedFirstRow(first_row)
    self._last_row = None

    self._state = Stock._PENDING
    self._transaction = None
    self._factor = 1.0
    self._adj_price = 0

    self._last_true_range = collections.deque(maxlen=Config.D)
    self._last_d_true_range_sum = 0
    self._high_price = LastNHigh(Config.N * 252)
    self._n_time_delta = datetime.timedelta(days=Config.N * 365)

  def same_stock(self, row):
    return self._permno_str == row.permno

  def next_row(self, row):
    row = ParsedRow(row)
    assert(row.permno == self._first_row.permno)
    assert(row.date >= self._first_row.date)
    if not row.parsed:
      return
    self._last_row = row

    self._factor = self._factor * (1.0 + row.facpr)
    adj_price = row.price * self._factor
    adj_ask_high = row.askhi * self._factor
    adj_bid_low = row.bidlo * self._factor

    true_range = max(
      adj_ask_high - adj_bid_low,
      adj_ask_high - self._adj_price,
      self._adj_price - adj_bid_low)
    self._adj_price = adj_price

    if len(self._last_true_range) >= self._last_true_range.maxlen:
      self._last_d_true_range_sum -= self._last_true_range[0]
    self._last_true_range.append(true_range)
    self._last_d_true_range_sum += true_range
    average_true_range =\
        self._last_d_true_range_sum / len(self._last_true_range)
    exit_price = adj_price - average_true_range * Config.M

    high_price = sys.maxint
    if row.date - self._first_row.date >= self._n_time_delta:
      high_price = self._high_price.last_n_high()
    self._high_price.insert(adj_price)

    if self._state == Stock._PENDING:
      if adj_price > high_price and \
          row.exchcd >= Config.EXCHCD_LOW and \
          row.exchcd <= Config.EXCHCD_HIGH and \
          row.price >= Config.P and \
          row.volume >= Config.V:
        self._state = Stock._BUY_TOMORROW
    elif self._state == Stock._BUY_TOMORROW:
      self._transaction = _Transaction(row, self._factor, average_true_range, exit_price)
      self._state = Stock._BOUGHT
    elif self._state == Stock._BOUGHT:
      self._transaction.update(exit_price, self._factor * row.divamt)
      if adj_price <= self._transaction.exit_price:
        self._state = Stock._SELL_TOMORROW
    else:
      assert self._state == Stock._SELL_TOMORROW
      self.done()

  def done(self):
    if self._transaction:
      self._transaction.sell(self._last_row, self._factor)
      self._transaction = None
      self._state = Stock._PENDING
