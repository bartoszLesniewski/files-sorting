"""
Constant values used in program.
"""

MAX_RECORD_LENGTH = 15
MIN_NUMBER = -100
MAX_NUMBER = 100
MAX_BLOCK_SIZE = 480  # in bytes
RECORD_SIZE = 60  # in bytes
DEFAULT_NUMBER_OF_RECORDS = 1000
b = MAX_BLOCK_SIZE / RECORD_SIZE
# test: length: 3, block_size: 48, record_size: 12
# default      15,            300,              60
