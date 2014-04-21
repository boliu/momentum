import collections
import time

class LastNHigh:
  def __init__(self, n):
    self._place = 0
    self._n = n
    self._deque = collections.deque(maxlen=n)

  def insert(self, new_value):
    if self._deque and self._deque[0][0] + self._n <= self._place:
      self._deque.popleft()

    while self._deque:
      (place, value) = self._deque[-1]
      if value <= new_value:
        self._deque.pop()
      else:
        break

    self._deque.append((self._place, new_value,))
    self._place = self._place + 1

  def last_n_high(self):
    return self._deque[0][1]


def test_basic():
  last_n_high = LastNHigh(5)
  for x in range(1,6):
    last_n_high.insert(x)
    assert last_n_high.last_n_high() == x

  for x in range(1,5):
    last_n_high.insert(5 - x)
    assert last_n_high.last_n_high() == 5

  for x in range(1,5):
    last_n_high.insert(1)
    assert last_n_high.last_n_high() == (5 - x)


def test_worst_case():
  start = time.clock()
  n = 10000
  last_n_high = LastNHigh(n)
  for x in xrange(n, 0, -1):
    sign = 1 - (x % 2) * 2
    last_n_high.insert(sign * x)

  for x in xrange(n, 0, -1):
    if x % 2 == 1:
      x = x - 1
    assert last_n_high.last_n_high() == x
    last_n_high.insert(0)

  duration = time.clock() - start
  print duration

if __name__ == '__main__':
  test_basic()
  test_worst_case()
