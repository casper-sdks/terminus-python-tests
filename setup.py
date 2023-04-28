import pycspr

# List of 3rd party python dependencies.
with open("requirements.txt", "r") as fstream:
    _REQUIRES = fstream.read().splitlines()

    pycspr