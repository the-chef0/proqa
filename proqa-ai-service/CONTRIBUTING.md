## Pipenv
Pipenv is a virtual environment used to easily manage our dependencies.

First, you need to sync your virtual environment with the dev dependencies.
`pipenv sync -d`

Then you need to activate the virtual environment.
`pipenv shell`

To install a package into the virtual enviornment and commit it into the repo you can do the following. Use the -d argument only if this is a developer package (such as pytest).
`pipenv install <library> -d` 

Before commiting you must lock the dependencies.
`pipenv lock`

## General workflow
The steps below describe the procedure for doing any kind of coding within this project. They provide a general overview, with more detailed instructions being provided in the sections below.

<ol>
    <li> Create a new branch to write the changes you want to introduce, naming it according to our conventions. </li>
    <li> Write your code and unit tests (if applicable). </li>
    <li> Commit your changes. </li>
    <li> Repeat steps 2 and 3 until your implementation needs to be merged into the main branch, completing step 5 at least once before proceeding to step 6, i.e. creating your merge request.
    <li> Check if your new code passes the testing pipeline. If not, fix whatever needs to be fixed.
    <li> Create a merge request.
</ol>

## Branch naming conventions
We name our branches using the convention:
    <p>```change-type/change-name``` </p>
For example, if you're adding a new feature which will let the user upvote/downvote answers, you can name it something like:
    <p>```feature/answer-voting``` </p>

## Unit testing
For unit testing, we use a library called ```pytest``` which looks for files whose names match the patterns ```*_test.py``` or ```test_*.py```. We use the second format. If you have a file with functions that need to be unit tested:
    <p> ```feature.py``` </p>
The corresponding unit tests should be written into a file called:
    <p> ```test_feature.py``` </p>
Additionally, the functions that you want to test should follow the same convention. That is, if your ```feature.py``` defines a function:
    <p> ```def do_stuff()``` </p>
The ```test_feature.py``` file should define its unit test:
    <p> ```def test_do_stuff()``` </p>
If there are multiple test cases for a given function, then the tests shall follow the following convention:
    <p> ```def test_do_stuff_given_<condition>_then_<expectation>()``` </p>

All test functions must be in the test directory.

## Testing pipeline
This project is set up so that every time you commit to the repo, it runs an automated sequence (a.k.a. a pipeline) of stages that check or ensure the correctness of the code. The stages each contain one or more job:
<ul>
    <li>
    Test
        <ul>
            <li> pytest - runs the unit tests. </li>
        </ul>
    </li>
    <li>
    Build
    </li>
    <li>
    Linting
        <ul>
            <li> isort - sorts imports according to PEP8 conventions. </li>
            <li> pylint - general linting, e.g. looking for bugs, offering refactoring suggestions, etc. </li>
        </ul>
    </li>
</ul>

To inspect the results of a pipeline for a commit, go to the menu on the left side of your screen in the project and go to <b> CI/CD -> Pipelines </b>. There you will see an overview of all the pipelines that ran for each commit. Find the entry corresponding to your commit (you can switch to the <b>Branches</b> tab to find the ones relevant to your branch) and look at the status badge. If it says "passed", you're good to go. If it says "failed" click on the badge to inspect each part of the pipeline individually.

On the following screen, you will see a breakdown of all the stages and an indication of which particular job failed. Since the entire pipeline terminates if a single job fails, inspect the output of the first job that failed and fix the issue.

Note that the pipeline also runs if you create a merge request. This is why it's important to make sure that the pipeline passes before you create a merge request. It will not be possible to merge unless the pipeline has passed.
