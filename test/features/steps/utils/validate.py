import re


# Validation utils

def validate_merkle_proofs(supplied, expected):
    count = re.findall(r'\d+', supplied)
    assert int(count[0]) == len(expected)
