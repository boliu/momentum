import csv
import io
import sys

from row import Row
from config import Config
from stock import Stock

def main():
  with io.open(Config.SAMPLE_INFILE, buffering=Config.BUFFER_SIZE) as infile:
    stock = None
    for line in infile:
      row = Row(csv.reader([line]).next())
      if row.permno.isdigit():
        if not stock or not stock.same_stock(row):
          if stock:
            stock.done()
          stock = Stock(row)
        else:
          stock.next_row(row)
    stock.done()

if __name__ == '__main__':
  sys.exit(main())
