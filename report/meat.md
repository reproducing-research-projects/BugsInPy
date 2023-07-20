<!--

This is a comment in Markdown (not rendered).

Keep each sentence in this file on a new line.
That line-break doesn't get rendered, and it makes line-based diff/merge work better.

Also, a reminder on how to add citations:

1. Create a Zotero database.
2. Tag all the things you want to cite with a specific tag, e.g., "bugsinpy-reproduction"
3. Click that tag and Ctrl+A to select all references with that tag.
4. Right click > Export Items with format BibLaTeX into `bugsinpy/report/your_name.bib`
5. insert `\addbibresource{your_name.bib}` to `main.tex`

-->

# Introduction

BugsInPy \cite{widyasari_bugsinpy_2020} is a curated dataset of real-world bugs in large Python projects.
BugsInPy is intended to be used by researchers to develop and evaluate software testing and debugging tools for Python on a diverse set of real-world bugs from multiple projects.
This can help to ensure that the tools are effective in detecting real-world bugs.

BugsInPy is used in many software engineering studies \cite{mukherjee_fixing_2021, smytzek_sflkit_2022, hirsch_systematic_2022, lukasczyk_empirical_2023, akimova_survey_2021}. Researchers and practitioners have leveraged the dataset to investigate different aspects of bug detection, fixing, and software reliability. BugsInPy has become an great resource for advancing the field of software engineering and fostering innovation in bug detection and fixing techniques.

The BugsInPy dataset contains a variety of information about each bug, including:

- A buggy commit
- A fixed commit
- Python version used
- Test cases that indicate the bugs presence

<!-- Double check source here

Source checked only report commit, python version ans test case
requirements.txt is not avilable in all projects
setup script is not available in all projects
-->

BugsInPy includes a database abstraction layer and a test execution framework.
The database abstraction layer provides a way to access the dataset in a structured way.
The test execution framework allows researchers to run the test cases that reveal the bugs.

BugsInPy is a valuable resource for researchers who are developing and evaluating software defect detection tools.
The dataset provides a large and diverse set of bugs that can be used to test the effectiveness of these tools.
BugsInPy also includes a variety of tools and resources that can help researchers to use the dataset effectively.

We sought to use the BugsInPy framework to verify that the test cases could be set up, that the buggy commit fails, and that the fixed commit passes.
This is a _reproduction_ \cite{acm_inc_staff_artifact_2020} of the original work, since we are using the original framework.

Our contributions are:

- A new script which can invoke the BugsInPy framework _en masse_.
- Modifications to the BugsInPy framework to install and use the correct version of Python.
- The results of which bugs were reproducible (software environment installs, buggy version fails exactly that one test, fixed version passes all tests).

This article proceeds with the methodology section, which explains what tools we used to run these codes reproducible.
Then we summarize the results of our executions and analyze the failures.
Finally, we engage in an open-ended discussion of our experiment with advice to authors of reproducible artifacts and those seeking to reproduce artifacts.

<!--
In the above section, don't mention Docker yet.
That is an "implementation detail".
Instead, use the term container or container image.

Replaced term docker by container in this section
-->

# Methodology

<!--
TODO
whether to cite faustinoaqbugsinpy-testall or just refer to the appendix.
-->

We would like to answer the following questions:

**RQ1.** How many of the bugs in BugsInPy are reproudcible with no "extra" work?
For a bug to be reproducible, the software environment should install without failure, the buggy verison should fail the identified test case, and the fixed version should pass.

**RQ2.** How many of those which are not reproducible can we rescue?
We rescue a bug by modifying the scripts and data such that the bug is reproducible.

As part of our rescue, we made the following changes:

1. We use a container build script to provide a consitent starting point in which our scripts will install the correct software environment.
Running in a container also sandboxes modifications that the BugsInPy script wants to make (e.g., modifying `~/.bashrc`).
While this image is available in this registry \cite{faustinoaqbugsinpy-testall}, we suggest users build the image themselves rather than depending on this registry to remain available.

2. For each bug, The BugsInPy script ignores the specified version of Python, deferring to the system default Python instead.
Presumably, the BugsInPy authors manually changed their system's version of Python according to the specification of each bug, but this is not an automated process, and that makes it difficult for future users.
We modified this script to install the correct version of Python using Conda.
Conda is a cross-platform package manager.
Packages installed by Conda neither use nor modify the system version of those packages, so Conda can support different environments each with their own possibly conflicting requirements.
Conda package repositories store packages containing pre-compiled binaries and metadata for each platform, so installing is rather quick.

