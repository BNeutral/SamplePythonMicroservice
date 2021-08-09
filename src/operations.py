'''
Supported operations on user balances
'''
from enum import Enum, IntEnum

class Operation(IntEnum, Enum):
    '''
    The supported operations.
    '''
    deposit = 1
    withdraw = 2
    