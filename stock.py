import collections

from row import ParsedRow
from config import Config

class Stock:
  def __init__(self, first_row):
    self.first_row = ParsedRow(first_row)

    self.last_true_range = collections.deque(maxlen=Config.D)
    self.last_d_true_range_sum = 0

  def next_row(self, row):
    row = ParsedRow(row)
    assert(row.permno == self.first_row.permno)
    assert(row.date >= self.first_row.date)