3. The original BugsInPy scripts install all Python packages using Pip package manager.
Pip can invoke the compiler to build dependencies from source \cite{noauthor_pip_nodate} or download prebuilt binary files.
<!--
The most common usage of pip is to install packages from the Python Package Index (PyPI) using requirement specifiers.
As specified in the official Python Packaging documentation, a requirement specifier typically consists of a project name followed by an optional version specifier.
The specification for requirement specifiers can be found in PEP 440, which provides a comprehensive guide to the currently supported specifiers \cite{noauthor_installing_nodate}.
-->
However, some packages may require additional system libraries or dependencies that cannot be installed solely through pip.
For example, Matplotlib, a popular Python plotting library, has certain system-level dependencies that pip cannot automatically handle, such as libpng, freetype, or Tk, which are required for Matplotlib to function properly \cite{noauthor_installation_nodate}.
Consequently, if a bug in a project's environment depends on Matplotlib, attempting to install and run that project on a vanilla Ubuntu or Debian system without the necessary system libraries would result in installation failures.
<!--
In such cases, it becomes the responsibility of the user or system administrator to ensure that the required system libraries are installed manually before attempting to install the package with pip.
The Matplotlib documentation provides detailed instructions on how to install the necessary system-level dependencies for different platforms \cite{noauthor_contributing_nodate}.
By following these instructions and setting up the required libraries, users can successfully install and utilize Matplotlib and any other package with similar external dependencies.
-->
Presumably the original authors manually modified their system to have these system libraries; in our case, we identify packages that Pip cannot install on vanilla Ubuntu or Debian and simply install those with Conda instead.

4. Building the environment from source can be quite costly, so we reuse environments when the Python package requirements and Python versions are exactly the same.
This optimization helps reduce the time and resources required for environment setup, as the costly process of building environments from source can be bypassed.
While it is tempting to use the same Conda environment for each project, there are multiple occasions where different bugs of the same project require different dependencies.
For example, `ansible/bugs/{1,11,14}/requirements.txt` all vary subtly.

5. The BugsInPy framework correctly recognizes that installing the dependencies line by line `cat requirements.txt | filter | xargs -n 1 pip install`, rather than using `pip install -r requirements.txt`, bypasses certain restrictions imposed by pip.
Specifically, when installing all dependencies at once, pip may ignore very old packages. However, installing the dependencies sequentially allows us to reproduce the bugs accurately.
However, this results in failed  installations for projects that include the `-e git+https://...` syntax in their `requirements.txt` file, since they would get passed along as `pip install -e` and `pip install git+https://...`.
This revised code ensures that each line from the requirements.txt file is properly processed and passed as an argument to the `pip install` command.
<!-- TODO: check this -->

By utilizing the modified approach, we were able to resolve the installation issues for specific repository dependencies. For instance, the installation of the `luigi` library from a specific GitHub repository now proceeds as expected, as evidenced by the successful cloning and checkout of the specified commit.

To address this issue, we have opened a pull request in the original repository \cite{noauthor_fixes_nodate}. This fix is crucial, as it impacts the reproducibility of bugs in projects such as black, cookiecutter, keras, luigi, pandas, sanic, and thefuck.

# Results

\begin{table}[htbp]
\centering
\caption{Reproduction of bugs in BugsInPy without modification}
\label{tab:unmodified-reproduction}
\scriptsize
\begin{tabular}{lrrrrr}
\toprule
Project   &  Err &    Bth-pass &  Bth-fail &      Exp &          Total \\
\midrule
PySnooper & 2 (67\%) & 0 (0\%) & 0 (0\%) & 1 (33\%) & 3 (100\%)\\
ansible & 3 (17\%) & 0 (0\%) & 0 (0\%) & 15 (83\%) & 18 (100\%)\\
black & 1 (4\%) & 0 (0\%) & 0 (0\%) & 22 (96\%) & 23 (100\%)\\
cookiecutter & 2 (50\%) & 0 (0\%) & 0 (0\%) & 2 (50\%) & 4 (100\%)\\
fastapi & 0 (0\%) & 0 (0\%) & 0 (0\%) & 16 (100\%) & 16 (100\%)\\
httpie & 4 (80\%) & 0 (0\%) & 0 (0\%) & 1 (20\%) & 5 (100\%)\\
keras & 14 (31\%) & 0 (0\%) & 0 (0\%) & 31 (69\%) & 45 (100\%)\\
luigi & 33 (100\%) & 0 (0\%) & 0 (0\%) & 0 (0\%) & 33 (100\%)\\
matplotlib & 29 (97\%) & 0 (0\%) & 0 (0\%) & 1 (3\%) & 30 (100\%)\\
pandas & 47 (28\%) & 0 (0\%) & 0 (0\%) & 122 (72\%) & 169 (100\%)\\
sanic & 5 (100\%) & 0 (0\%) & 0 (0\%) & 0 (0\%) & 5 (100\%)\\
scrapy & 11 (28\%) & 0 (0\%) & 0 (0\%) & 29 (72\%) & 40 (100\%)\\
spacy & 2 (20\%) & 0 (0\%) & 0 (0\%) & 8 (80\%) & 10 (100\%)\\
thefuck & 8 (25\%) & 0 (0\%) & 0 (0\%) & 24 (75\%) & 32 (100\%)\\
tornado & 1 (6\%) & 0 (0\%) & 0 (0\%) & 15 (94\%) & 16 (100\%)\\
tqdm & 2 (22\%) & 0 (0\%) & 0 (0\%) & 7 (78\%) & 9 (100\%)\\
youtube-dl & 0 (0\%) & 0 (0\%) & 0 (0\%) & 43 (100\%) & 43 (100\%)\\
\midrule
Total & 164 (33\%) & 0 (0\%) & 0 (0\%) & 337 (67\%) & 501 (100\%)\\
\bottomrule
\end{tabular}
\end{table}

