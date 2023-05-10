import re

from dateutil import parser


# Validation utils

def validate_merkle_proofs(supplied, expected):
    count = re.findall(r'\d+', supplied)
    assert int(count[0]) == len(expected)


def compare_timestamps(t1, t2):
    return t1 == parser.parse(t2).timestamp()
