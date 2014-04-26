import collections

from row import ParsedRow, ParsedFirstRow
from config import Config

class Stock:
  def __init__(self, first_row):
    self._permno_str = first_row.permno
    self._first_row = ParsedFirstRow(first_row)
    self._factor = 1.0

    self.last_true_range = collections.deque(maxlen=Config.D)
    self.last_d_true_range_sum = 0

  def same_stock(self, row):
    return self._permno_str == row.permno

  def next_row(self, row):
    row = ParsedRow(row)
    assert(row.permno == self._first_row.permno)
    assert(row.date >= self._first_row.date)
    if not row.parsed:
      return

    self._factor = self._factor * (1.0 + row.facpr)

  def done(self):
    print self._permno_str, self._factor