**RQ1.** With the original BugsInPy framework, we achieved the following bug reproduction rates \Cref{tab:unmodified-reproduction}.
In that table, the results we can get are:

- **Error**: Some part of the installation of the software environment needed to test the bug failed.
- **Both-pass**: Both versions pass; we would expect the buggy version to fail.
- **Both-fail**: Both versions fail; we would expect the fixed version to pass.
- **Expected**: The buggy version fails, and the fixed version passes. We consider _only_ these bugs, "reproduced".

In that table, for each project, we show the raw count as well as percentage of outcomes for all bugs in that project.
The last row shows the raw count as well as percentage of outcomes for all bugs in the dataset.

**RQ2.** We were able to rescue many of the broken test cases, as shown in \Cref{tab:unmodified-reproduction}.

\begin{table}[htbp]
\centering
\caption{Reproduction of bugs in BugsInPy, after rescuing}
\label{tab:rescued-reproduction}
\scriptsize
\begin{tabular}{lrrrrr}
Project   &  Err &    Bth-pass &  Bth-fail &      Exp &          Total \\
\midrule
PySnooper & 1 (33\%) & 0 (0\%) & 1 (33\%) & 1 (33\%) & 3 (100\%)\\
ansible & 0 (0\%) & 0 (0\%) & 0 (0\%) & 18 (100\%) & 18 (100\%)\\
black & 0 (0\%) & 0 (0\%) & 1 (4\%) & 22 (96\%) & 23 (100\%)\\
cookiecutter & 0 (0\%) & 0 (0\%) & 0 (0\%) & 4 (100\%) & 4 (100\%)\\
fastapi & 0 (0\%) & 0 (0\%) & 0 (0\%) & 16 (100\%) & 16 (100\%)\\
httpie & 0 (0\%) & 0 (0\%) & 0 (0\%) & 5 (100\%) & 5 (100\%)\\
keras & 3 (7\%) & 0 (0\%) & 1 (2\%) & 41 (91\%) & 45 (100\%)\\
luigi & 0 (0\%) & 6 (18\%) & 0 (0\%) & 27 (82\%) & 33 (100\%)\\
matplotlib & 3 (10\%) & 1 (3\%) & 0 (0\%) & 26 (87\%) & 30 (100\%)\\
pandas & 4 (2\%) & 0 (0\%) & 0 (0\%) & 165 (98\%) & 169 (100\%)\\
sanic & 0 (0\%) & 0 (0\%) & 0 (0\%) & 5 (100\%) & 5 (100\%)\\
scrapy & 0 (0\%) & 2 (5\%) & 0 (0\%) & 38 (95\%) & 40 (100\%)\\
spacy & 1 (10\%) & 0 (0\%) & 0 (0\%) & 9 (90\%) & 10 (100\%)\\
thefuck & 0 (0\%) & 0 (0\%) & 0 (0\%) & 32 (100\%) & 32 (100\%)\\
tornado & 0 (0\%) & 0 (0\%) & 0 (0\%) & 16 (100\%) & 16 (100\%)\\
tqdm & 0 (0\%) & 0 (0\%) & 0 (0\%) & 9 (100\%) & 9 (100\%)\\
youtube-dl & 0 (0\%) & 0 (0\%) & 0 (0\%) & 43 (100\%) & 43 (100\%)\\
\midrule
Total & 12 (2\%) & 9 (2\%) & 3 (1\%) & 477 (95\%) & 501 (100\%)\\
\bottomrule
\end{tabular}
\end{table}

