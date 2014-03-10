import csv
import io
import sys

class Config:
  INFILE="data.csv"
  TINY_INFILE="tiny.csv"
  SAMPLE_INFILE="sample.csv"
  BUFFER_SIZE=1000 * 1024 * 1024

# io.open(file, mode='r', buffering=-1, encoding=None, errors=None, newline=None, closefd=True)

def main():
  with io.open(Config.INFILE, buffering=Config.BUFFER_SIZE) as infile:
    for line in infile:
      row = csv.reader([line]).next()

if __name__ == '__main__':
  sys.exit(main())
