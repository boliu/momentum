import datetime

_ROW_NAMES=[
  'PERMNO',
  'date',
  'NAMEENDT',
  'SHRCD',
  'EXCHCD',
  'SICCD',
  'NCUSIP',
  'TICKER',
  'COMNAM',
  'SHRCLS',
  'TSYMBOL',
  'NAICS',
  'PRIMEXCH',
  'TRDSTAT',
  'SECSTAT',
  'PERMCO',
  'ISSUNO',
  'HEXCD',
  'HSICCD',
  'CUSIP',
  'DCLRDT',
  'DLAMT',
  'DLPDT',
  'DLSTCD',
  'NEXTDT',
  'PAYDT',
  'RCRDDT',
  'SHRFLG',
  'HSICMG',
  'HSICIG',
  'DISTCD',
  'DIVAMT',
  'FACPR',
  'FACSHR',
  'ACPERM',
  'ACCOMP',
  'NWPERM',
  'DLRETX',
  'DLPRC',
  'DLRET',
  'TRTSCD',
  'NMSIND',
  'MMCNT',
  'NSDINX',
  'BIDLO',
  'ASKHI',
  'PRC',
  'VOL',
  'RET',
  'BID',
  'ASK',
  'SHROUT',
  'CFACPR',
  'CFACSHR',
  'OPENPRC',
  'NUMTRD',
  'RETX',
  'vwretd',
  'vwretx',
  'ewretd',
  'ewretx',
  'sprtrn',
]

_R2I = {}
for index, name in enumerate(_ROW_NAMES):
  _R2I[name] = index

# TODO: only needed for debugging
_row_id = 0

class Row:
  def __init__(self, parsed_array):
    global _row_id
    _row_id = _row_id + 1
    self._row_id = _row_id

    # TODO: Can make this faster by hard coding
    self.permno = parsed_array[_R2I['PERMNO']]
    self.date = parsed_array[_R2I['date']]
    self.exchcd = parsed_array[_R2I['EXCHCD']]
    self.price = parsed_array[_R2I['PRC']]
    self.volume = parsed_array[_R2I['VOL']]
    self.facpr = parsed_array[_R2I['FACPR']]
    self.bidlo = parsed_array[_R2I['BIDLO']]
    self.askhi = parsed_array[_R2I['ASKHI']]
    self.divamt = parsed_array[_R2I['DIVAMT']]

class ParsedFirstRow:
  def __init__(self, row):
    self._row_id = row._row_id
    self.parsed = True
    try:
      # TODO: Do this lazily.
      self.permno = int(row.permno)
      self.date = self.ParseDate(row.date)
    except ValueError:
      self.parsed = False

  @staticmethod
  def ParseDate(date):
    int_date = int(date)
    return datetime.date(year = (int_date / 10000) % 10000,
                         month = (int_date / 100) % 100,
                         day = int_date % 100)

class ParsedRow(ParsedFirstRow):
  def __init__(self, row):
    ParsedFirstRow.__init__(self, row)
    try:
      # TODO: Do this lazily.
      self.exchcd = int(row.exchcd)
      self.price = float(row.price)
      self.volume = int(row.volume)
      if row.facpr:
        self.facpr = float(row.facpr)
      else:
        self.facpr = 0.0
      self.bidlo = float(row.bidlo)
      self.askhi = float(row.askhi)
      if row.divamt:
        self.divamt = float(row.divamt)
      else:
        self.divamt = 0.0
    except ValueError:
      self.parsed = False

def test():
  parsed_array = ['10318', '19911230', '', '11', '3', '2860', '5766520', 'BLCC', 'BALCHEM CORP', '', 'BLCC', '', 'Q', 'A', 'R', '8237', '10810', '3', '2800', '5766520', '19911111', '', '', '', '', '19911227', '19911206', '1', '28', '280', '5523', '0', '0.33333', '0.33333', '', '', '', '', '', '', '1', '2', '5', '2', '6.875', '8', '6.875', '1500', '0.055156', '6.875', '7.875', '2020', '11.390625', '11.390625', '', '2', '0.055156', '0.020303', '0.020295', '0.012477', '0.012459', '0.021355', '', '', 'OTE', 'NTP', 'NTV', 'FALSE', '', '', '', '24.192675', '5.435184444', '13.125', '-20.24305556', '', '', '', '', '', '', '', '', '', '3', '6958', '1.33333', '1.6666625', '11.45830469', '13.3333', '11.45830469']
  row = Row(parsed_array)
  assert row.permno == '10318'
  assert row.date == '19911230'
  assert row.exchcd == '3'
  assert row.price == '6.875'
  assert row.volume == '1500'
  assert row.facpr == '0.33333'
  assert row.bidlo == '6.875'
  assert row.askhi == '8'
  assert row.divamt == '0'

  parsed_row = ParsedRow(row)
  assert parsed_row.permno == 10318
  assert parsed_row.date == datetime.date(1991, 12, 30)
  assert parsed_row.exchcd == 3
  assert parsed_row.price == 6.875
  assert parsed_row.volume == 1500
  assert parsed_row.facpr == 0.33333
  assert parsed_row.bidlo == 6.875
  assert parsed_row.askhi == 8
  assert parsed_row.divamt == 0.0

if __name__ == '__main__':
  test()
