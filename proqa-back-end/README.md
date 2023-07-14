# proqa-back-end
Temporarily, the contributing.MD has been copied into here for higher visibility.
## Pipenv
Pipenv is a virtual environment used to easily manage our dependencies.

Make sure you have pipenv installed.
```
pip install pipenv
```

First, sync the virtual environment with the dev dependencies.
```
pipenv sync -d
```

Then you need to activate the virtual environment.
```
pipenv shell
```

To install a package into the virtual enviornment and commit it into the repo you can do the following. Use the -d argument only if this is a developer package (such as pytest).
```
pipenv install -d <library>
```

Before commiting you must lock the dependencies.
```
pipenv lock
```

## Docker compose
Docker is used to create isolated containers for each of our individual applications.
We use a docker compose file to easily launch all of the applications for development.
First, you should install the [docker application](https://docs.docker.com/compose/install/).
To launch the django app along with the postgres database locally, you can run the following command.
```
docker compose up -d --build
```
If you are on Linux and encounter permission issues, use the following command to allow your user to access the .data folder.
```
sudo setfacl -m u:$(id -u):rwx -R ./.data
```
This creates the containers, and launches them in the detached mode, to remove the containers you can run
```
docker compose down
```
To run terminal commands in the containers, you can run the following to access a bash terminal for django (this can be replaced with postgres/redis).
```
docker compose exec django bash
```

## Django
Django is the library we use to manage our data as well as the admin dashboard. When you make changes to django models (aka anything that will change SQL schema), migrations must be made for these changes to take effect. To do this, first follow the docker steps and enter the django bash. Note that any other changes in django will be autmatically reflected after a save.
```
python manage.py makemigrations
```
This creates the migration files. To actually migrate the dataset, run this.
```
python manage.py migrate
```
Note that running the docker compose file will automatically migrate for you if there are any unmigrated migrations.

## OpenID Mock Server Login
With the openID server, you can make a default user and relogin with the same user. You cannot assign admin rights, omly the superuser can do that. 

When making a new user through OpenID Mock server, you will need to use bothfields: 
<ol>
    <li> User/Subject
    <li> JSON Values
</ol>

In the first field, enter your desired username. This will be the username you use to log in again to the same account. In the second field, use the structure provided in the input-schema.json file to ensure you provide the correct credentials. Here is an example:

```
{
    "preferred_username": "test",
    "email": "test@gmail.com"
}
```

The preferred username is the username Django will associate you with. Its easier if the username entered in the first field and the preferred username are the same. By adding a preferred username, this will override Djangos automatic username allocation which assigns a random, long username. 

To relogin to the same user, you can just enter the same username you used in the first field. 

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
For unit testing, we use a library called ```pytest``` which looks for files whose names match the patterns ```*_test.py``` or ```test_*.py```. We use the second format. If you have a file with functions that need to be unit tested in a directory of a Django app ```djangoapp```:
    <p> ```feature.py``` </p>
The corresponding unit tests should be written into the corresponding app directory ```djangoapp/tests``` (see example in ```chatbox``` app), with the filename
    <p> ```test_feature.py``` </p>
Additionally, the functions that you want to test should follow the same convention. That is, if your ```feature.py``` defines a function:
    <p> ```def do_stuff()``` </p>
The ```feature_test.py``` file should define its unit test:
    <p> ```def test_do_stuff()``` </p>

```pytest``` also offers additional features, e.g. marking a specific test so that it gets skipped. You can read about this in the ```pytest``` docs.

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