Analyzing the specific project results, we can observe variations in the success rates. Some projects, such as Ansible, Cookiecutter, FastAPI, Httpie, Sanic, Thefuck, Tornado, and Tqdm, show a 100% success rate in reproducing and passing the bug tests for both the buggy and fixed versions.
On the other hand, projects like Pandas, Keras, Scrapy, and Matplotlib have a lower success rate in reproducing and passing the bug tests.
Note that our bugs are _repeatable_, which means that we can run our code twice and get the same result \cite{acm_inc_staff_artifact_2020}.

<!--
These results provide valuable insights into the quality, reliability, and effectiveness of the bug fixing process for each project.
Project maintainers can utilize these findings to prioritize bug fixes, allocate resources for improving code quality, and enhance the overall reliability and stability of the software.

Says more about the original dataset than anything else.
-->

By achieving a high success rate in reproducing bugs and passing tests, the BugsInPy dataset demonstrates the effectiveness of the bug fixing process and highlights the overall quality of the codebase.
With over 95% of bugs being successfully reproduced and passing the tests, researchers have more bugs at their disposal for evaluating fuzzing, automatic program repair repair, and other research techniques.

The success rate also indicates that the projects in the BugsInPy dataset have undergone rigorous testing and debugging processes.
This level of thoroughness contributes to improved software quality and can inspire trust among users and stakeholders.

<!--
The variations in success rates among different projects provide further insights.
Projects with a 100% success rate in reproducing and passing tests demonstrate excellent code quality and a robust bug fixing process.
Conversely, projects with a lower success rate may require additional attention and improvements in their debugging and testing practices.

Can't really draw that conclusion; could be lack of data.
-->

\Cref{tab:reproduction-time} presents the running time required to reproduce bugs in each project within the BugsInPy dataset, along with the respective containers.
The provided running times are specific to the reproduction process on the given VM configuration, which had 8GB of RAM, 4 cores, and 100GB of free disk space.
Reproduction times can vary depending on hardware resources, system configurations, and other environmental factors.
The projects are sorted based on their running time in descending order, with the project "pandas" having the highest running time of 963 minutes, followed by "luigi," "scrapy," and so on.

\begin{table}[htbp]
\centering
\caption{Reproduction Time for Bugs in Each Project}
\label{tab:reproduction-time}
\begin{tabular}{lrr}
\toprule
Project & Running Time (minutes) \\
\midrule
pandas       & 963 \\
luigi        & 510 \\
scrapy       & 268 \\
keras        & 230 \\
black        & 214 \\
fastapi      & 197 \\
thefuck      & 195 \\
sanic        & 136 \\
spacy        & 131 \\
ansible      & 80  \\
tqdm         & 36  \\
youtube-dl   & 59  \\
cookiecutter & 40  \\
httpie       & 39  \\
matplotlib   & 26  \\
tornado      & 14  \\
pysnooper    & 5   \\
\bottomrule
\end{tabular}
\end{table}

Additionally, it is noteworthy that the "pandas" project has the most bugs registered in the dataset, with a total of 169 bugs out of the 501 bugs analyzed.
The reproduction of bugs in the "pandas" project required a relatively longer running time, taking approximately 963 minutes.
The extended time may be attributed to factors such as the complexity of the codebase, the number of bugs present in the project, and the specific characteristics of the bugs encountered during the reproduction process.

The inclusion of Python version information in the bug dataset is crucial for ensuring the reproducibility of tests executed for bug detection and fixing.
Often, packages required by the software environment are only installable in a specific version of Python.

\begin{table}[htbp]
\centering
\caption{Python Versions in BugsInPy Dataset}
\label{tab:reproduction-py-versions}
\begin{tabular}{lll}
\toprule
Python & Bugs \\
\midrule
3.6.9 & 31  & 6\%   \\
3.7.0 & 58  & 12\%  \\
3.7.3 & 50  & 10\%  \\
3.7.4 & 33  & 7\%   \\
3.7.7 & 9   & 2\%   \\
3.8.1 & 33  & 7\%   \\
3.8.3 & 287 & 57\%  \\
Total & 501 & 100\% \\
\bottomrule
\end{tabular}
\end{table}

\Cref{tab:reproduction-py-versions} provides a summary of Python versions and their corresponding counts in the BugsInPy dataset.
The percentages give us insights into the distribution of bugs across different Python versions in the dataset.
The dataset certainly shows its age; Python 3.6 and 3.7 reached their official end-of-life and are not supported by CPython developers \cite{cpython_developers_status_nodate}.

