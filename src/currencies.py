'''
Supported currency types.
'''
from enum import Enum, IntEnum

class Currency(IntEnum, Enum):
    '''
    The supported currencies.
    TODO: Autogenerate DB schema based on these.
          Then autodetect and changes to this enum so nobody accidentally breaks the database.
    '''
    ars = 1
    usdt = 2
    btc = 3

currency_decimals = {
    Currency.ars : 2,
    Currency.usdt : 2,
    Currency.btc: 8
}
