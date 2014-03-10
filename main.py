import csv
import io
import sys
from row import Row

class Config:
  INFILE="data.csv"
  TINY_INFILE="tiny.csv"
  SAMPLE_INFILE="sample.csv"
  BUFFER_SIZE=1000 * 1024 * 1024

def main():
  with io.open(Config.SAMPLE_INFILE, buffering=Config.BUFFER_SIZE) as infile:
    for line in infile:
      row = Row(csv.reader([line]).next())

if __name__ == '__main__':
  sys.exit(main())