# Discussion

## What makes our reproduction easy?

The ease of bug reproduction in the BugsInPy dataset can be attributed to several factors:

1. **Automatation**: The `bugsinpy-testall` script provides an automated approach to reproducing and testing bugs in Python projects.
The script streamlines the reproduction process, minimizes manual effort, and ensures we use a consistent procedure on each project.
Note that these automation scripts must be carefully written and maintained.
In particular, the original scripts did not have `set -e`, so some intermediate step might fail without alerting the user.

2. **Environment/Package manager**: Conda environment/package manager contributes to easy management of project dependencies.
The key insight is that Conda can install packages to a local environment without interferring with global, system-wide packages.
This makes it possible to define project-specific versions of libraries which would be normally managed by a platform-specific system-wide package manager.

3. **Lack of non-deterministic bugs**: None of the bugs in our dataset are race-conditions.
Our scope is limited to constructing a reproducible software environment consistent with the original bug, and then the bug will show itself deterministically.

These factors collectively contribute to the ease of reproducing bugs in the BugsInPy dataset, providing a reliable and efficient framework for bug analysis and investigation.

## What makes our reproduction hard?

Despite the facilitative factors mentioned above, bug reproduction can still present challenges due to the following factors:

1. **Resource constraints during building**: Projects with a large number of bugs can pose challenges in terms of the time and resources required for bug reproduction.
Sometimes, the software environment will involve a computationally-expensive step of building software from source.
Reproducing and testing a significant number of bugs within limited resources may result in longer reproduction times and potential resource limitations.

1. **Lack of storage**: Our script ends up with quite a few Conda environments.
These can be quite expensive to store, and we can't, for example, archive our environments in GitHub, due to space constraints.

1. **Missing packages in Conda**: Unfortunately, not all Pip packages and versions exist in our selected Conda repositories.

Addressing these challenges requires careful consideration of project-specific factors and may involve additional research, debugging techniques, and resources to ensure accurate and reliable bug reproduction.

## Recommendations to artifact authors

For authors providing Python research artifacts, the following recommendations can enhance the reproducibility of their artifacts:

1. **`requirements.txt` is not enough**:
Pip cannot handle library dependencies.
Researchers should provide a container, a Conda lockfile, Spack lockfile, or other detailed environment specification.

1. **Archival storage**: Ensure that the artifact repository is archived in long-term storage such as Zenodo or FigShare, so that it does not become bit rot.

1. **Make it automatic/easy to use**: The BugsInPy dataset has Python versions, but there is no automation to switch to a specific version, so users are unlikely to do so.
Our improved version uses Conda to automatically switch to the right Python version.

## Threats to Validity

It may be possible that some of these bugs are reproducible, but the error is on our side.
In particular, the authors do release data on the Python version, but none of their scripts make use of that information.
Furthermore, we believe our efforts reflect an "average" user effort with limited resources, not a researcher with infinite time to reproduce every bit of the BugsInPy dataset.

It may be possible that our work is not reproducible for the following reasons:

1. Although we pin our Docker base images exact version, it is possible that the source location (DockerHub) stops hosting our image (e.g., goes out of business, ends free tier).
In this case, one would need to change the base image, but it should still work, so long as that base image has Conda.

2. Conda package repositories can stop existing (e.g., if Anaconda goes out of business) or drop the old package versions we refer to.
However, the definition of Conda packages describes how to build the packages from source.
The package definitions are smaller than the package binaries, so they may remain longer.

3. The reproducers might not have enough computational resources to do the reproduction in a timely manner.
However, we reuse Conda environments to minimize the computational cost.
Furthermore, our scripts support reproducing just one project or just one bug from one project.

# Conclusion

The study presented in this paper demonstrates the effectiveness of the BugsInPy dataset in reproducing and testing bugs in Python projects.
The standardized and automated approach provided by the `bugsinpy-testall` script, coupled with the use of Conda for dependency management, streamlines the bug reproduction process and enhances its ease.

The high success rate in reproducing bugs, with over 95% of bugs passing the tests, indicates the reliability and accuracy of the bug fixes in the dataset.

However, challenges still exist in reproducing certain bugs due to complex codebases, interdependencies, intermittent nature, and resource constraints.
Addressing these challenges requires further research, debugging techniques, and allocation of appropriate resources.

To improve the reproducibility of BugsInPy, it is recommended to enhance the documentation and description of software environments, making reproducibility tools more accessible and user-friendly.
Collaboration within the Python community can also foster a supportive and collaborative environment for addressing challenges and enhancing the reproducibility process.

