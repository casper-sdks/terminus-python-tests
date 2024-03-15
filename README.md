## Terminus Python

This repo holds a set of tests to be run against the Casper Python SDK.

Points to note are:

- The tests can be run manually via the Terminus project [here](https://github.com/casper-sdks/terminus) 
- The tests are built using Cucumber features

### How to run locally

- Install python

- Clone the repo and initialise the test project

  ```bash
  git clone git@github.com:casper-sdks/terminus-python-tests.git
  
  cd terminus-python-tests/script && chmod +x terminus
  
  ./terminus init
  ```

- The default SDK branch and node docker location can be overriden in the terminus init command 

- ```bash
  ./terminus -b dev -n cctl:latest
  ```

- To view the defaults and other terminus commands, run

- ```bash
  ./terminus help
  ```

- To run the tests:

  ```bash
  ./terminus test
  ```

- JUnit test results will be output to /reports

### How to run locally IDE

Alternatively the tests can be run using an IDE

They are developed using JetBrains PyCharm

