"""
Constant values used in program.
"""

MAX_RECORD_LENGTH = 3
MIN_NUMBER = -100
MAX_NUMBER = 100
MAX_BLOCK_SIZE = 48  # in bytes
RECORD_SIZE = 12  # in bytes
DEFAULT_NUMBER_OF_RECORDS = 1000
b = MAX_BLOCK_SIZE / RECORD_SIZE
# test: length: 3, block_size: 48, record_size: 12
# default      15,            300,              60
