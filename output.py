import sys

def _print_csv(args):
  for arg in args:
    sys.stdout.write(str(arg))
    sys.stdout.write(',')
  sys.stdout.write('\n')

def print_header():
  _print_csv((
      'ticker',
      'comnam',
      'permno',
      'entrydate',
      'entryPRC',
      'entryBIDLO',
      'entryASKHI',
      'entryVOL',
      'entryFactor',
      'exitdate',
      'exitPRC',
      'exitBIDLO',
      'exitASKHI',
      'exitVOL',
      'exitFactor',
      'divident',
      'PnL'))

def print_trasaction(
    ticker,
    comnam,
    permno,
    entrydate,
    entryPRC,
    entryBIDLO,
    entryASKHI,
    entryVOL,
    entryFactor,
    exitdate,
    exitPRC,
    exitBIDLO,
    exitASKHI,
    exitVOL,
    exitFactor,
    divident,
    PnL):
  _print_csv((
      ticker,
      comnam,
      permno,
      entrydate.strftime('%Y%m%d'),
      entryPRC,
      entryBIDLO,
      entryASKHI,
      entryVOL,
      entryFactor,
      exitdate.strftime('%Y%m%d'),
      exitPRC,
      exitBIDLO,
      exitASKHI,
      exitVOL,
      exitFactor,
      divident,
      PnL))
