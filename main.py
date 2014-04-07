import csv
import io
import sys

from row import Row
from config import Config

def main():
  with io.open(Config.SAMPLE_INFILE, buffering=Config.BUFFER_SIZE) as infile:
    for line in infile:
      row = Row(csv.reader([line]).next())

if __name__ == '__main__':
  sys.exit(main())
