import re

from dateutil import parser
import datetime


# Validation utils

def validate_merkle_proofs(supplied, expected):
    count = re.findall(r'\d+', supplied)
    assert int(count[0]) == len(expected)


def compare_timestamps(t1, t2):
    return t1 == parser.parse(t2).timestamp()


def compare_dates(_iso, _timestamp):
    return datetime.datetime.fromisoformat(_iso).timestamp() == _timestamp.value
