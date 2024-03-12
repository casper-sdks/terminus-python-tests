## Terminus Python

This repo holds a set of tests to be run against the Casper Python SDK.

Points to note are:

- The tests can be run manually via the Terminus project [here](https://github.com/casper-sdks/terminus) 
- The tests are built using Cucumber features

### How to run locally

- Install python

- Clone repo and start NCTL (please note the NCTL Casper node version in the script 'docker-run')

  ```bash
  git clone git@github.com:casper-sdks/terminus-python-tests.git
  cd terminus-python-tests/script
  chmod +x test-node && ./test-node
  chmod +x docker-copy-assets && /docker-copy-assets 
  cd ..
  ```

- Edit and install the requirements file to use the desired SDK repo

  ```bash
  awk '{sub(/@dev/,"@$[required-branch]1' requirements.txt > temp.txt && mv temp.txt requirements.txt 
            
  pip install -r requirements.txt
  pip install behave
  ```

- Run the tests

  ```bash
  behave test/features --junit
  ```

- TODO script the above

- JUnit test results will be output to /reports

### How to run locally IDE

Alternatively the tests can be run using an IDE

They are developed using JetBrains PyCharm

