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

Prerequisite is `docker` and `docker compose` please see [documentation](https://docs.docker.com/engine/install/)

- Remove previous index and cleanup old containers before a new run:
  - `rm projects/index.csv`
  - `docker compose down`
- Reproduce all the bugs in a specific project:
  - `docker compose up setup youtube-dl --build`
- Reproduce all projects bugs running buggy (0) and fixed (1) versions
  - ⚠️ Reproduce all projects may require a lot of resources, tested successfully on 4 cores 8 RAM 100GB free drive space
  - `docker compose up --build`

# New script: `bugsinpy-testall`

The `bugsinpy-testall` script automates the execution of the BugsInPy dataset, which contains bugs in various Python projects.
The script reproduces the bugs, executes tests, and records the results.
It enhances the reproducibility of Python projects by providing a standardized process for reproducing and testing bugs in different projects.

Here's a summary of how the script works:

1. The script takes command-line arguments to control its behavior. It provides options to display help, perform cleanup, and specify projects or ranges of bugs to reproduce and test.

2. It creates a `temp/projects` directory to store the output and logs.

3. The script iterates over the specified projects or all projects in the `BugsInPy/projects` directory.

4. For each project, it determines the range of bugs to reproduce and test.

5. It executes the tests for each bug by performing the following steps:
   a. Checks if the bug has already been tested and skips it if so.
   b. Sets up the environment for testing the buggy (0) version:
      - Uses `bugsinpy-checkout` to checkout the buggy version.
      - Activates the proper Python environment using Miniconda (specified in the `bugsinpy_bug.info` file).
      - Compiles the project (if required) and runs the tests using `bugsinpy-test`.
      - Check if the buggy version fails as expected for the test specific to the bug and save the output in the `BugsInPy/projects/<repo>/bugs/<bugid>/bug_buggy.txt`.
      - Updates the `BugsInPy/projects/bugsinpy-index.csv` with the results `<repo>,<bugid>,buggy,fail`
   c. The it proceeds to test the fixed (1) version:
      - Uses `bugsinpy-checkout` to checkout the fixed version.
      - Compiles the project (if required) and runs the tests.
      - Activates the proper Python environment using Miniconda (specified in the `bugsinpy_bug.info` file).
      - Compiles the project (if required) and runs the tests using `bugsinpy-test`.
      - Check if the fixed version pass as expected for the test specific to the bug and save the output in the `BugsInPy/projects/<repo>/bugs/<bugid>/bug_fixed.txt`.
      - Updates the `BugsInPy/projects/bugsinpy-index.csv` with the results `<repo>,<bugid>,fixed,pass`

6. The script deactivates the Conda environment and repeats the process for the next bug in the project.

The `bugsinpy-testall` script improves reproducibility by providing a standardized and automated approach to reproduce and test bugs in Python projects. It ensures that bugs are tested consistently across different projects, enabling easier verification of bug fixes and facilitating the replication of test results. By logging the output and test results, it helps track the status of bug reproduction and provides a central record for analysis and further investigation.
