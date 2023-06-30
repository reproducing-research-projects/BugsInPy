# BugsInPy

BugsInPy: A Database of Existing Bugs in Python Programs to Enable Controlled Testing and Debugging Studies.
The objective of this work is to support reproducible research on real-world Python projects.

# Steps to set up BugsInPy

1. Clone BugsInPy:
   - `git clone https://github.com/soarsmu/BugsInPy`
2. Add BugsInPy executables path:
   - `export PATH=$PATH:<bugsinpy_path>/framework/bin`

# BugsInPy Command

| Command  | Description                                                                                                           |
| -------- | --------------------------------------------------------------------------------------------------------------------- |
| info     | Get the information of a specific project or a specific bug                                                           |
| checkout | Checkout buggy or fixed version project from dataset                                                                  |
| compile  | Compile sources from project that have been checkout                                                                  |
| test     | Run test case that relevant with bug, single-test case from input user, or all test cases from project                |
| coverage | Run code coverage analysis from test case that relevant with bug, single-test case from input user, or all test cases |
| mutation | Run mutation analysis from input user or test case that relevant with bug                                             |
| fuzz     | Run a test input generation from specific bug                                                                         |
| testall  | Reproduce all bugs buggy and fixed version for all projects                                                           |

# Example BugsInPy Command

- Help usage from checkout command:
  - `bugsinpy-checkout --help`
- Checkout a buggy source code version (youtube-dl, bug 2, buggy version):
  - `bugsinpy-checkout -p youtube-dl -v 0 -i 2 -w /temp/projects`
- Compile sources and tests, and run tests from current directory:
  - `bugsinpy-compile`
  - `bugsinpy-test`

# Example BugsInPy Docker

The docker enviroments make sure all the dependencies and specific python versions are met by using the [miniconda3 image](https://hub.docker.com/r/continuumio/miniconda3)

Prerequisite is `docker` please see [documentation](https://docs.docker.com/engine/install/)

- Build docker image using `Dockerfile`:
  - `docker build -t "bugsinpy-testall:Dockerfile" .`
- Run a new container based in the docker image:
  - `docker run -it bugsinpy-testall:Dockerfile /bin/bash`
- Reproduce all projects bugs running buggy and fixed versions:
  - `bugsinpy-testall`
